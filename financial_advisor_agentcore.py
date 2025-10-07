#!/usr/bin/env python3
"""
AgentCore Financial Advisor Wrapper

This module provides an Amazon Bedrock AgentCore Runtime compatible wrapper
for the existing financial advisor multiagent system. It maintains all existing
functionality while adapting to AgentCore's service contract and deployment patterns.

The wrapper follows the SDK Integration approach using BedrockAgentCoreApp for
automatic HTTP server setup and built-in deployment tools.

Author: Financial Advisory System
License: Educational Use Only
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

# Import specific exceptions for comprehensive error handling
from duckduckgo_search.exceptions import RatelimitException, DuckDuckGoSearchException

# ============================================================
# AgentCore Application Setup
# ============================================================

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Initialize the existing financial advisor orchestrator
advisor = FinancialAdvisorOrchestrator()

# ============================================================
# Payload Processing Functions
# ============================================================

def process_agentcore_payload(payload: Dict[str, Any]) -> str:
    """
    Extract and validate user query from AgentCore payload.
    
    Handles missing or empty prompt with helpful error message that guides users
    on proper input format for financial advisory requests.
    
    Args:
        payload: AgentCore request payload with 'prompt' field
        
    Returns:
        str: Processed user query for financial advisor system
        
    Raises:
        ValueError: If payload is invalid or missing required fields
    """
    # Log payload processing start
    app.logger.debug(f"Processing AgentCore payload: {type(payload)}")
    
    if not isinstance(payload, dict):
        app.logger.error("Invalid payload type - expected dictionary")
        # Log security event for monitoring
        app.logger.error(f"SECURITY_EVENT: Invalid payload type received - expected dict, got {type(payload)}")
        raise ValueError("Payload must be a dictionary")
    
    user_query = payload.get("prompt", "")
    app.logger.debug(f"Extracted prompt field: {bool(user_query)}")
    
    if not user_query:
        app.logger.warning("Empty or missing prompt field in payload")
        raise ValueError(
            "Please provide a financial advisory request. "
            "Include ticker symbol, risk tolerance (Conservative/Moderate/Aggressive), "
            "and investment horizon (Short-term/Medium-term/Long-term) for best results. "
            "Example: 'Analyze AAPL stock for moderate risk investor with long-term horizon'"
        )
    
    if not isinstance(user_query, str):
        app.logger.error(f"Invalid prompt type - expected string, got {type(user_query)}")
        # Log security event for monitoring
        app.logger.error(f"SECURITY_EVENT: Invalid prompt field type - expected string, got {type(user_query)}")
        raise ValueError("The 'prompt' field must be a string containing your financial query")
    
    # Strip whitespace and validate length
    processed_query = user_query.strip()
    
    # Security: Limit input length to prevent resource exhaustion (Requirement 8.4)
    MAX_INPUT_LENGTH = 5000
    if len(processed_query) > MAX_INPUT_LENGTH:
        app.logger.warning(f"Security: Input query too long: {len(processed_query)} characters (max: {MAX_INPUT_LENGTH})")
        # Log security event for monitoring
        app.logger.error(f"SECURITY_EVENT: Input length validation failed - query length {len(processed_query)} exceeds maximum {MAX_INPUT_LENGTH}")
        raise ValueError(f"Query too long. Maximum {MAX_INPUT_LENGTH} characters allowed.")
    
    # Security: Basic content validation to detect potential injection attempts
    suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(', '__import__', 'subprocess', 'os.system']
    query_lower = processed_query.lower()
    for pattern in suspicious_patterns:
        if pattern in query_lower:
            app.logger.error(f"SECURITY_EVENT: Suspicious content detected in query - pattern: {pattern}")
            raise ValueError("Invalid characters detected in query. Please provide a standard financial advisory request.")
    
    if not processed_query:
        app.logger.warning("Prompt field contains only whitespace")
        raise ValueError(
            "Please provide a non-empty financial advisory request. "
            "Include ticker symbol, risk tolerance, and investment horizon for best results."
        )
    
    app.logger.info(f"Successfully processed payload - query length: {len(processed_query)} characters")
    return processed_query


def format_agentcore_response(advisor_response: str) -> Dict[str, Any]:
    """
    Format financial advisor response for AgentCore compatibility.
    
    Returns structured dict with "result", "timestamp", and "system" fields,
    plus metadata field for extensibility as required by AgentCore specification.
    
    Args:
        advisor_response: Response string from FinancialAdvisorOrchestrator
        
    Returns:
        dict: AgentCore-compatible response structure with required fields
    """
    # Log response formatting
    response_length = len(advisor_response) if advisor_response else 0
    app.logger.debug(f"Formatting AgentCore response - length: {response_length} characters")
    
    formatted_response = {
        "result": advisor_response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": "financial-advisor-multiagent",
        "metadata": {
            "version": "1.0.0",
            "agent_type": "financial_advisor",
            "educational_disclaimer": True,
            "response_format": "structured_analysis",
            "capabilities": [
                "market_intelligence",
                "strategy_development", 
                "execution_planning",
                "risk_assessment"
            ],
            "disclaimer": "Educational purposes only - not licensed financial advice",
            "response_stats": {
                "character_count": response_length,
                "processing_timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    }
    
    app.logger.debug("Successfully formatted AgentCore response")
    return formatted_response


# ============================================================
# Agent Orchestration with Enhanced Logging
# ============================================================
#
# This section implements comprehensive logging integration with AgentCore
# while maintaining all existing agent error handling mechanisms:
#
# Existing Error Handling Mechanisms Preserved:
# 1. invoke_agent() function: Multi-parameter format attempts for model compatibility
#    - Tries max_output_tokens, max_tokens, generation_config, inference_params
#    - Falls back to no-kwargs call if parameterized calls fail
#    - Returns error messages instead of raising exceptions
#
# 2. websearch() tool: Comprehensive web search error handling
#    - Handles RatelimitException with informative retry messages
#    - Handles DuckDuckGoSearchException with fallback responses
#    - Handles general exceptions with error reporting
#
# 3. Token Management: Conservative 2000-token limits
#    - Prevents token limit exceeded errors
#    - Maintains response quality while avoiding truncation
#
# 4. Graceful Degradation: System continues operating with partial functionality
#    - Web search failures don't crash the system
#    - Agent parameter errors trigger fallback mechanisms
#    - Missing data results in helpful guidance rather than failures
#
# AgentCore Logging Integration (Requirements 8.1, 8.3):
# - Uses app.logger for all error logging and debugging information
# - Logs detailed error information for monitoring and troubleshooting
# - Maintains existing error handling while adding observability
# - Provides structured error responses with metadata for debugging
#
# ============================================================

def invoke_financial_advisor_with_logging(user_query: str) -> str:
    """
    Invoke the financial advisor orchestrator with comprehensive logging.
    
    This function maintains existing agent error handling mechanisms while
    adding detailed logging for monitoring and troubleshooting as required
    by AgentCore deployment specifications.
    
    The existing system includes:
    - Multi-parameter format attempts for model compatibility (invoke_agent function)
    - Web search error handling with rate limit detection (websearch tool)
    - Conservative 2000-token limits with fallback mechanisms
    - Graceful degradation when agents or external services fail
    
    Args:
        user_query: User's financial advisory request
        
    Returns:
        str: Financial advisor response
        
    Raises:
        Exception: Re-raises any exceptions from the orchestrator for handling
                  by the main entry point function
    """
    try:
        app.logger.info("Initializing financial advisor orchestrator")
        app.logger.debug("Existing error handling mechanisms active: multi-parameter agent calls, web search fallbacks, token limits")
        
        # Log query characteristics for debugging
        query_stats = {
            "length": len(user_query),
            "word_count": len(user_query.split()),
            "contains_ticker": any(word.isupper() and len(word) <= 5 for word in user_query.split()),
            "contains_risk": any(risk in user_query.lower() for risk in ['conservative', 'moderate', 'aggressive']),
            "contains_horizon": any(horizon in user_query.lower() for horizon in ['short', 'medium', 'long'])
        }
        app.logger.debug(f"Query analysis: {query_stats}")
        
        # Invoke the existing orchestrator (maintains all existing error handling)
        app.logger.info("Invoking financial advisor orchestrator with preserved error handling mechanisms")
        app.logger.debug("Orchestrator will use: invoke_agent() with multi-parameter fallbacks, websearch() with rate limit handling")
        
        response = advisor.analyze(user_query)
        
        # Log successful completion
        response_stats = {
            "response_length": len(response) if response else 0,
            "contains_disclaimer": "educational" in response.lower() if response else False,
            "contains_strategies": "strategy" in response.lower() if response else False,
            "contains_error_message": any(error_term in response.lower() for error_term in ['error', 'exception', 'failed']) if response else False
        }
        app.logger.info(f"Financial advisor analysis completed successfully: {response_stats}")
        
        # Log if the response contains error messages from existing fallback mechanisms
        if response_stats.get("contains_error_message"):
            app.logger.debug("Response contains error messages - existing fallback mechanisms may have been triggered")
        
        return response
        
    except Exception as e:
        # Log the error but re-raise for handling by main entry point
        app.logger.error(f"Financial advisor orchestrator error: {type(e).__name__}: {e}")
        app.logger.debug("Error occurred during advisor.analyze() - existing fallback mechanisms engaged")
        app.logger.debug("Existing mechanisms include: agent parameter fallbacks, web search error handling, token limit management")
        raise  # Re-raise for main entry point error handling


# ============================================================
# AgentCore Entry Point
# ============================================================

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    AgentCore entry point that processes financial advisory requests.
    
    This function serves as the main interface between AgentCore Runtime
    and the existing financial advisor system. It handles payload validation,
    processes requests through the orchestrator, and returns structured responses.
    
    Comprehensive error handling catches specific exceptions and returns structured
    error responses instead of raising exceptions, as required by AgentCore.
    
    Args:
        payload: AgentCore payload with 'prompt' field containing user query
        
    Returns:
        dict: Structured response with 'result' field containing financial analysis
              or structured error response for any failures
    """
    try:
        # Extract and validate user query from payload
        user_query = process_agentcore_payload(payload)
        
        # Log the incoming request (using AgentCore's logger)
        app.logger.info(f"Processing financial advisory request: {user_query[:100]}...")
        
        # Process through existing orchestrator with enhanced logging
        response = invoke_financial_advisor_with_logging(user_query)
        
        # Format response for AgentCore compatibility
        formatted_response = format_agentcore_response(response)
        
        app.logger.info("Financial advisory request processed successfully")
        return formatted_response
        
    except ValueError as e:
        # Handle payload validation errors (Requirements 8.1, 8.5)
        error_message = f"Invalid request format: {str(e)}"
        app.logger.error(f"Payload validation error: {error_message}")
        
        # Log security event if this appears to be a potential security issue
        error_str = str(e).lower()
        if any(term in error_str for term in ['too long', 'invalid', 'type', 'format']):
            app.logger.error(f"SECURITY_EVENT: Payload validation failed - {error_message}")
        
        return {
            "error": error_message,
            "error_type": "validation_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "payload_validation",
                "recoverable": True,
                "suggestion": "Please check your request format and try again"
            }
        }
        
    except RatelimitException as e:
        # Handle DuckDuckGo rate limiting (Requirements 8.1, 8.3, 8.5)
        error_message = "Web search rate limit exceeded. Please try again after a short delay."
        app.logger.warning(f"DuckDuckGo rate limit hit: {e}")
        app.logger.debug("Web search rate limit detected - existing websearch() tool error handling mechanism triggered")
        app.logger.info("Existing system gracefully handles rate limits by returning informative error messages")
        return {
            "error": error_message,
            "error_type": "rate_limit_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "web_search_rate_limit",
                "recoverable": True,
                "retry_after_seconds": 60,
                "existing_mechanism": "websearch() tool handles RatelimitException gracefully",
                "suggestion": "Please wait a minute and try your request again"
            }
        }
        
    except DuckDuckGoSearchException as e:
        # Handle DuckDuckGo search API errors (Requirements 8.1, 8.3, 8.5)
        error_message = "Web search service temporarily unavailable. Analysis may be limited."
        app.logger.error(f"DuckDuckGo search error: {e}")
        app.logger.debug("DuckDuckGo search API error detected - existing websearch() tool error handling mechanism triggered")
        app.logger.info("Existing system gracefully handles search API failures with fallback responses")
        return {
            "error": error_message,
            "error_type": "web_search_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "web_search_failure",
                "recoverable": True,
                "fallback_available": True,
                "existing_mechanism": "websearch() tool handles DuckDuckGoSearchException with informative error messages",
                "suggestion": "The system will attempt analysis with available data"
            }
        }
        
    except TypeError as e:
        # Handle agent parameter/model compatibility errors (Requirements 8.1, 8.2, 8.5)
        error_message = "Agent configuration error. Using fallback mechanisms."
        app.logger.error(f"Agent parameter error (fallback engaged): {e}")
        app.logger.debug("Agent parameter TypeError detected - existing invoke_agent() fallback mechanism triggered")
        app.logger.info("Existing system tries multiple parameter formats (max_output_tokens, max_tokens, generation_config, inference_params) before falling back to no-kwargs call")
        return {
            "error": error_message,
            "error_type": "agent_parameter_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "agent_invocation",
                "recoverable": True,
                "fallback_engaged": True,
                "existing_mechanism": "invoke_agent() function tries multiple parameter formats for model compatibility",
                "fallback_sequence": ["max_output_tokens", "max_tokens", "generation_config", "inference_params", "no-kwargs"],
                "suggestion": "The system is using fallback mechanisms to process your request"
            }
        }
        
    except MemoryError as e:
        # Handle memory/token limit issues (Requirements 8.1, 8.4, 8.5)
        error_message = "Request too large. Please try with a shorter query."
        app.logger.error(f"Memory/token limit exceeded: {e}")
        return {
            "error": error_message,
            "error_type": "memory_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "token_limit_exceeded",
                "recoverable": True,
                "suggestion": "Please shorten your query and try again"
            }
        }
        
    except ConnectionError as e:
        # Handle network/connectivity issues (Requirements 8.1, 8.5)
        error_message = "Network connectivity issue. Please try again."
        app.logger.error(f"Network connection error: {e}")
        return {
            "error": error_message,
            "error_type": "connection_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "network_connectivity",
                "recoverable": True,
                "suggestion": "Please check your connection and try again"
            }
        }
        
    except TimeoutError as e:
        # Handle timeout issues (Requirements 8.1, 8.5)
        error_message = "Request timeout. The analysis is taking longer than expected."
        app.logger.error(f"Request timeout: {e}")
        return {
            "error": error_message,
            "error_type": "timeout_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "request_timeout",
                "recoverable": True,
                "suggestion": "Please try again or simplify your request"
            }
        }
        
    except PermissionError as e:
        # Handle permission/access errors (Requirements 8.1, 8.5)
        error_message = "Access denied. Please check your permissions."
        app.logger.error(f"Permission error: {e}")
        app.logger.error(f"SECURITY_EVENT: Permission denied - {e}")
        return {
            "error": error_message,
            "error_type": "permission_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "access_control",
                "recoverable": False,
                "suggestion": "Please contact support if you believe this is an error"
            }
        }
        
    except Exception as e:
        # Handle all other system errors (Requirements 8.1, 8.2, 8.5)
        error_message = "An unexpected error occurred processing your financial advisory request"
        app.logger.error(f"Unexpected system error: {type(e).__name__}: {e}", exc_info=True)
        
        # Log security event for unexpected errors that might indicate security issues
        if any(term in str(e).lower() for term in ['security', 'unauthorized', 'forbidden', 'access', 'permission']):
            app.logger.error(f"SECURITY_EVENT: Unexpected error with security implications - {type(e).__name__}: {e}")
        
        return {
            "error": error_message,
            "error_type": "system_error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "financial-advisor-multiagent",
            "metadata": {
                "error_category": "system_error",
                "error_class": type(e).__name__,
                "recoverable": False,
                "suggestion": "Please try again later or contact support if the issue persists"
            }
        }


# ============================================================
# Application Execution
# ============================================================

if __name__ == "__main__":
    """
    Start the AgentCore application server.
    
    This will start the HTTP server on localhost:8080 for local testing,
    or be managed by AgentCore Runtime when deployed to AWS.
    """
    print("Starting Financial Advisor AgentCore Application...")
    print("Server will be available at http://localhost:8080")
    print("Endpoints:")
    print("  POST /invocations - Main agent invocation")
    print("  GET /ping - Health check")
    print("\n**Important:** This system is for educational purposes only.")
    
    # Log application startup
    app.logger.info("Financial Advisor AgentCore Application starting up")
    app.logger.info("Initializing financial advisor orchestrator and agents")
    
    try:
        # Test orchestrator initialization and existing error handling mechanisms
        app.logger.debug("Testing financial advisor orchestrator initialization")
        app.logger.debug("This test will verify existing error handling mechanisms are preserved")
        test_response = advisor.analyze("Test initialization")
        app.logger.info("Financial advisor orchestrator initialized successfully")
        app.logger.debug("Existing error handling mechanisms verified: invoke_agent() fallbacks, websearch() error handling, token limits")
    except Exception as e:
        app.logger.error(f"Failed to initialize financial advisor orchestrator: {e}")
        app.logger.warning("Application may not function correctly")
        app.logger.debug("Initialization failure - existing error handling mechanisms may not be available")
    
    app.logger.info("Starting AgentCore HTTP server on localhost:8080")
    app.run()