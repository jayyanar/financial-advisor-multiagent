# AgentCore Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Financial Advisor Multiagent System to Amazon Bedrock AgentCore Runtime. The deployment maintains all existing functionality while adapting to AgentCore's managed infrastructure.

## Prerequisites

### System Requirements
- Python 3.10 or higher
- Active AWS account with AgentCore access
- Existing virtual environment with Strands Agents installed
- AWS CLI configured with appropriate permissions

### Required Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "agentcore:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Installation

### 1. Install AgentCore Dependencies

```bash
# Activate existing virtual environment
source .venv/bin/activate

# Install AgentCore toolkit
pip install bedrock-agentcore-starter-toolkit

# Verify installation
python -c "from bedrock_agentcore.runtime import BedrockAgentCoreApp; print('AgentCore installed successfully')"
```

### 2. Create Requirements File

Create `requirements-agentcore.txt`:
```text
# AgentCore runtime
bedrock-agentcore-starter-toolkit>=1.0.0

# Existing system dependencies
strands-agents>=1.10.0
strands-agents-tools>=0.2.9
duckduckgo-search>=6.3.4
boto3>=1.40.0
pydantic>=2.11.0
```

## Implementation

### 1. Create AgentCore Wrapper

Create `financial_advisor_agentcore.py`:

```python
#!/usr/bin/env python3
"""
AgentCore-compatible wrapper for Financial Advisor Multiagent System.

This module adapts the existing financial advisor system to work with
Amazon Bedrock AgentCore Runtime while preserving all functionality.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

# Initialize AgentCore app and financial advisor
app = BedrockAgentCoreApp()
advisor = FinancialAdvisorOrchestrator()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_agentcore_payload(payload: Dict[str, Any]) -> str:
    """
    Extract and validate user query from AgentCore payload.
    
    Args:
        payload: AgentCore request payload with 'prompt' field
        
    Returns:
        str: Processed user query for financial advisor system
        
    Raises:
        ValueError: If payload is invalid or missing required fields
    """
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")
    
    user_query = payload.get("prompt", "").strip()
    
    if not user_query:
        return ("Please provide a financial advisory request. "
                "Include ticker symbol, risk tolerance (Conservative/Moderate/Aggressive), "
                "and investment horizon (Short-term/Medium-term/Long-term) for best results.")
    
    # Basic input sanitization
    if len(user_query) > 5000:
        user_query = user_query[:5000] + "..."
        logger.warning("User query truncated due to length")
    
    return user_query


def format_agentcore_response(advisor_response: str, 
                            metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format financial advisor response for AgentCore compatibility.
    
    Args:
        advisor_response: Response from FinancialAdvisorOrchestrator
        metadata: Optional metadata to include in response
        
    Returns:
        dict: AgentCore-compatible response structure
    """
    response = {
        "result": advisor_response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": "financial-advisor-multiagent",
        "version": "1.0.0"
    }
    
    if metadata:
        response["metadata"] = metadata
    
    return response


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    AgentCore entry point for financial advisory requests.
    
    This function serves as the main interface between AgentCore Runtime
    and the Financial Advisor Multiagent System. It processes incoming
    requests and returns structured responses.
    
    Args:
        payload: AgentCore payload containing user request
            Expected format: {"prompt": "user query string"}
            
    Returns:
        dict: Structured response with analysis results
            Format: {"result": "analysis", "timestamp": "iso_date", ...}
            
    Example:
        >>> payload = {"prompt": "Analyze AAPL for moderate risk investor"}
        >>> response = invoke(payload)
        >>> print(response["result"])
    """
    try:
        # Log request (without sensitive data)
        logger.info(f"Processing financial advisory request")
        
        # Extract and validate user query
        user_query = process_agentcore_payload(payload)
        
        # Process through existing orchestrator
        logger.info("Invoking financial advisor orchestrator")
        advisor_response = advisor.analyze(user_query)
        
        # Format response for AgentCore
        response = format_agentcore_response(
            advisor_response,
            metadata={"query_length": len(user_query)}
        )
        
        logger.info("Financial advisory request completed successfully")
        return response
        
    except ValueError as e:
        # Invalid payload format
        error_msg = f"Invalid request format: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent"
        }
        
    except Exception as e:
        # General system errors
        error_msg = "An error occurred processing your financial advisory request"
        logger.error(f"Financial advisor error: {e}", exc_info=True)
        return {
            "error": error_msg,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent"
        }


if __name__ == "__main__":
    logger.info("Starting Financial Advisor AgentCore Runtime")
    app.run()
```

### 2. Local Testing

Create `test_agentcore_local.py`:

```python
#!/usr/bin/env python3
"""
Local testing script for AgentCore financial advisor deployment.
"""

import json
import requests
import time
from typing import Dict, Any


def test_health_endpoint():
    """Test the health check endpoint."""
    try:
        response = requests.get("http://localhost:8080/ping", timeout=5)
        print(f"Health check: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_financial_analysis(payload: Dict[str, Any]):
    """Test financial analysis endpoint."""
    try:
        response = requests.post(
            "http://localhost:8080/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response keys: {list(result.keys())}")
            if "result" in result:
                print(f"Analysis preview: {result['result'][:200]}...")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False


def main():
    """Run comprehensive local testing."""
    print("=== AgentCore Financial Advisor Local Testing ===\n")
    
    # Wait for server startup
    print("Waiting for server startup...")
    time.sleep(2)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    if not test_health_endpoint():
        print("❌ Health check failed - server may not be running")
        return
    print("✅ Health check passed\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Basic stock analysis",
            "payload": {"prompt": "Analyze AAPL stock for moderate risk investor"}
        },
        {
            "name": "Complete analysis request",
            "payload": {"prompt": "I want to invest in TSLA with aggressive risk tolerance and short-term horizon"}
        },
        {
            "name": "Missing information",
            "payload": {"prompt": "Tell me about investing"}
        },
        {
            "name": "Empty prompt",
            "payload": {"prompt": ""}
        }
    ]
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 2):
        print(f"{i}. Testing: {test_case['name']}")
        success = test_financial_analysis(test_case["payload"])
        print(f"{'✅' if success else '❌'} {test_case['name']}\n")


if __name__ == "__main__":
    main()
```

## Deployment Process

### 1. Configure AgentCore

```bash
# Configure deployment
agentcore configure --entrypoint financial_advisor_agentcore.py

# Verify configuration
agentcore status
```

### 2. Deploy to AWS

```bash
# Launch to AgentCore Runtime
agentcore launch

# Monitor deployment status
agentcore status

# View logs
agentcore logs
```

### 3. Test Deployment

```bash
# Test with sample request
agentcore invoke '{"prompt": "Analyze NVDA for moderate risk investor with medium-term horizon"}'

# Test error handling
agentcore invoke '{"invalid": "payload"}'
```

## Monitoring and Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed in the deployment environment
   - Verify `financial_advisor_multiagent.py` is in the same directory

2. **Model Access Errors**
   - Check AWS credentials and permissions
   - Verify Bedrock model access in the deployment region

3. **Web Search Failures**
   - DuckDuckGo API may be rate-limited
   - Check network connectivity from AgentCore environment

### Monitoring Commands

```bash
# View real-time logs
agentcore logs --follow

# Check resource usage
agentcore metrics

# Test connectivity
agentcore invoke '{"prompt": "test"}'
```

## Security Best Practices

### 1. Credential Management
- Use IAM roles instead of hardcoded credentials
- Rotate access keys regularly
- Monitor AWS CloudTrail for unusual activity

### 2. Input Validation
- Implement strict input sanitization
- Set reasonable request size limits
- Monitor for unusual query patterns

### 3. Error Handling
- Sanitize error messages before returning to users
- Log detailed errors internally for debugging
- Implement structured error responses

### 4. Monitoring
- Enable CloudWatch logging and metrics
- Set up alerts for error rates and response times
- Monitor token usage patterns

## Performance Optimization

### 1. Token Management
- Maintain 2000-token conservative limits
- Monitor token consumption patterns
- Implement token-based rate limiting if needed

### 2. Response Times
- Web search introduces latency (2-5 seconds typical)
- Multiple agent invocations run sequentially
- Consider timeout handling for long analyses

### 3. Scaling Considerations
- AgentCore handles horizontal scaling automatically
- Stateless design supports concurrent users
- Monitor resource usage and adjust as needed

## Validation Checklist

- [ ] All dependencies installed correctly
- [ ] Local testing passes all test cases
- [ ] AgentCore configuration successful
- [ ] Deployment to AWS completes without errors
- [ ] Remote testing produces expected results
- [ ] Error handling works correctly
- [ ] Educational disclaimers present in all outputs
- [ ] Performance meets acceptable thresholds
- [ ] Security best practices implemented
- [ ] Monitoring and logging configured

## Support and Resources

- **AgentCore Documentation**: [AWS AgentCore Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- **Strands Agents SDK**: [Strands Documentation](https://docs.strands.ai/)
- **Issue Reporting**: Create issues in the project repository
- **AWS Support**: Use AWS Support for AgentCore-specific issues