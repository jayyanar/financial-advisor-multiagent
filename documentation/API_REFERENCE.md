# Financial Advisor Multiagent System - API Reference

This document provides comprehensive API documentation for the `financial_advisor_multiagent.py` module.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Classes](#core-classes)
- [Agent Tools](#agent-tools)
- [Utility Functions](#utility-functions)
- [AgentCore Deployment](#agentcore-deployment)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Installation

```bash
pip install strands-agents strands-agents-tools duckduckgo-search boto3
```

## Quick Start

```python
from financial_advisor_multiagent import initialize_system

# Initialize the system
advisor = initialize_system()

# Simple analysis
response = advisor.analyze("Analyze AAPL for moderate risk investor")

# Complete workflow
results = advisor.run_complete_analysis("AAPL", "Moderate", "Medium-term")
```

## Core Classes

### FinancialAdvisorOrchestrator

Main orchestrator class that coordinates all specialist agents.

#### Constructor

```python
FinancialAdvisorOrchestrator(model: str = DEFAULT_MODEL)
```

**Parameters:**
- `model` (str): Model identifier to use for the orchestrator (default: "us.anthropic.claude-3-7-sonnet-20250219-v1:0")

#### Methods

##### analyze(user_query: str) -> str

Process a user query through the complete financial advisory workflow.

**Parameters:**
- `user_query` (str): User's financial advisory request

**Returns:**
- `str`: Comprehensive financial advisory response

**Example:**
```python
response = advisor.analyze("I want to invest $10,000 in tech stocks with moderate risk")
```

##### get_market_analysis(ticker: str, lookback_days: int = 7) -> str

Get market analysis for a specific ticker.

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
- `lookback_days` (int): Number of days to analyze (default: 7)

**Returns:**
- `str`: Market analysis report with sources

**Example:**
```python
market_report = advisor.get_market_analysis("AAPL", lookback_days=14)
```

##### get_strategies(ticker: str, risk_attitude: str, horizon: str) -> str

Generate trading strategies for a ticker with specified parameters.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `risk_attitude` (str): Risk tolerance ("Conservative", "Moderate", "Aggressive")
- `horizon` (str): Time horizon ("Short-term", "Medium-term", "Long-term")

**Returns:**
- `str`: Multiple trading strategies with rationale

**Example:**
```python
strategies = advisor.get_strategies("AAPL", "Moderate", "Medium-term")
```

##### get_execution_plan(ticker: str, strategy_summary: str) -> str

Generate execution plan for given strategies.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `strategy_summary` (str): Summary of trading strategies

**Returns:**
- `str`: Detailed execution plan with order types and risk controls

**Example:**
```python
execution_plan = advisor.get_execution_plan("AAPL", strategies)
```

##### get_risk_assessment(ticker: str, market_summary: str, strategies_summary: str, execution_plan: str) -> str

Generate comprehensive risk assessment.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `market_summary` (str): Market analysis
- `strategies_summary` (str): Trading strategies
- `execution_plan` (str): Execution plan

**Returns:**
- `str`: Comprehensive risk assessment with mitigation recommendations

**Example:**
```python
risk_assessment = advisor.get_risk_assessment("AAPL", market_report, strategies, execution_plan)
```

##### run_complete_analysis(ticker: str, risk_attitude: str = "Moderate", horizon: str = "Medium-term", lookback_days: int = 7) -> Dict[str, str]

Run complete financial advisory analysis workflow.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `risk_attitude` (str): Risk tolerance (default: "Moderate")
- `horizon` (str): Time horizon (default: "Medium-term")
- `lookback_days` (int): Analysis lookback period (default: 7)

**Returns:**
- `Dict[str, str]`: Complete analysis results with all components

**Example:**
```python
results = advisor.run_complete_analysis(
    ticker="AAPL",
    risk_attitude="Aggressive",
    horizon="Short-term",
    lookback_days=14
)

# Access individual components
market_analysis = results["market_analysis"]
strategies = results["strategies"]
execution_plan = results["execution_plan"]
risk_assessment = results["risk_assessment"]
```

### FinancialAdvisoryAgents

Container class for all specialist financial advisory agents.

#### Constructor

```python
FinancialAdvisoryAgents(model: str = DEFAULT_MODEL)
```

**Parameters:**
- `model` (str): Model identifier to use for all agents

#### Properties

- `market_intelligence`: Market Intelligence Agent instance
- `strategy_architect`: Strategy Architect Agent instance
- `execution_planner`: Execution Planner Agent instance
- `risk_assessor`: Risk Assessor Agent instance

## Agent Tools

### market_intel_tool(ticker: str, lookback_days: int = 7) -> str

Delegates market research & analysis to MarketIntelligenceAgent.

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
- `lookback_days` (int): Number of days to look back for analysis (default: 7)

**Returns:**
- `str`: Market intelligence analysis with sources

### strategy_architect_tool(ticker: str, risk_attitude: str, horizon: str) -> str

Delegates strategy generation to StrategyArchitectAgent.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `risk_attitude` (str): Risk tolerance level ("Conservative", "Moderate", "Aggressive")
- `horizon` (str): Investment time horizon ("Short-term", "Medium-term", "Long-term")

**Returns:**
- `str`: Multiple trading strategies with rationale

### execution_planner_tool(ticker: str, strategy_summary: str) -> str

Delegates execution planning to ExecutionPlannerAgent.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `strategy_summary` (str): Summary of trading strategies from StrategyArchitectAgent

**Returns:**
- `str`: Detailed execution plan with order types and risk controls

### risk_assessor_tool(ticker: str, market_summary: str, strategies_summary: str, execution_plan: str) -> str

Delegates comprehensive risk evaluation to RiskAssessorAgent.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `market_summary` (str): Market analysis from MarketIntelligenceAgent
- `strategies_summary` (str): Strategy analysis from StrategyArchitectAgent
- `execution_plan` (str): Execution plan from ExecutionPlannerAgent

**Returns:**
- `str`: Comprehensive risk assessment with mitigation recommendations

### websearch(keywords: str, region: str = "us-en", max_results: Optional[int] = None) -> str

Search the web to get updated information using DuckDuckGo.

**Parameters:**
- `keywords` (str): The search query
- `region` (str): Region code like 'wt-wt', 'us-en', 'uk-en', etc. (default: "us-en")
- `max_results` (Optional[int]): Maximum number of results to return

**Returns:**
- `str`: Search results or error message

## Utility Functions

### invoke_agent(agent: Agent, prompt: str, max_tokens: int = TOKEN_CAP) -> str

Call an Agent with a conservative token cap and robust error handling.

**Parameters:**
- `agent` (Agent): The Strands Agent instance to invoke
- `prompt` (str): The prompt to send to the agent
- `max_tokens` (int): Maximum tokens for the response (default: 2000)

**Returns:**
- `str`: Agent response or error message

### initialize_system(model: str = DEFAULT_MODEL) -> FinancialAdvisorOrchestrator

Initialize the complete financial advisory system.

**Parameters:**
- `model` (str): Model identifier to use for all agents

**Returns:**
- `FinancialAdvisorOrchestrator`: Initialized orchestrator instance

## AgentCore Deployment

The financial advisor system can be deployed to Amazon Bedrock AgentCore Runtime using a wrapper that maintains all existing functionality while adapting to AgentCore's service contract.

### AgentCore Wrapper Functions

#### process_agentcore_payload(payload: Dict[str, Any]) -> str

Extract and validate user query from AgentCore payload format.

**Parameters:**
- `payload` (Dict[str, Any]): AgentCore request payload with 'prompt' field

**Returns:**
- `str`: Processed user query for financial advisor system

**Raises:**
- `ValueError`: If payload is invalid, missing required fields, or exceeds length limits

**Security Features:**
- Input validation and sanitization
- Length limits (5000 characters maximum)
- Type checking for prompt field

#### format_agentcore_response(advisor_response: str) -> Dict[str, Any]

Format financial advisor response for AgentCore compatibility.

**Parameters:**
- `advisor_response` (str): Response from FinancialAdvisorOrchestrator

**Returns:**
- `Dict[str, Any]`: AgentCore-compatible response with metadata

**Response Structure:**
```json
{
    "result": "financial analysis content",
    "timestamp": "2024-01-15T10:30:00Z",
    "system": "financial-advisor-multiagent",
    "metadata": {
        "version": "1.0.0",
        "agent_type": "financial_advisor",
        "educational_disclaimer": true,
        "capabilities": ["market_intelligence", "strategy_development", "execution_planning", "risk_assessment"]
    }
}
```

### AgentCore Entry Point

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from financial_advisor_multiagent import FinancialAdvisorOrchestrator

app = BedrockAgentCoreApp()
advisor = FinancialAdvisorOrchestrator()

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    AgentCore entry point for financial advisory requests.
    
    Args:
        payload: AgentCore payload containing user request
            Expected format: {"prompt": "user query string"}
            
    Returns:
        dict: Structured response with analysis results
            Format: {"result": "analysis", "timestamp": "iso_date", ...}
    """
    user_query = payload.get("prompt", "")
    response = advisor.analyze(user_query)
    return {"result": response}

if __name__ == "__main__":
    app.run()
```

### AgentCore Payload Format

**Input Payload:**
```json
{
    "prompt": "Analyze AAPL stock for moderate risk investor with medium-term horizon"
}
```

**Output Response:**
```json
{
    "result": "Comprehensive financial analysis...",
    "timestamp": "2024-01-15T10:30:00Z",
    "system": "financial-advisor-multiagent",
    "version": "1.0.0"
}
```

### AgentCore Deployment Commands

```bash
# Install AgentCore dependencies
pip install bedrock-agentcore-starter-toolkit

# Configure deployment
agentcore configure --entrypoint financial_advisor_agentcore.py

# Deploy to AWS
agentcore launch

# Test deployed agent
agentcore invoke '{"prompt": "Provide financial analysis for TSLA"}'

# Monitor deployment
agentcore status
agentcore logs
```

### AgentCore Error Handling

The AgentCore wrapper includes comprehensive error handling:

```python
@app.entrypoint
def invoke(payload):
    try:
        # Process request
        user_query = process_agentcore_payload(payload)
        response = advisor.analyze(user_query)
        return format_agentcore_response(response)
        
    except ValueError as e:
        # Invalid payload format
        return {"error": f"Invalid request format: {str(e)}"}
        
    except Exception as e:
        # General system errors
        app.logger.error(f"Financial advisor error: {e}")
        return {"error": "An error occurred processing your request"}
```

### AgentCore Security Considerations

- **Input Validation**: All user inputs are sanitized and validated
- **Credential Management**: Uses IAM roles for AWS service access
- **Error Sanitization**: Error messages are sanitized to prevent information disclosure
- **Rate Limiting**: Built-in rate limiting through AgentCore infrastructure
- **Monitoring**: Comprehensive logging and monitoring through CloudWatch

For complete AgentCore deployment instructions, see [AGENTCORE_DEPLOYMENT_GUIDE.md](AGENTCORE_DEPLOYMENT_GUIDE.md).

## Configuration

### Constants

- `TOKEN_CAP`: Conservative 2000-token cap per agent call
- `DEFAULT_MODEL`: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

### Model Configuration

```python
# Use default model
advisor = initialize_system()

# Use custom model
advisor = initialize_system(model="your-custom-model-id")
```

## Error Handling

The system implements robust error handling with multiple fallback mechanisms:

### Agent Invocation Resilience

The `invoke_agent` function tries multiple parameter formats:
1. `{"max_output_tokens": max_tokens}` - Anthropic-style
2. `{"max_tokens": max_tokens}` - OpenAI-style  
3. `{"generation_config": {"max_output_tokens": max_tokens}}` - Generic SDK
4. `{"inference_params": {"max_tokens": max_tokens}}` - Alternative format
5. Plain agent call without parameters as final fallback

### Web Search Resilience

The `websearch` tool handles various exceptions:
- `RatelimitException`: Graceful degradation with retry message
- `DDGSException`: DuckDuckGo-specific errors
- Generic `Exception`: Catch-all for unexpected errors

### Token Management

- Conservative 2000-token limits prevent excessive resource usage
- Automatic truncation when passing data between agents
- Intelligent string slicing to maintain context

## Examples

### Basic Usage

```python
from financial_advisor_multiagent import initialize_system

# Initialize system
advisor = initialize_system()

# Simple analysis
response = advisor.analyze("Should I invest in NVDA with high risk tolerance?")
print(response)
```

### Complete Workflow

```python
# Run complete analysis
results = advisor.run_complete_analysis(
    ticker="TSLA",
    risk_attitude="Aggressive", 
    horizon="Short-term",
    lookback_days=14
)

# Print each component
for component, content in results.items():
    if component not in ["ticker", "risk_attitude", "horizon"]:
        print(f"\n=== {component.upper().replace('_', ' ')} ===")
        print(content)
```

### Individual Components

```python
# Get market analysis only
market_analysis = advisor.get_market_analysis("AAPL", lookback_days=30)

# Generate strategies based on market context
strategies = advisor.get_strategies("AAPL", "Conservative", "Long-term")

# Create execution plan
execution_plan = advisor.get_execution_plan("AAPL", strategies[:2000])

# Assess risks
risk_assessment = advisor.get_risk_assessment(
    ticker="AAPL",
    market_summary=market_analysis[:2000],
    strategies_summary=strategies[:2000], 
    execution_plan=execution_plan[:2000]
)
```

### Custom Model Usage

```python
# Use different model
custom_advisor = initialize_system(model="anthropic.claude-3-sonnet-20240229-v1:0")

# Use with custom configuration
response = custom_advisor.analyze("Analyze AMZN for retirement portfolio")
```

### Error Handling Example

```python
try:
    results = advisor.run_complete_analysis("INVALID_TICKER")
except Exception as e:
    print(f"Analysis failed: {e}")
    # The system will still return results with error messages
    # rather than crashing completely
```

## Important Notes

### Educational Disclaimers

All agent outputs include comprehensive educational disclaimers:
- "This analysis is for educational purposes only and does not constitute financial advice."
- "These strategies are for educational purposes only and do not constitute financial advice."
- "This execution plan is for educational purposes only and does not constitute financial advice."
- "This risk assessment is for educational purposes only and does not constitute financial advice."

### Rate Limiting

Web search functionality may be rate-limited by DuckDuckGo. The system handles this gracefully with appropriate error messages.

### Token Limits

The 2000-token limit per agent call may truncate very detailed analyses. For complex scenarios, consider breaking down requests into smaller components.

### Data Sources

The system relies on publicly available information through DuckDuckGo search. It does not have access to real-time market feeds or proprietary financial data.