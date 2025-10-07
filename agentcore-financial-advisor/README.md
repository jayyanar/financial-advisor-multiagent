# AgentCore Financial Advisor Deployment

This directory contains the AgentCore-compatible version of the financial advisor multiagent system, transformed to run on Amazon Bedrock AgentCore Runtime while maintaining all existing functionality and educational disclaimers.

## Overview

The AgentCore Financial Advisor is a comprehensive educational financial advisory system that orchestrates multiple specialized AI agents to provide structured financial guidance through:

- **Market Intelligence**: Web-based research and analysis using DuckDuckGo Search
- **Strategy Development**: Multi-strategy generation with risk alignment
- **Execution Planning**: Phase-based implementation with specific order types
- **Risk Assessment**: Multi-category risk evaluation with mitigation recommendations

**Important**: This system is for educational purposes only and does not provide licensed financial advice.

## Architecture

The system uses the "Agents as Tools" pattern with hierarchical orchestration:

```
Financial Coordinator Agent (Orchestrator)
├── Market Intelligence Agent (Research & Analysis)
├── Strategy Architect Agent (Strategy Development)  
├── Execution Planner Agent (Implementation Planning)
└── Risk Assessor Agent (Risk Analysis & Alignment)
```

The AgentCore wrapper (`financial_advisor_agentcore.py`) provides:
- HTTP server setup via `BedrockAgentCoreApp`
- Payload processing for AgentCore format
- Comprehensive error handling and logging
- Structured response formatting

## File Structure

```
agentcore-financial-advisor/
├── financial_advisor_agentcore.py    # AgentCore entry point wrapper
├── requirements.txt                  # All dependencies for deployment
├── README.md                        # This documentation
└── tests/                           # Test suite for AgentCore integration
    └── .gitkeep                     # Placeholder for test files
```

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **AWS Account**: With appropriate AgentCore permissions
- **Virtual Environment**: Recommended for dependency isolation
- **AgentCore CLI**: Installed and configured

### AWS Permissions
Your AWS account needs permissions for:
- Amazon Bedrock model access (Claude 3.5 Sonnet)
- AgentCore Runtime deployment and management
- CloudWatch logging (for monitoring)

### AgentCore CLI Installation
```bash
# Install AgentCore CLI (if not already installed)
pip install bedrock-agentcore-starter-toolkit
```

## Installation and Setup

### 1. Environment Setup

Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### 2. Install Dependencies

Install all required dependencies:
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `bedrock-agentcore-starter-toolkit>=1.0.0` - AgentCore runtime support
- `strands-agents>=1.10.0` - Core agent framework
- `strands-agents-tools>=0.2.9` - Agent tools and utilities
- `duckduckgo-search>=6.3.4` - Web search functionality
- `boto3>=1.40.0` - AWS SDK for Bedrock access

### 3. AWS Configuration

Configure AWS credentials:
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Local Testing

### 1. Start Local Server

Run the AgentCore application locally:
```bash
python financial_advisor_agentcore.py
```

The server will start on `http://localhost:8080` with endpoints:
- `POST /invocations` - Main agent invocation
- `GET /ping` - Health check

### 2. Test Basic Functionality

Test the health endpoint:
```bash
curl http://localhost:8080/ping
```

Test financial analysis:
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze AAPL stock for moderate risk investor with long-term horizon"}'
```

### 3. Test Various Query Formats

**Simple ticker query:**
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "TSLA analysis"}'
```

**Complete query with parameters:**
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Provide comprehensive analysis for Microsoft (MSFT) stock for an aggressive risk investor with medium-term investment horizon"}'
```

**Missing information query:**
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I want to invest in tech stocks"}'
```

### 4. Test Error Handling

**Invalid payload format:**
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"invalid": "payload"}'
```

**Empty prompt:**
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": ""}'
```

## AgentCore Deployment

### 1. Configure Deployment

Configure AgentCore with your entry point:
```bash
agentcore configure --entrypoint financial_advisor_agentcore.py
```

This creates the necessary configuration for deployment.

### 2. Deploy to AWS

Launch the agent to AgentCore Runtime:
```bash
agentcore launch
```

This command will:
- Package your application and dependencies
- Create necessary AWS resources (Lambda, API Gateway, etc.)
- Deploy to AgentCore Runtime infrastructure
- Provide deployment status and endpoint information

### 3. Test Deployed Agent

Test the deployed agent using AgentCore CLI:
```bash
# Basic test
agentcore invoke '{"prompt": "Analyze AAPL stock for moderate risk investor"}'

# Comprehensive test
agentcore invoke '{"prompt": "Provide detailed financial analysis for Tesla (TSLA) stock for an aggressive risk investor with short-term investment horizon"}'

# Test parameter extraction
agentcore invoke '{"prompt": "I want to invest in Amazon stock but need guidance on risk management"}'
```

### 4. Monitor Deployment

Check deployment status:
```bash
agentcore status
```

View logs:
```bash
agentcore logs
```

## Usage Examples

### Basic Stock Analysis
```json
{
  "prompt": "Analyze AAPL stock for moderate risk investor"
}
```

### Comprehensive Analysis with Parameters
```json
{
  "prompt": "Provide comprehensive financial analysis for Microsoft (MSFT) stock for an aggressive risk investor with long-term investment horizon. Include multiple trading strategies and detailed risk assessment."
}
```

### Investment Guidance Request
```json
{
  "prompt": "I'm interested in investing in renewable energy stocks. I have a conservative risk tolerance and a medium-term investment horizon. What should I consider?"
}
```

## Response Format

The system returns structured JSON responses:

### Successful Response
```json
{
  "result": "# Financial Analysis for AAPL...",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "system": "financial-advisor-multiagent",
  "metadata": {
    "version": "1.0.0",
    "agent_type": "financial_advisor",
    "educational_disclaimer": true,
    "response_format": "structured_analysis",
    "capabilities": [
      "market_intelligence",
      "strategy_development",
      "execution_planning",
      "risk_assessment"
    ],
    "disclaimer": "Educational purposes only - not licensed financial advice"
  }
}
```

### Error Response
```json
{
  "error": "Invalid request format: Please provide a financial advisory request...",
  "error_type": "validation_error",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "system": "financial-advisor-multiagent",
  "metadata": {
    "error_category": "payload_validation",
    "recoverable": true,
    "suggestion": "Please check your request format and try again"
  }
}
```

## System Capabilities

### Market Intelligence
- Real-time web research using DuckDuckGo Search
- SEC filing analysis and regulatory insights
- News aggregation and analyst commentary
- Historical performance analysis
- Source attribution for all research findings

### Strategy Development
- Minimum 5 distinct trading strategies per request
- Risk alignment (Conservative/Moderate/Aggressive)
- Investment horizon matching (Short/Medium/Long-term)
- Strategy categories: Growth, momentum, value, options-enhanced, pullback accumulation
- Clear rationale and risk assessment for each strategy

### Execution Planning
- Phase-based implementation with defined milestones
- Detailed order specifications (types, sizing, timing)
- Comprehensive risk controls (stop-loss, limit orders, hedging)
- Performance monitoring frameworks
- Technical analysis with support/resistance levels

### Risk Assessment
- Multi-category analysis (market, competitive, execution, strategy-specific)
- Alignment evaluation against user preferences
- Misalignment detection and conflict identification
- Actionable risk mitigation recommendations
- Portfolio context and diversification considerations

## Error Handling and Resilience

The system includes comprehensive error handling:

### Payload Validation
- Invalid or missing prompt field detection
- Helpful error messages with usage guidance
- Type validation for all input fields

### Web Search Resilience
- DuckDuckGo rate limit handling with retry guidance
- API failure graceful degradation
- Fallback responses when search is unavailable

### Agent Invocation Resilience
- Multiple parameter format attempts for model compatibility
- Fallback mechanisms for agent parameter errors
- Conservative 2000-token limits to prevent truncation

### Network and System Errors
- Connection error handling with retry suggestions
- Timeout detection and user guidance
- Memory/token limit exceeded handling
- Comprehensive logging for debugging

## Token Management

The system uses conservative token management:
- **Token Cap**: 2000 tokens per agent call
- **Fallback Mechanisms**: Multiple parameter format attempts
- **Input Truncation**: Automatic truncation when passing data between agents
- **Quality Preservation**: Balanced approach to maintain response quality

## Security Considerations

### Data Protection
- No sensitive financial data stored or logged
- Educational disclaimers prevent misuse as actual financial advice
- Session isolation provided by AgentCore Runtime

### API Security
- DuckDuckGo search uses public endpoints only
- Bedrock model access through IAM roles
- No API keys or credentials stored in code

### Access Control
- AgentCore Runtime handles authentication and authorization
- IAM roles control Bedrock model access
- Network isolation through AgentCore infrastructure

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Verify Strands Agents installation
python -c "from strands import Agent; print('Strands installed successfully')"
```

**2. AWS Credentials**
```bash
# Verify AWS configuration
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

**3. Local Server Issues**
```bash
# Check if port 8080 is available
lsof -i :8080

# Run with debug logging
python financial_advisor_agentcore.py --log-level DEBUG
```

**4. AgentCore Deployment Issues**
```bash
# Check AgentCore CLI configuration
agentcore status

# Verify deployment configuration
agentcore configure --list
```

### Error Messages

**"Invalid request format"**: Check that your payload includes a "prompt" field with a non-empty string.

**"Web search rate limit exceeded"**: Wait 60 seconds and retry. The system handles DuckDuckGo rate limits gracefully.

**"Agent configuration error"**: The system is using fallback mechanisms. This is normal and the request should still process.

**"Request timeout"**: Try simplifying your query or retry after a short delay.

## Performance Considerations

### Response Times
- Web search may introduce 2-5 second latency
- Multiple agent invocations run sequentially
- Complex analyses may take 10-30 seconds
- Timeout handling for long-running requests

### Scalability
- AgentCore Runtime handles scaling automatically
- Stateless agent design supports horizontal scaling
- Session isolation prevents interference between users
- Conservative token limits ensure consistent performance

### Optimization Tips
- Include specific ticker symbols for faster processing
- Specify risk tolerance and investment horizon explicitly
- Keep queries focused for better response times
- Use simple language for parameter extraction

## Educational Disclaimers

**Important**: This system is designed for educational purposes only:

- **Not Licensed Financial Advice**: All outputs are for educational exploration only
- **No Investment Recommendations**: Strategies are theoretical examples, not recommendations
- **Consult Professionals**: Always consult qualified financial advisors for actual investment decisions
- **No Performance Guarantees**: Past performance does not guarantee future results
- **Risk Awareness**: All investments carry risk of loss

## Support and Resources

### Documentation
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- [Strands Agents Framework](https://github.com/strands-ai/strands-agents)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)

### Getting Help
- Check the troubleshooting section above
- Review AgentCore logs using `agentcore logs`
- Verify AWS permissions and credentials
- Test locally before deploying to AgentCore

### Version Information
- **AgentCore Wrapper Version**: 1.0.0
- **Strands Agents**: >=1.10.0
- **Python**: 3.10+
- **AgentCore Runtime**: Latest

## Differences from Original System

This section documents the key differences between the AgentCore-compatible version and the original `financial_advisor_multiagent.py` system.

### Summary of Changes

The AgentCore version transforms the original standalone Python module into a web service that can be deployed on AWS managed infrastructure. The core transformation involves:

1. **HTTP Service Wrapper**: The `BedrockAgentCoreApp` wrapper converts the original system into an HTTP service with `/invocations` and `/ping` endpoints
2. **Payload Processing**: Input/output transformation between HTTP JSON payloads and the original system's string-based interface
3. **Deployment Integration**: AWS managed deployment through AgentCore CLI instead of local Python execution
4. **Error Response Formatting**: Structured JSON error responses instead of Python exceptions

**Key Preservation**: All core financial advisory logic, agent coordination, token management, and educational disclaimers remain identical to the original system.

### Architecture Differences

#### Original System Architecture
The original system is designed as a standalone Python module with direct instantiation:

```python
# Original system usage
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

advisor = FinancialAdvisorOrchestrator()
response = advisor.analyze("Analyze AAPL stock for moderate risk investor")
```

#### AgentCore System Architecture
The AgentCore version wraps the original system with HTTP service capabilities:

```python
# AgentCore wrapper structure
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

app = BedrockAgentCoreApp()
advisor = FinancialAdvisorOrchestrator()

@app.entrypoint
def invoke(payload):
    user_query = payload.get("prompt", "")
    response = advisor.analyze(user_query)
    return {"result": response}
```

### Interface Differences

#### Input Format

**Original System:**
- Direct string input to methods
- Multiple method interfaces available
- Python function calls

```python
# Direct method calls
response = advisor.analyze("Analyze AAPL stock")
market_data = advisor.get_market_analysis("AAPL", lookback_days=7)
strategies = advisor.get_strategies("AAPL", "Moderate", "Medium-term")
```

**AgentCore System:**
- JSON payload with "prompt" field
- Single HTTP endpoint interface
- REST API calls

```json
{
  "prompt": "Analyze AAPL stock for moderate risk investor"
}
```

#### Output Format

**Original System:**
- Direct string responses
- Dictionary responses for complete analysis
- Python objects

```python
# String response
response = advisor.analyze(query)  # Returns: str

# Dictionary response
results = advisor.run_complete_analysis("AAPL")  # Returns: Dict[str, str]
```

**AgentCore System:**
- Structured JSON responses with metadata
- Consistent response format
- HTTP response objects

```json
{
  "result": "# Financial Analysis for AAPL...",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "system": "financial-advisor-multiagent",
  "metadata": {
    "version": "1.0.0",
    "agent_type": "financial_advisor",
    "educational_disclaimer": true,
    "capabilities": ["market_intelligence", "strategy_development", "execution_planning", "risk_assessment"]
  }
}
```

### Deployment Differences

#### Original System Deployment
- Local Python environment execution
- Direct import and instantiation
- Jupyter notebook integration
- Manual dependency management

```bash
# Original system usage
python -c "from financial_advisor_multiagent import initialize_system; advisor = initialize_system()"
```

#### AgentCore System Deployment
- AWS managed infrastructure
- HTTP server with automatic scaling
- Container-based deployment
- Managed dependency resolution

```bash
# AgentCore deployment
agentcore configure --entrypoint financial_advisor_agentcore.py
agentcore launch
```

### Functional Differences

#### Method Availability

**Original System Methods:**
```python
# All methods available directly
advisor.analyze(query)                    # Main orchestrator method
advisor.get_market_analysis(ticker)       # Direct market analysis
advisor.get_strategies(ticker, risk, horizon)  # Direct strategy generation
advisor.get_execution_plan(ticker, strategies)  # Direct execution planning
advisor.get_risk_assessment(...)          # Direct risk assessment
advisor.run_complete_analysis(...)        # Complete workflow
```

**AgentCore System Methods:**
```python
# Single entry point method
invoke(payload)  # Only method available via HTTP
```

The AgentCore version only exposes the main `analyze()` method through the HTTP interface. Direct access to individual specialist methods (`get_market_analysis`, `get_strategies`, etc.) is not available via the HTTP API.

#### Error Handling Differences

**Original System:**
- Python exceptions raised directly
- Error messages as return values from tools
- Console logging and print statements

```python
# Original error handling
try:
    response = advisor.analyze(query)
except Exception as e:
    print(f"Error: {e}")
```

**AgentCore System:**
- Structured error responses (no exceptions raised)
- HTTP status codes and error metadata
- AgentCore logging integration

```json
{
  "error": "Invalid request format: Please provide a financial advisory request...",
  "error_type": "validation_error",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "metadata": {
    "error_category": "payload_validation",
    "recoverable": true,
    "suggestion": "Please check your request format and try again"
  }
}
```

### Payload Format Requirements

#### Original System Input Flexibility
The original system accepts various input formats and provides multiple interaction patterns:

```python
# Flexible input formats
advisor.analyze("AAPL analysis")
advisor.analyze("Analyze Apple stock for conservative investor with long-term horizon")
advisor.run_complete_analysis("AAPL", "Aggressive", "Short-term")
```

#### AgentCore System Payload Requirements
The AgentCore system requires specific JSON payload structure:

**Required Format:**
```json
{
  "prompt": "Your financial advisory request here"
}
```

**Validation Rules:**
- Payload must be a valid JSON object
- Must contain "prompt" field
- "prompt" field must be a non-empty string
- Additional fields are ignored but preserved in metadata

**Invalid Payloads:**
```json
// Missing prompt field
{"query": "Analyze AAPL"}  // ❌ Invalid

// Empty prompt
{"prompt": ""}  // ❌ Invalid

// Wrong data type
{"prompt": 123}  // ❌ Invalid

// Not an object
"Analyze AAPL"  // ❌ Invalid
```

### Behavioral Changes

#### Session Management
**Original System:**
- Stateless individual method calls
- No session persistence
- Manual state management

**AgentCore System:**
- HTTP request/response cycle
- No session state maintained between requests
- Each request is independent

#### Logging and Monitoring
**Original System:**
- Python logging to console
- Manual error tracking
- Local debugging capabilities

**AgentCore System:**
- AgentCore integrated logging (`app.logger`)
- CloudWatch integration when deployed
- Structured error reporting with metadata
- Request/response tracking

#### Performance Characteristics
**Original System:**
- Direct Python execution
- No HTTP overhead
- Local resource usage

**AgentCore System:**
- HTTP request/response overhead
- Network latency considerations
- AWS managed scaling and resource allocation
- Container startup time

### Limitations in AgentCore Version

#### Reduced API Surface
The AgentCore version only exposes the main orchestrator functionality. Direct access to individual specialist agents is not available:

**Not Available in AgentCore:**
- `get_market_analysis()` - Direct market analysis
- `get_strategies()` - Direct strategy generation  
- `get_execution_plan()` - Direct execution planning
- `get_risk_assessment()` - Direct risk assessment
- `run_complete_analysis()` - Structured workflow with dictionary output

**Available in AgentCore:**
- `analyze()` - Main orchestrator method (via HTTP payload)

#### Response Format Constraints
The AgentCore version always returns structured JSON responses, while the original system can return various Python data types.

#### Deployment Dependencies
The AgentCore version requires:
- AWS account and credentials
- AgentCore CLI installation
- Network connectivity for deployment
- Container runtime environment

### Preserved Functionality

#### Core Agent Logic
All core financial advisory logic is preserved:
- Same specialist agents (Market Intelligence, Strategy Architect, Execution Planner, Risk Assessor)
- Same agent tools and coordination patterns
- Same token management (2000-token conservative limits)
- Same error handling mechanisms within agents
- Same educational disclaimers and responsible AI practices

#### Web Search Integration
- DuckDuckGo search functionality maintained
- Same rate limit handling and error recovery
- Same search result processing

#### Model Compatibility
- Same model provider support (Amazon Bedrock Claude 3.5 Sonnet)
- Same multi-parameter format attempts for model compatibility
- Same fallback mechanisms for agent invocation

### Migration Considerations

#### From Original to AgentCore
When migrating from the original system to AgentCore:

1. **Change Interface**: Replace direct method calls with HTTP requests
2. **Update Input Format**: Convert string inputs to JSON payloads with "prompt" field
3. **Handle Response Format**: Parse JSON responses instead of direct string returns
4. **Update Error Handling**: Handle structured error responses instead of exceptions
5. **Consider Deployment**: Set up AWS credentials and AgentCore CLI

#### Example Migration
**Original Code:**
```python
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

advisor = FinancialAdvisorOrchestrator()
try:
    response = advisor.analyze("Analyze AAPL for moderate risk investor")
    print(response)
except Exception as e:
    print(f"Error: {e}")
```

**AgentCore Equivalent:**
```python
import requests

response = requests.post(
    "http://localhost:8080/invocations",
    json={"prompt": "Analyze AAPL for moderate risk investor"}
)

if response.status_code == 200:
    result = response.json()
    if "result" in result:
        print(result["result"])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
else:
    print(f"HTTP Error: {response.status_code}")
```

---

**Educational Use Only**: This financial advisor system is designed for learning about AI agent architectures and financial analysis concepts. It is not intended for actual investment decisions.