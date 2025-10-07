# AgentCore Local Testing Guide

This directory contains comprehensive testing scripts for the AgentCore financial advisor deployment. These scripts help verify that the system works correctly before deploying to AWS.

## Test Scripts Overview

### 1. `test_local_agentcore_server.py`
Tests server startup and basic connectivity.

**Features:**
- Starts the financial_advisor_agentcore.py server locally
- Verifies server starts on localhost:8080
- Tests basic connectivity and health endpoint
- Supports interactive mode for manual testing

**Usage:**
```bash
# Run automated startup test
python test_local_agentcore_server.py

# Run with custom timeout
python test_local_agentcore_server.py --timeout 60

# Run in interactive mode (keeps server running)
python test_local_agentcore_server.py --interactive
```

### 2. `test_agentcore_http_requests.py`
Tests HTTP endpoints with sample financial queries.

**Features:**
- Tests POST /invocations endpoint with financial queries
- Tests GET /ping endpoint for health checks
- Validates response formats match AgentCore expectations
- Tests error handling scenarios
- Comprehensive response validation

**Usage:**
```bash
# Run comprehensive HTTP tests (assumes server is running)
python test_agentcore_http_requests.py

# Run quick tests only
python test_agentcore_http_requests.py --quick

# Test against different server
python test_agentcore_http_requests.py --server http://localhost:8080
```

### 3. `test_agentcore_complete.py`
Complete test suite combining server startup and HTTP testing.

**Features:**
- Automatically starts server and runs HTTP tests
- Comprehensive test workflow
- Automatic cleanup
- Multiple test modes

**Usage:**
```bash
# Run complete test suite
python test_agentcore_complete.py

# Run quick tests only
python test_agentcore_complete.py --quick

# Run server tests only
python test_agentcore_complete.py --server-only

# Run HTTP tests only (assumes server running)
python test_agentcore_complete.py --http-only
```

## Test Requirements

### Prerequisites
- Python 3.10+ with virtual environment activated
- All dependencies installed (see requirements.txt)
- financial_advisor_agentcore.py in the current directory
- financial_advisor_multiagent.py available for import

### Required Python Packages
```bash
pip install requests
pip install bedrock-agentcore-starter-toolkit
pip install strands-agents strands-agents-tools
pip install duckduckgo-search boto3
```

## Test Scenarios

### Server Startup Tests
- ✅ Server process starts successfully
- ✅ Server listens on localhost:8080
- ✅ Health endpoint responds with 200 status
- ✅ Basic connectivity verification

### HTTP Request Tests
- ✅ POST /invocations with valid financial queries
- ✅ GET /ping health check endpoint
- ✅ Response format validation (AgentCore compatibility)
- ✅ Error handling for invalid payloads
- ✅ Educational disclaimer presence
- ✅ Response timing and performance

### Sample Test Queries
The HTTP tests include these sample financial queries:
- "Analyze AAPL stock for moderate risk investor"
- "Provide financial analysis for TSLA with aggressive risk tolerance and long-term investment horizon"
- "Analyze MSFT for conservative investor with short-term horizon"
- "Research GOOGL stock and provide investment recommendations"

## Expected Response Format

AgentCore responses should follow this structure:
```json
{
  "result": "Financial analysis response...",
  "timestamp": "2024-01-01T12:00:00Z",
  "system": "financial-advisor-multiagent",
  "metadata": {
    "version": "1.0.0",
    "agent_type": "financial_advisor",
    "educational_disclaimer": true,
    "capabilities": ["market_intelligence", "strategy_development", "execution_planning", "risk_assessment"]
  }
}
```

Error responses should include:
```json
{
  "error": "Error description",
  "error_type": "validation_error",
  "timestamp": "2024-01-01T12:00:00Z",
  "system": "financial-advisor-multiagent",
  "metadata": {
    "error_category": "payload_validation",
    "recoverable": true,
    "suggestion": "Please check your request format"
  }
}
```

## Troubleshooting

### Common Issues

**Server won't start:**
- Check that financial_advisor_agentcore.py exists
- Verify all dependencies are installed
- Check that port 8080 is available
- Review error messages in console output

**HTTP tests fail:**
- Ensure server is running on localhost:8080
- Check network connectivity
- Verify request/response formats
- Review timeout settings

**Import errors:**
- Activate virtual environment
- Install missing dependencies
- Check Python path and module availability

### Debug Mode
For detailed debugging, check the server logs when running:
```bash
python financial_advisor_agentcore.py
```

The server provides detailed logging for:
- Request processing
- Agent invocations
- Error handling
- Response formatting

## Integration with AgentCore CLI

After local testing passes, you can deploy using AgentCore CLI:

```bash
# Configure deployment
agentcore configure --entrypoint financial_advisor_agentcore.py

# Deploy to AWS
agentcore launch

# Test deployed agent
agentcore invoke '{"prompt": "Analyze AAPL stock for moderate risk investor"}'
```

## Test Results Interpretation

### Success Indicators
- ✅ All tests pass with green checkmarks
- ✅ Server starts within timeout period
- ✅ Health endpoint returns 200 status
- ✅ Financial queries return valid responses
- ✅ Educational disclaimers present in responses
- ✅ Response formats match AgentCore expectations

### Failure Indicators
- ❌ Server startup timeout
- ❌ Connection refused errors
- ❌ Invalid response formats
- ❌ Missing educational disclaimers
- ❌ Agent invocation errors
- ❌ Web search failures

## Next Steps

Once local testing passes:
1. Review test results and fix any issues
2. Commit changes to version control
3. Configure AgentCore deployment
4. Deploy to AWS using AgentCore CLI
5. Test deployed agent with agentcore invoke
6. Monitor production performance

## Support

For issues with:
- **Server startup**: Check dependencies and port availability
- **HTTP requests**: Verify server is running and accessible
- **Agent responses**: Check financial_advisor_multiagent.py functionality
- **AgentCore deployment**: Refer to AgentCore documentation

Remember: This system is for educational purposes only and does not provide licensed financial advice.