# Financial Advisor Multiagent System Documentation

## Overview

The Financial Advisor Multiagent System is a comprehensive educational financial advisory platform built using the Strands Agents framework. This system orchestrates multiple specialized AI agents to provide structured financial guidance through market analysis, trading strategy development, execution planning, and risk assessment.

## System Architecture

### Core Framework
- **Primary Framework**: Strands Agents SDK
- **Programming Language**: Python 3.12+
- **Development Environment**: Jupyter Notebook
- **Model Provider**: Amazon Bedrock (Claude 3.5 Sonnet)
- **Web Search Integration**: DuckDuckGo Search (ddgs)

### Multi-Agent Architecture Pattern
The system implements the "Agents as Tools" pattern with a hierarchical structure:

```
Financial Coordinator Agent (Orchestrator)
├── Market Intelligence Agent
├── Strategy Architect Agent  
├── Execution Planner Agent
└── Risk Assessor Agent
```

## Agent Specifications

### 1. Financial Coordinator Agent (Orchestrator)
**Role**: Primary orchestrator that coordinates all specialist agents and manages user interactions.

**Responsibilities**:
- Request missing inputs (ticker symbol, risk tolerance, investment horizon)
- Coordinate specialist agents through tool calls
- Summarize outputs from all agents
- Maintain conversation flow and user engagement
- Ensure educational disclaimers are included

**Model**: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`

**Tools Available**:
- `market_intel_tool`
- `strategy_architect_tool`
- `execution_planner_tool`
- `risk_assessor_tool`

### 2. Market Intelligence Agent
**Role**: Specialized market research and analysis agent.

**Responsibilities**:
- Perform web-based research using DuckDuckGo search
- Extract insights from SEC filings, news, and analyst commentary
- Provide structured, objective market summaries with sources
- Focus on recent market developments and performance context

**Key Features**:
- Dynamic ticker symbol support
- Configurable lookback periods (default: 7 days)
- Source attribution for all research findings
- Educational disclaimers included

### 3. Strategy Architect Agent
**Role**: Trading strategy development specialist.

**Responsibilities**:
- Generate multiple distinct trading strategies (minimum 5)
- Align strategies with user risk tolerance (Conservative/Moderate/Aggressive)
- Match strategies to investment horizon (Short/Medium/Long-term)
- Provide clear rationale and risk assessment for each strategy

**Strategy Categories**:
- Growth-focused accumulation
- Momentum breakout strategies
- Value-based approaches
- Options-enhanced income strategies
- Pullback accumulation methods

### 4. Execution Planner Agent
**Role**: Tactical execution and implementation specialist.

**Responsibilities**:
- Translate strategies into actionable execution plans
- Specify order types, position sizing, and timing
- Define comprehensive risk controls and mitigation steps
- Provide step-by-step tactical guidance

**Execution Components**:
- Phase-based implementation plans
- Order type specifications
- Risk management protocols
- Performance monitoring frameworks

### 5. Risk Assessor Agent
**Role**: Comprehensive risk analysis specialist.

**Responsibilities**:
- Evaluate all relevant risk categories
- Assess alignment with user preferences
- Identify misalignments and areas of concern
- Provide actionable risk mitigation recommendations

**Risk Categories Assessed**:
- Market risk and volatility
- Competitive landscape risks
- Execution and timing risks
- Strategy-specific risks
- Portfolio concentration risks

## Technical Implementation

### Token Management
The system implements conservative token management with a 2000-token cap per agent call:

```python
TOKEN_CAP = 2000

def invoke_agent(agent: Agent, prompt: str, max_tokens: int = TOKEN_CAP) -> str:
    # Tries multiple parameter formats for different model providers
    for kwargs in (
        {"max_output_tokens": max_tokens},
        {"max_tokens": max_tokens},
        {"generation_config": {"max_output_tokens": max_tokens}},
        {"inference_params": {"max_tokens": max_tokens}},
    ):
        try:
            return str(agent(prompt, **kwargs))
        except TypeError:
            continue
    # Fallback to no-kwargs call
    return str(agent(prompt))
```

### Web Search Integration
Robust web search functionality with error handling:

```python
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    except DDGSException as d:
        return f"DuckDuckGoSearchException: {d}"
    except Exception as e:
        return f"Exception: {e}"
```

### Agent Tool Delegation
Each specialist agent is wrapped as a tool for the orchestrator:

```python
@tool
def market_intel_tool(ticker: str, lookback_days: int = 7) -> str:
    prompt = (
        f"Research {ticker} for the last {lookback_days} days. "
        f"Use `websearch` to find SEC filings, reputable news, and analyst commentary. "
        f"Provide sources and a concise market summary."
    )
    return invoke_agent(MarketIntelligenceAgent, prompt, max_tokens=TOKEN_CAP)
```

## Usage Examples

### Basic Usage
```python
# Initialize the system (already done in notebook)
# AdvisoryOrchestratorAgent is ready to use

# Example user query
user_query = """
I'm interested in getting financial advice for AAPL stock. 
I have a moderate risk tolerance and am looking at a medium-term investment horizon.
"""

# Get comprehensive financial advice
response = AdvisoryOrchestratorAgent(user_query)
print(response)
```

### Manual Agent Testing
```python
# Test individual agents
market_analysis = market_intel_tool(ticker="AAPL", lookback_days=7)
strategies = strategy_architect_tool(ticker="AAPL", risk_attitude="Moderate", horizon="Medium-term")
execution_plan = execution_planner_tool(ticker="AAPL", strategy_summary=strategies[:2000])
risk_assessment = risk_assessor_tool(
    ticker="AAPL", 
    market_summary=market_analysis[:2000],
    strategies_summary=strategies[:2000], 
    execution_plan=execution_plan[:2000]
)
```

## Key Features

### 1. Dynamic Ticker Support
- System accepts any stock ticker symbol
- Agents adapt research and analysis to the specified security
- No hardcoded stock-specific logic

### 2. Risk Tolerance Alignment
- **Conservative**: Focus on capital preservation, dividend strategies, lower volatility
- **Moderate**: Balanced growth and income approaches, moderate risk tolerance
- **Aggressive**: Growth-focused strategies, higher risk tolerance, momentum plays

### 3. Investment Horizon Matching
- **Short-term**: 3-12 months, technical analysis focus, momentum strategies
- **Medium-term**: 1-3 years, balanced fundamental/technical approach
- **Long-term**: 3+ years, fundamental analysis focus, value strategies

### 4. Comprehensive Risk Assessment
- Market and volatility risks
- Competitive landscape analysis
- Execution and timing risks
- Portfolio concentration concerns
- Strategy alignment evaluation

### 5. Educational Focus
All agents include educational disclaimers:
> "This analysis/strategy/plan is for educational purposes only and does not constitute financial advice."

## Error Handling and Resilience

### Web Search Resilience
- Rate limit handling with graceful degradation
- Multiple exception types caught and handled
- Fallback responses when search fails

### Agent Invocation Resilience
- Multiple parameter format attempts for different model providers
- Graceful fallback to basic agent calls
- Error message capture and reporting

### Token Management
- Conservative 2000-token limits to prevent truncation
- Automatic truncation of inputs when passing between agents
- Efficient prompt engineering to maximize information density

## Output Structure

### Market Intelligence Output
- Stock performance summary
- Recent developments and news
- Financial performance metrics
- Analyst perspectives
- Market context and outlook
- Source attribution

### Strategy Development Output
- 5+ distinct trading strategies
- Objective and thesis for each strategy
- Entry/exit criteria
- Risk management approach
- Expected market conditions
- Risk-return profile assessment

### Execution Planning Output
- Phase-based implementation plan
- Specific order types and sizing
- Timing and execution windows
- Risk controls and stop-losses
- Performance monitoring framework
- Technical level specifications

### Risk Assessment Output
- Market alignment analysis
- Risk category evaluation
- Misalignment identification
- Mitigation recommendations
- Portfolio-level considerations
- Scenario analysis

## Best Practices

### 1. User Input Validation
- Always request missing required parameters (ticker, risk tolerance, horizon)
- Validate risk tolerance against accepted values
- Confirm investment horizon alignment

### 2. Source Attribution
- Include sources for all market research
- Timestamp analysis when relevant
- Distinguish between factual data and analysis

### 3. Educational Emphasis
- Include disclaimers in all outputs
- Emphasize educational nature of advice
- Encourage users to consult licensed financial advisors

### 4. Risk Management
- Always include stop-loss recommendations
- Address position sizing considerations
- Discuss portfolio diversification needs

## Limitations and Considerations

### 1. Educational Purpose Only
- System provides educational content, not licensed financial advice
- Users should consult qualified financial advisors for investment decisions
- No guarantee of strategy performance or outcomes

### 2. Market Data Limitations
- Relies on web search for market data (not real-time feeds)
- Information accuracy depends on source quality
- May have delays in accessing latest market developments

### 3. Model Limitations
- Subject to AI model limitations and potential hallucinations
- Token limits may truncate complex analyses
- No access to proprietary financial databases

### 4. Risk Assessment Scope
- Cannot account for individual financial situations
- Limited to publicly available information
- No access to user's complete financial picture

## Future Enhancements

### Potential Improvements
1. **Real-time Data Integration**: Connect to financial data APIs
2. **Portfolio Analysis**: Add portfolio-level optimization capabilities
3. **Backtesting Framework**: Historical strategy performance analysis
4. **Regulatory Compliance**: Enhanced compliance checking
5. **Multi-Asset Support**: Extend beyond individual stocks to ETFs, bonds, etc.
6. **Sentiment Analysis**: Incorporate social media and news sentiment
7. **Technical Analysis Tools**: Add charting and technical indicator analysis

### Scalability Considerations
- Agent response caching for common queries
- Parallel agent execution for improved performance
- Database integration for historical analysis storage
- User session management for personalized experiences

## Conclusion

The Financial Advisor Multiagent System demonstrates a sophisticated approach to AI-powered financial analysis using the Strands Agents framework. By orchestrating multiple specialized agents, the system provides comprehensive, structured financial guidance while maintaining educational focus and responsible AI practices.

The modular architecture allows for easy extension and modification, while the robust error handling ensures reliable operation even when external dependencies (web search, model APIs) experience issues. The system serves as an excellent example of multi-agent coordination and practical AI application in the financial domain.