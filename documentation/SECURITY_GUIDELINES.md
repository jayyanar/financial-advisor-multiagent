# Security Guidelines for AgentCore Deployment

## Overview

This document outlines security considerations and best practices for deploying the Financial Advisor Multiagent System to Amazon Bedrock AgentCore Runtime.

## Security Risk Assessment

### HIGH PRIORITY

#### 1. AWS Credential Management
**Risk**: Exposure of AWS credentials could lead to unauthorized access to Bedrock models and AgentCore resources.

**Mitigation Strategies**:
```python
# ❌ NEVER do this - hardcoded credentials
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"  # Example only - never use real keys
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # Example only

# ✅ Use IAM roles and environment variables
import boto3
from botocore.exceptions import NoCredentialsError

try:
    # Use default credential chain (IAM roles, environment variables, etc.)
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise NoCredentialsError("No AWS credentials found")
except NoCredentialsError:
    logger.error("AWS credentials not configured properly")
```

**Best Practices**:
- Use IAM roles for AgentCore deployment
- Never commit credentials to version control
- Rotate access keys regularly (if using keys)
- Use AWS credential chains in order of preference:
  1. IAM roles (recommended for AgentCore)
  2. Environment variables
  3. AWS credential files
  4. Instance metadata (for EC2)

#### 2. Input Validation and Sanitization
**Risk**: Malicious input could cause system errors, resource exhaustion, or injection attacks.

**Mitigation Implementation**:
```python
import re
from typing import Optional

def sanitize_user_input(user_query: str) -> str:
    """
    Sanitize user input to prevent injection attacks and resource exhaustion.
    
    Args:
        user_query: Raw user input string
        
    Returns:
        str: Sanitized input string
        
    Raises:
        ValueError: If input is invalid or potentially malicious
    """
    # Length validation
    if len(user_query) > 5000:
        raise ValueError("Query too long (max 5000 characters)")
    
    # Remove potentially dangerous characters
    # Allow alphanumeric, spaces, and common punctuation
    sanitized = re.sub(r'[^\w\s\-.,!?()$%]', '', user_query)
    
    # Validate ticker symbols (if present)
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    tickers = re.findall(ticker_pattern, sanitized)
    
    # Validate against known ticker format
    for ticker in tickers:
        if not re.match(r'^[A-Z]{1,5}$', ticker):
            logger.warning(f"Potentially invalid ticker symbol: {ticker}")
    
    return sanitized.strip()

def validate_payload_structure(payload: dict) -> bool:
    """
    Validate AgentCore payload structure.
    
    Args:
        payload: Request payload dictionary
        
    Returns:
        bool: True if payload is valid
        
    Raises:
        ValueError: If payload structure is invalid
    """
    required_fields = ['prompt']
    
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")
    
    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(payload['prompt'], str):
        raise ValueError("Prompt field must be a string")
    
    return True
```

### MEDIUM PRIORITY

#### 3. External API Security
**Risk**: DuckDuckGo API dependency could be compromised or rate-limited.

**Mitigation Strategies**:
```python
import time
from functools import wraps
from typing import Optional

class APISecurityManager:
    """Manage external API security and rate limiting."""
    
    def __init__(self):
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        self.max_retries = 3
        
    def rate_limit_decorator(self, func):
        """Decorator to implement rate limiting."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
            return func(*args, **kwargs)
        return wrapper
    
    def secure_web_search(self, keywords: str, region: str = "us-en", 
                         max_results: Optional[int] = None) -> str:
        """
        Secure wrapper for web search with enhanced error handling.
        
        Args:
            keywords: Search query (pre-sanitized)
            region: Search region
            max_results: Maximum results to return
            
        Returns:
            str: Search results or error message
        """
        # Sanitize search keywords
        sanitized_keywords = re.sub(r'[^\w\s\-.]', '', keywords)
        
        if not sanitized_keywords.strip():
            return "Invalid search query after sanitization"
        
        # Implement retry logic with exponential backoff
        for attempt in range(self.max_retries):
            try:
                results = DDGS().text(
                    sanitized_keywords, 
                    region=region, 
                    max_results=max_results
                )
                return results if results else "No results found."
                
            except RatelimitException:
                if attempt < self.max_retries - 1:
                    wait_time = (2 ** attempt) * 1.0  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                return "Search temporarily unavailable due to rate limiting"
                
            except Exception as e:
                logger.error(f"Search API error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1.0)
                    continue
                return "Search service temporarily unavailable"
        
        return "Search service unavailable after multiple attempts"
```

#### 4. Error Information Disclosure
**Risk**: Detailed error messages could expose internal system information.

**Secure Error Handling**:
```python
import traceback
from enum import Enum

class ErrorLevel(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecureErrorHandler:
    """Handle errors securely without information disclosure."""
    
    def __init__(self, logger):
        self.logger = logger
        
    def sanitize_error_message(self, error: Exception, 
                             error_level: ErrorLevel = ErrorLevel.MEDIUM) -> str:
        """
        Create user-safe error message while logging details internally.
        
        Args:
            error: The original exception
            error_level: Severity level of the error
            
        Returns:
            str: Sanitized error message for user
        """
        # Log full error details internally
        self.logger.error(
            f"Error occurred: {type(error).__name__}: {str(error)}",
            exc_info=True
        )
        
        # Return sanitized message based on error type
        if isinstance(error, ValueError):
            return "Invalid input provided. Please check your request format."
        elif isinstance(error, ConnectionError):
            return "Service temporarily unavailable. Please try again later."
        elif isinstance(error, TimeoutError):
            return "Request timed out. Please try again with a simpler query."
        else:
            return "An unexpected error occurred. Please try again later."
    
    def create_error_response(self, error: Exception, 
                            request_id: Optional[str] = None) -> dict:
        """
        Create structured error response for AgentCore.
        
        Args:
            error: The original exception
            request_id: Optional request identifier for tracking
            
        Returns:
            dict: Structured error response
        """
        sanitized_message = self.sanitize_error_message(error)
        
        response = {
            "error": sanitized_message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent"
        }
        
        if request_id:
            response["request_id"] = request_id
            
        return response
```

### LOW PRIORITY

#### 5. Token Usage Monitoring
**Risk**: Excessive token usage could indicate abuse or system compromise.

**Rate Limiting Recommendations**:
- Implement per-user request limits (e.g., 10 requests per minute)
- Monitor token consumption patterns for anomalies
- Set up alerts for unusual usage spikes
- Consider implementing exponential backoff for repeated requests

**Monitoring Implementation**:
```python
class TokenUsageMonitor:
    """Monitor and alert on unusual token usage patterns."""
    
    def __init__(self):
        self.usage_history = []
        self.alert_threshold = 10000  # tokens per hour
        
    def log_token_usage(self, tokens_used: int, user_id: Optional[str] = None):
        """Log token usage for monitoring."""
        usage_record = {
            "timestamp": datetime.now(timezone.utc),
            "tokens": tokens_used,
            "user_id": user_id
        }
        
        self.usage_history.append(usage_record)
        
        # Clean old records (keep last 24 hours)
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        self.usage_history = [
            record for record in self.usage_history 
            if record["timestamp"] > cutoff_time
        ]
        
        # Check for unusual usage patterns
        self._check_usage_alerts()
    
    def _check_usage_alerts(self):
        """Check for unusual usage patterns and alert if necessary."""
        # Calculate usage in last hour
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        recent_usage = sum(
            record["tokens"] for record in self.usage_history
            if record["timestamp"] > one_hour_ago
        )
        
        if recent_usage > self.alert_threshold:
            logger.warning(
                f"High token usage detected: {recent_usage} tokens in last hour"
            )
```

## Security Configuration Checklist

### Pre-Deployment Security Checks

- [ ] **Credential Security**
  - [ ] No hardcoded AWS credentials in source code
  - [ ] IAM roles configured with minimal required permissions
  - [ ] Environment variables properly secured
  - [ ] AWS credential rotation schedule established

- [ ] **Input Validation**
  - [ ] User input sanitization implemented
  - [ ] Payload structure validation in place
  - [ ] Request size limits configured
  - [ ] Ticker symbol validation implemented

- [ ] **External API Security**
  - [ ] Rate limiting implemented for web search
  - [ ] Retry logic with exponential backoff
  - [ ] API timeout handling configured
  - [ ] Error handling for API failures

- [ ] **Error Handling**
  - [ ] Sanitized error messages for users
  - [ ] Detailed error logging for developers
  - [ ] Structured error response format
  - [ ] No stack trace exposure to users

- [ ] **Monitoring and Logging**
  - [ ] Token usage monitoring implemented
  - [ ] Security event logging configured
  - [ ] Alert thresholds established
  - [ ] Log retention policies defined

### Post-Deployment Security Monitoring

- [ ] **Regular Security Reviews**
  - [ ] Monthly credential rotation (if using keys)
  - [ ] Quarterly security assessment
  - [ ] Annual penetration testing
  - [ ] Continuous vulnerability scanning

- [ ] **Monitoring Alerts**
  - [ ] Unusual token usage patterns
  - [ ] High error rates
  - [ ] Failed authentication attempts
  - [ ] Suspicious query patterns

- [ ] **Incident Response**
  - [ ] Security incident response plan
  - [ ] Contact information for security team
  - [ ] Escalation procedures defined
  - [ ] Recovery procedures documented

## Compliance Considerations

### Data Protection
- **No PII Storage**: System does not store personally identifiable information
- **Educational Disclaimers**: All outputs include educational disclaimers
- **Session Isolation**: AgentCore provides session isolation between users
- **Data Retention**: No persistent storage of user queries or responses

### Financial Regulations
- **Educational Purpose**: System explicitly states educational purpose only
- **No Financial Advice**: Clear disclaimers that output is not financial advice
- **Risk Warnings**: All strategies include appropriate risk warnings
- **Compliance Monitoring**: Regular review of output for compliance

### AWS Security Standards
- **IAM Best Practices**: Follow AWS IAM security best practices
- **Network Security**: Use VPC and security groups appropriately
- **Encryption**: Enable encryption in transit and at rest
- **Audit Logging**: Enable AWS CloudTrail for audit logging

## Emergency Procedures

### Security Incident Response

1. **Immediate Actions**
   - Disable compromised credentials immediately
   - Stop AgentCore deployment if necessary
   - Document incident details and timeline

2. **Investigation**
   - Review CloudTrail logs for unauthorized access
   - Check application logs for suspicious activity
   - Analyze token usage patterns for anomalies

3. **Recovery**
   - Rotate all credentials and API keys
   - Update security configurations as needed
   - Redeploy with enhanced security measures

4. **Post-Incident**
   - Conduct post-mortem analysis
   - Update security procedures based on lessons learned
   - Implement additional monitoring if needed

### Contact Information

- **AWS Support**: Use AWS Support for AgentCore security issues
- **Security Team**: [Your security team contact information]
- **Emergency Escalation**: [Emergency contact procedures]

## Security Testing

### Automated Security Testing
```bash
# Run security linting
bandit -r financial_advisor_agentcore.py

# Check for hardcoded secrets
truffleHog --regex --entropy=False .

# Dependency vulnerability scanning
safety check -r requirements-agentcore.txt
```

### Manual Security Testing
- Input validation testing with malicious payloads
- Error handling testing with invalid inputs
- Rate limiting testing with rapid requests
- Authentication testing with invalid credentials

This security framework ensures the AgentCore deployment maintains high security standards while preserving all functional capabilities of the financial advisor system.