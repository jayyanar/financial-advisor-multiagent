# AgentCore Comprehensive Testing Guide

This document provides complete guidance for testing the AgentCore financial advisor system, covering all testing workflows implemented for task 8 of the AgentCore deployment specification.

## Overview

The comprehensive testing suite validates three critical aspects of the AgentCore system:

1. **Integration Workflow Testing** - Complete analysis workflow validation
2. **Query Format Testing** - Various input format handling
3. **Error Handling Testing** - Error scenarios and graceful degradation

## Requirements Coverage

The testing suite covers the following requirements:

- **Requirements 1.1, 1.2, 1.3**: Core financial advisory functionality and educational disclaimers
- **Requirements 3.2, 3.3, 3.4**: Specialist agent coordination and workflow
- **Requirements 7.1, 7.2, 7.3, 7.4**: Query format handling and parameter extraction
- **Requirements 8.1, 8.2, 8.3, 8.5**: Error handling and graceful degradation

## Test Suite Components

### 1. Integration Workflow Test (`test_agentcore_integration_workflow.py`)

**Purpose**: Validates the complete financial analysis workflow through AgentCore.

**What it tests**:
- Market intelligence → strategy → execution → risk assessment flow
- All specialist agents work correctly through AgentCore wrapper
- Educational disclaimers appear in all outputs
- Response structure and metadata compliance

**Key validations**:
- ✅ Market Intelligence component present
- ✅ Strategy Development component present  
- ✅ Execution Planning component present
- ✅ Risk Assessment component present
- ✅ Educational disclaimers included
- ✅ Specialist agents functioning correctly
- ✅ Response time within acceptable limits

### 2. Query Format Test (`test_agentcore_query_formats.py`)

**Purpose**: Validates handling of various input query formats and parameter extraction.

**What it tests**:
- Simple ticker-only queries
- Complete queries with risk tolerance and horizon
- Queries missing required information
- Parameter extraction accuracy
- Missing parameter handling appropriateness

**Test categories**:
- **Simple Ticker Only**: `"AAPL"`, `"Analyze TSLA"`
- **Complete Queries**: `"Analyze AAPL for moderate risk, long-term horizon"`
- **Missing Parameters**: Queries missing ticker, risk tolerance, or horizon
- **Edge Cases**: Empty queries, multiple tickers, extreme parameters

### 3. Error Handling Test (`test_agentcore_error_handling.py`)

**Purpose**: Validates comprehensive error handling and graceful degradation.

**What it tests**:
- Invalid payload formats
- Web search API failures and rate limiting
- Agent invocation errors
- Network and timeout scenarios
- Structured error responses

**Error scenarios**:
- **Invalid Payloads**: Empty JSON, missing prompt, wrong data types
- **Malformed Requests**: Invalid JSON, wrong content types, oversized payloads
- **Network Issues**: Timeouts, connection interruptions
- **Agent Errors**: Rate limits, search failures, parameter errors

## Running Tests

### Quick Start

```bash
# Run all tests (recommended)
python test_runner.py --all

# Run individual test suites
python test_runner.py --integration
python test_runner.py --query-formats
python test_runner.py --error-handling

# List available tests
python test_runner.py --list
```

### Comprehensive Testing

```bash
# Run the complete test suite with detailed reporting
python run_comprehensive_agentcore_tests.py
```

This will:
1. Run all three test suites in sequence
2. Generate comprehensive analysis and reporting
3. Save detailed results to JSON and text files
4. Provide overall system validation status

### Individual Test Scripts

You can also run test scripts directly:

```bash
# Integration workflow test
python test_agentcore_integration_workflow.py

# Query format test
python test_agentcore_query_formats.py

# Error handling test
python test_agentcore_error_handling.py
```

## Test Results and Reporting

### Result Files

Each test suite generates detailed result files:

- `agentcore_integration_test_results.json` - Integration test detailed results
- `agentcore_query_format_test_results.json` - Query format test results
- `agentcore_error_handling_test_results.json` - Error handling test results
- `comprehensive_agentcore_test_results.json` - Combined results from all suites
- `comprehensive_agentcore_test_report.txt` - Human-readable comprehensive report

### Understanding Results

**Success Criteria**:
- Integration Test: Complete workflow validation with all components present
- Query Format Test: 80%+ success rate across all query categories
- Error Handling Test: 85%+ success rate for graceful error handling

**Key Metrics**:
- Response times (should be < 3 minutes for comprehensive analysis)
- Parameter extraction accuracy
- Error response structure and helpfulness
- Educational disclaimer presence
- Specialist agent activity validation

## Prerequisites

### System Requirements

1. **AgentCore Environment**: 
   ```bash
   pip install bedrock-agentcore-starter-toolkit
   ```

2. **Financial Advisor System**:
   ```bash
   pip install strands-agents strands-agents-tools
   pip install duckduckgo-search boto3
   ```

3. **Testing Dependencies**:
   ```bash
   pip install requests
   ```

### Files Required

Ensure these files are present in your testing directory:
- `financial_advisor_agentcore.py` - AgentCore wrapper implementation
- `financial_advisor_multiagent.py` - Original financial advisor system
- All test scripts (created by task 8 implementation)

## Test Execution Flow

### Automatic Server Management

All test scripts automatically:
1. Start the AgentCore server (`financial_advisor_agentcore.py`)
2. Wait for server readiness (health check on `/ping`)
3. Execute test scenarios
4. Gracefully stop the server
5. Generate and save results

### Test Sequence

When running comprehensive tests:

1. **Integration Workflow Test** (5-10 minutes)
   - Tests complete analysis with comprehensive query
   - Validates all specialist agents and workflow components
   - Checks educational disclaimers and response structure

2. **Query Format Test** (3-5 minutes)
   - Tests 15+ different query formats across 4 categories
   - Validates parameter extraction and missing parameter handling
   - Checks response appropriateness for each query type

3. **Error Handling Test** (2-4 minutes)
   - Tests 15+ error scenarios across 4 categories
   - Validates graceful error responses and structured error data
   - Checks system resilience and fallback mechanisms

## Troubleshooting

### Common Issues

**Server Startup Failures**:
```bash
# Check if port 8080 is available
lsof -i :8080

# Verify AgentCore installation
python -c "from bedrock_agentcore.runtime import BedrockAgentCoreApp; print('AgentCore OK')"

# Check financial advisor system
python -c "from financial_advisor_multiagent import FinancialAdvisorOrchestrator; print('Advisor OK')"
```

**Test Timeouts**:
- Integration tests may take 2-3 minutes for comprehensive analysis
- Increase timeout values in test scripts if needed
- Check network connectivity for web search functionality

**Import Errors**:
```bash
# Verify all dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Debug Mode

For detailed debugging, modify test scripts to include:
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Increase timeouts
timeout = 300  # 5 minutes

# Save intermediate responses
with open("debug_response.json", "w") as f:
    json.dump(response_data, f, indent=2)
```

## Validation Checklist

Before considering the AgentCore system ready for deployment, ensure:

### ✅ Integration Workflow
- [ ] Complete analysis workflow executes successfully
- [ ] All four specialist agents (market, strategy, execution, risk) are active
- [ ] Educational disclaimers present in all outputs
- [ ] Response structure matches AgentCore requirements
- [ ] Performance within acceptable limits (< 3 minutes)

### ✅ Query Format Handling
- [ ] Simple ticker queries handled appropriately
- [ ] Complete queries with all parameters work correctly
- [ ] Missing parameter scenarios provide helpful guidance
- [ ] Edge cases handled gracefully
- [ ] Parameter extraction accuracy > 80%

### ✅ Error Handling
- [ ] Invalid payloads return structured error responses
- [ ] Web search failures handled gracefully
- [ ] Agent errors trigger appropriate fallback mechanisms
- [ ] Network issues handled without system crashes
- [ ] Error responses include helpful guidance and metadata

### ✅ Overall System Health
- [ ] No system crashes during any test scenario
- [ ] All error responses are structured and helpful
- [ ] Educational disclaimers maintained throughout
- [ ] Performance metrics within acceptable ranges
- [ ] All requirements coverage validated

## Success Criteria Summary

**Overall Success**: All three test suites must pass with:
- Integration Test: Complete workflow validation
- Query Format Test: ≥80% success rate
- Error Handling Test: ≥85% success rate

**Deployment Readiness**: System is ready for AgentCore deployment when:
- All tests pass consistently
- No critical failures in error handling
- Educational disclaimers present in all scenarios
- Performance metrics within acceptable ranges
- All specialist agents functioning correctly through AgentCore wrapper

## Next Steps

After successful testing:

1. **Review Results**: Examine detailed test reports for any warnings or recommendations
2. **Performance Optimization**: Address any performance issues identified
3. **Deploy to AgentCore**: Use `agentcore configure` and `agentcore launch`
4. **Production Testing**: Run `agentcore invoke` tests with sample queries
5. **Monitoring Setup**: Enable CloudWatch observability for production monitoring

---

**Note**: This testing suite provides comprehensive validation of the AgentCore financial advisor system. All tests are designed to run automatically and provide detailed feedback on system readiness for production deployment.