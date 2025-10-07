# Implementation Plan

- [x] 1. Set up AgentCore development environment
  - Install bedrock-agentcore-starter-toolkit in existing virtual environment
  - Verify compatibility with existing strands-agents dependencies
  - Create project structure for AgentCore deployment
  - _Requirements: 1.4, 2.2_

- [x] 2. Create AgentCore wrapper entry point
  - [x] 2.1 Create financial_advisor_agentcore.py with BedrockAgentCoreApp setup
    - Import BedrockAgentCoreApp and existing FinancialAdvisorOrchestrator
    - Initialize app instance and orchestrator instance
    - _Requirements: 2.1, 2.2, 3.1_

  - [x] 2.2 Implement @app.entrypoint decorated function
    - Create invoke function that accepts AgentCore payload format
    - Extract prompt from payload with validation
    - Call existing orchestrator.analyze() method
    - Return structured response with "result" field
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

  - [x] 2.3 Add app.run() execution control
    - Implement if __name__ == "__main__" block with app.run()
    - Ensure AgentCore runtime controls agent execution
    - _Requirements: 2.3_

- [x] 3. Implement payload processing functions
  - [x] 3.1 Create process_agentcore_payload function
    - Extract and validate prompt field from payload
    - Handle missing or empty prompt with helpful error message
    - Return processed user query string
    - _Requirements: 7.1, 7.2, 8.4_

  - [x] 3.2 Create format_agentcore_response function
    - Accept advisor response string as input
    - Return structured dict with "result", "timestamp", and "system" fields
    - Include metadata field for extensibility
    - _Requirements: 2.5, 7.5_

- [x] 4. Add comprehensive error handling
  - [x] 4.1 Implement try-catch wrapper in entry point function
    - Catch ValueError for invalid payload formats
    - Catch general exceptions for system errors
    - Return structured error responses instead of raising exceptions
    - Added input length validation (5000 character limit)
    - _Requirements: 8.1, 8.2, 8.5_

  - [x] 4.2 Add logging integration with AgentCore
    - Use app.logger for error logging
    - Log detailed error information for debugging
    - Maintain existing agent error handling mechanisms
    - Added security event logging for monitoring
    - _Requirements: 8.1, 8.3_

- [x] 5. Create requirements.txt for AgentCore deployment
  - [x] 5.1 Add bedrock-agentcore-starter-toolkit dependency
    - Include bedrock-agentcore-starter-toolkit>=1.0.0
    - Add bedrock-agentcore runtime dependency
    - _Requirements: 1.4, 2.1_

  - [x] 5.2 Include all existing system dependencies
    - Add strands-agents>=1.10.0 and strands-agents-tools>=0.2.9
    - Include duckduckgo-search>=6.3.4 for web search functionality
    - Add boto3>=1.40.0 and other supporting dependencies
    - _Requirements: 1.4, 4.3, 4.4_

- [x] 6. Implement local testing capabilities
  - [x] 6.1 Create test script for local AgentCore server
    - Script to start financial_advisor_agentcore.py locally
    - Verify server starts on localhost:8080
    - _Requirements: 5.1, 5.2_

  - [x] 6.2 Create HTTP test requests for validation
    - Test POST /invocations endpoint with sample financial queries
    - Test GET /ping endpoint for health checks
    - Validate response formats match AgentCore expectations
    - _Requirements: 5.2, 5.3, 5.4_

  - [ ]* 6.3 Write unit tests for payload processing functions
    - Test process_agentcore_payload with various input formats
    - Test format_agentcore_response with different advisor outputs
    - Test error handling scenarios
    - _Requirements: 5.3, 5.4_

- [x] 7. Create deployment configuration
  - [x] 7.1 Set up AgentCore CLI configuration
    - Create configuration for agentcore configure command
    - Specify financial_advisor_agentcore.py as entry point
    - _Requirements: 6.1, 6.2_

  - [x] 7.2 Create deployment script
    - Script to run agentcore configure and agentcore launch
    - Include error handling for deployment failures
    - _Requirements: 6.2, 6.3_

- [x] 8. Implement comprehensive testing workflow
  - [x] 8.1 Create integration test for complete analysis workflow
    - Test market intelligence → strategy → execution → risk assessment flow
    - Verify all specialist agents work correctly through AgentCore
    - Confirm educational disclaimers appear in all outputs
    - _Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4_

  - [x] 8.2 Test various input query formats
    - Test simple ticker-only queries
    - Test complete queries with risk tolerance and horizon
    - Test queries missing required information
    - Verify parameter extraction and missing parameter handling
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 8.3 Validate error handling scenarios
    - Test invalid payload formats
    - Test web search API failures and rate limiting
    - Test agent invocation errors
    - Verify graceful error responses
    - _Requirements: 8.1, 8.2, 8.3, 8.5_

- [x] 9. Create deployment documentation
  - [x] 9.1 Write README.md for AgentCore deployment
    - Document installation and setup process
    - Include local testing instructions
    - Provide deployment commands and examples
    - _Requirements: 5.1, 6.1, 6.2, 6.3_

  - [x] 9.2 Document differences from original system
    - Explain AgentCore wrapper functionality
    - Document payload format requirements
    - Note any behavioral changes or limitations
    - _Requirements: 1.1, 2.4, 2.5_

- [-] 10. Validate production readiness
  - [x] 10.1 Test deployed agent with agentcore invoke
    - Deploy to AWS using agentcore launch
    - Test with various financial advisory queries
    - Verify responses match local testing results
    - _Requirements: 6.3, 6.4, 6.5_

  - [x] 10.2 Verify all original functionality preserved
    - Compare outputs with original financial_advisor_multiagent.py
    - Confirm all specialist agents work correctly
    - Validate token limits and error handling maintained
    - Ensure educational disclaimers present in all responses
    - _Requirements: 1.1, 1.2, 1.3, 3.1, 3.2, 3.3, 3.4, 3.5_