#!/usr/bin/env python3
"""
AgentCore Financial Advisor Module Entry Point

This module serves as the entry point when running as `python -m financial_advisor_agentcore`
"""

from .main import app

if __name__ == "__main__":
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
        # Test orchestrator initialization
        from financial_advisor_multiagent import FinancialAdvisorOrchestrator
        advisor = FinancialAdvisorOrchestrator()
        app.logger.debug("Testing financial advisor orchestrator initialization")
        test_response = advisor.analyze("Test initialization")
        app.logger.info("Financial advisor orchestrator initialized successfully")
    except Exception as e:
        app.logger.error(f"Failed to initialize financial advisor orchestrator: {e}")
        app.logger.warning("Application may not function correctly")
    
    app.logger.info("Starting AgentCore HTTP server on localhost:8080")
    app.run()