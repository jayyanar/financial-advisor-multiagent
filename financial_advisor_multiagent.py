#!/usr/bin/env python3
"""
Multi-Agent Financial Advisory System

A comprehensive educational financial advisory platform built using the Strands Agents framework.
This system orchestrates multiple specialized AI agents to provide structured financial guidance
through market analysis, trading strategy development, execution planning, and risk assessment.

Architecture Pattern: "Agents as Tools" with hierarchical orchestration
- Financial Coordinator Agent (Orchestrator)
- Market Intelligence Agent (Research & Analysis)
- Strategy Architect Agent (Strategy Development)
- Execution Planner Agent (Implementation Planning)
- Risk Assessor Agent (Risk Analysis & Alignment)

Author: Financial Advisory System
License: Educational Use Only
"""

import logging
from typing import Optional, List, Dict, Any

from strands import Agent, tool
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import RatelimitException, DuckDuckGoSearchException

# ============================================================
# Configuration and Constants
# ============================================================

# Token management - Conservative 2000-token cap per agent call
TOKEN_CAP = 2000

# Model configuration
DEFAULT_MODEL = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

# Logging configuration
logging.getLogger("strands").setLevel(logging.INFO)

# ============================================================
# Core Utility Functions
# ============================================================

def invoke_agent(agent: Agent, prompt: str, max_tokens: int = TOKEN_CAP) -> str:
    """
    Call an Agent with a conservative token cap and robust error handling.
    
    Tries multiple parameter formats for different model providers, then falls back
    to a plain call if parameterized calls fail.
    
    Args:
        agent: The Strands Agent instance to invoke
        prompt: The prompt to send to the agent
        max_tokens: Maximum tokens for the response (default: 2000)
        
    Returns:
        str: Agent response or error message
    """
    # Try common inference kwargs in descending likelihood
    for kwargs in (
        {"max_output_tokens": max_tokens},               # Anthropic-like wrappers
        {"max_tokens": max_tokens},                      # OpenAI-style
        {"generation_config": {"max_output_tokens": max_tokens}},  # some SDKs
        {"inference_params": {"max_tokens": max_tokens}},          # generic
    ):
        try:
            return str(agent(prompt, **kwargs))
        except TypeError:
            continue
        except Exception as e:
            return f"Agent invocation error: {e}"

    # Last-ditch: call without any kwargs
    try:
        return str(agent(prompt))
    except Exception as e:
        return f"Agent invocation error (no-kwargs): {e}"


# ============================================================
# Web Search Tool
# ============================================================

@tool
def websearch(keywords: str, region: str = "us-en", max_results: Optional[int] = None) -> str:
    """
    Search the web to get updated information using DuckDuckGo.
    
    Args:
        keywords: The search query
        region: Region code like 'wt-wt', 'us-en', 'uk-en', etc.
        max_results: Maximum number of results to return
        
    Returns:
        str: Search results or error message
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    except DuckDuckGoSearchException as d:
        return f"DuckDuckGoSearchException: {d}"
    except Exception as e:
        return f"Exception: {e}"


# ============================================================
# Specialist Agents
# ============================================================

class FinancialAdvisoryAgents:
    """Container class for all specialist financial advisory agents."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize all specialist agents with the specified model.
        
        Args:
            model: The model identifier to use for all agents
        """
        self.model = model
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialist agents with their system prompts."""
        
        # Market Intelligence Agent
        self.market_intelligence = Agent(
            model=self.model,
            system_prompt="""You are a specialized Market Intelligence Agent within a financial advisory system.
Your role is to research and analyze market data, news, and filings for a given ticker symbol using web search.

## Responsibilities:
1. Perform web-based research using DuckDuckGo (via the `websearch` tool)
2. Extract insights from SEC filings, reputable news, performance context, and analyst commentary
3. Provide a structured, objective market summary with sources
4. Always include this disclaimer: "This analysis is for educational purposes only and does not constitute financial advice."
""",
            tools=[websearch],
        )
        
        # Strategy Architect Agent
        self.strategy_architect = Agent(
            model=self.model,
            system_prompt="""You are a specialized Strategy Architect Agent within a financial advisory system.
Your role is to develop tailored trading strategies based on user preferences, risk tolerance, and market analysis data.

## Responsibilities:
1. Generate at least 5 distinct trading strategies
2. Align strategies with the user's risk attitude (Conservative, Moderate, Aggressive)
3. Match strategies to the user's investment horizon (Short-term, Medium-term, Long-term)
4. Provide clear rationale and risk assessment for each strategy

Always include the disclaimer: "These strategies are for educational purposes only and do not constitute financial advice."
""",
            tools=[websearch],
        )
        
        # Execution Planner Agent
        self.execution_planner = Agent(
            model=self.model,
            system_prompt="""You are a specialized Execution Planner Agent within a financial advisory system.
Your role is to translate trading strategies into actionable execution guidance with detailed risk management protocols.

## Responsibilities:
1. Create detailed execution plans covering all phases of implementation
2. Specify order types, position sizing, and execution timing
3. Define comprehensive risk controls and mitigation steps
4. Provide step-by-step tactical guidance

Always include the disclaimer: "This execution plan is for educational purposes only and does not constitute financial advice."
""",
            tools=[websearch],
        )
        
        # Risk Assessor Agent
        self.risk_assessor = Agent(
            model=self.model,
            system_prompt="""You are a specialized Risk Assessor Agent within a financial advisory system.
Your role is to provide comprehensive risk analysis of the proposed financial plan, evaluating consistency across market analysis,
trading strategies, execution plans, and user preferences.

## Responsibilities:
1. Evaluate all relevant risk categories comprehensively
2. Assess alignment with the user's stated risk tolerance and timeline
3. Identify misalignments or areas of concern
4. Provide actionable risk mitigation recommendations

Always include the disclaimer: "This risk assessment is for educational purposes only and does not constitute financial advice."
""",
            tools=[websearch],
        )


# ============================================================
# Specialist Agent Tools
# ============================================================

# Global agents instance (initialized when module is imported)
_agents = FinancialAdvisoryAgents()

@tool
def market_intel_tool(ticker: str, lookback_days: int = 7) -> str:
    """
    Delegates market research & analysis to MarketIntelligenceAgent.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        lookback_days: Number of days to look back for analysis (default: 7)
        
    Returns:
        str: Market intelligence analysis with sources
    """
    prompt = (
        f"Research {ticker} for the last {lookback_days} days. "
        f"Use `websearch` to find SEC filings, reputable news, and analyst commentary. "
        f"Provide sources and a concise market summary. "
        f'End with: "This analysis is for educational purposes only and does not constitute financial advice."'
    )
    return invoke_agent(_agents.market_intelligence, prompt, max_tokens=TOKEN_CAP)


@tool
def strategy_architect_tool(ticker: str, risk_attitude: str, horizon: str) -> str:
    """
    Delegates strategy generation to StrategyArchitectAgent.
    
    Args:
        ticker: Stock ticker symbol
        risk_attitude: Risk tolerance level (Conservative, Moderate, Aggressive)
        horizon: Investment time horizon (Short-term, Medium-term, Long-term)
        
    Returns:
        str: Multiple trading strategies with rationale
    """
    prompt = (
        f"Based on market context for {ticker}, generate 5 distinct strategies. "
        f"Align to risk attitude: {risk_attitude}; and horizon: {horizon}. "
        f"For each: objective, thesis, entry/exit, risk, and expected conditions. "
        f'End with: "These strategies are for educational purposes only and do not constitute financial advice."'
    )
    return invoke_agent(_agents.strategy_architect, prompt, max_tokens=TOKEN_CAP)


@tool
def execution_planner_tool(ticker: str, strategy_summary: str) -> str:
    """
    Delegates execution planning to ExecutionPlannerAgent.
    
    Args:
        ticker: Stock ticker symbol
        strategy_summary: Summary of trading strategies from StrategyArchitectAgent
        
    Returns:
        str: Detailed execution plan with order types and risk controls
    """
    prompt = (
        f"Convert the following strategy summary for {ticker} into a detailed execution plan:\n\n"
        f"{strategy_summary}\n\n"
        f"Include order types, sizing, timing windows, and risk controls (stops, limits, hedges). "
        f'End with: "This execution plan is for educational purposes only and does not constitute financial advice."'
    )
    return invoke_agent(_agents.execution_planner, prompt, max_tokens=TOKEN_CAP)


@tool
def risk_assessor_tool(ticker: str, market_summary: str, strategies_summary: str, execution_plan: str) -> str:
    """
    Delegates comprehensive risk evaluation to RiskAssessorAgent.
    
    Args:
        ticker: Stock ticker symbol
        market_summary: Market analysis from MarketIntelligenceAgent
        strategies_summary: Strategy analysis from StrategyArchitectAgent
        execution_plan: Execution plan from ExecutionPlannerAgent
        
    Returns:
        str: Comprehensive risk assessment with mitigation recommendations
    """
    prompt = (
        f"Evaluate overall risk for {ticker}. Consider:\n"
        f"- Market summary:\n{market_summary}\n\n"
        f"- Strategies summary:\n{strategies_summary}\n\n"
        f"- Execution plan:\n{execution_plan}\n\n"
        f"Identify misalignments, key risks, and actionable mitigations. "
        f'End with: "This risk assessment is for educational purposes only and does not constitute financial advice."'
    )
    return invoke_agent(_agents.risk_assessor, prompt, max_tokens=TOKEN_CAP)


# ============================================================
# Orchestrator Agent
# ============================================================

class FinancialAdvisorOrchestrator:
    """
    Main orchestrator for the financial advisory system.
    
    Coordinates all specialist agents and manages user interactions.
    """
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the orchestrator with all specialist tools.
        
        Args:
            model: The model identifier to use for the orchestrator
        """
        self.model = model
        
        # System prompt for the orchestrator
        self.system_prompt = """You are the Financial Coordinator Agent — the lead orchestrator in a comprehensive financial advisory system.
Coordinate specialists, request missing inputs (ticker, risk attitude, horizon), summarize outputs, and keep users informed.

Always include: "**Important:** This is for educational purposes only and does not constitute financial advice."
Keep responses concise and under ~2000 tokens when possible.
"""
        
        # Available tools for the orchestrator
        self.tools = [
            market_intel_tool,
            strategy_architect_tool,
            execution_planner_tool,
            risk_assessor_tool,
        ]
        
        # Create the orchestrator agent
        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            tools=self.tools,
        )
    
    def analyze(self, user_query: str) -> str:
        """
        Process a user query through the complete financial advisory workflow.
        
        Args:
            user_query: User's financial advisory request
            
        Returns:
            str: Comprehensive financial advisory response
        """
        return str(self.agent(user_query))
    
    def get_market_analysis(self, ticker: str, lookback_days: int = 7) -> str:
        """
        Get market analysis for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
            lookback_days: Number of days to analyze
            
        Returns:
            str: Market analysis report
        """
        return market_intel_tool(ticker=ticker, lookback_days=lookback_days)
    
    def get_strategies(self, ticker: str, risk_attitude: str, horizon: str) -> str:
        """
        Generate trading strategies for a ticker with specified parameters.
        
        Args:
            ticker: Stock ticker symbol
            risk_attitude: Risk tolerance (Conservative, Moderate, Aggressive)
            horizon: Time horizon (Short-term, Medium-term, Long-term)
            
        Returns:
            str: Trading strategies report
        """
        return strategy_architect_tool(ticker=ticker, risk_attitude=risk_attitude, horizon=horizon)
    
    def get_execution_plan(self, ticker: str, strategy_summary: str) -> str:
        """
        Generate execution plan for given strategies.
        
        Args:
            ticker: Stock ticker symbol
            strategy_summary: Summary of trading strategies
            
        Returns:
            str: Execution plan report
        """
        return execution_planner_tool(ticker=ticker, strategy_summary=strategy_summary)
    
    def get_risk_assessment(self, ticker: str, market_summary: str, 
                          strategies_summary: str, execution_plan: str) -> str:
        """
        Generate comprehensive risk assessment.
        
        Args:
            ticker: Stock ticker symbol
            market_summary: Market analysis
            strategies_summary: Trading strategies
            execution_plan: Execution plan
            
        Returns:
            str: Risk assessment report
        """
        return risk_assessor_tool(
            ticker=ticker,
            market_summary=market_summary,
            strategies_summary=strategies_summary,
            execution_plan=execution_plan
        )
    
    def run_complete_analysis(self, ticker: str, risk_attitude: str = "Moderate", 
                            horizon: str = "Medium-term", lookback_days: int = 7) -> Dict[str, str]:
        """
        Run complete financial advisory analysis workflow.
        
        Args:
            ticker: Stock ticker symbol
            risk_attitude: Risk tolerance (default: Moderate)
            horizon: Time horizon (default: Medium-term)
            lookback_days: Analysis lookback period (default: 7)
            
        Returns:
            Dict[str, str]: Complete analysis results with all components
        """
        # Step 1: Market Analysis
        market_analysis = self.get_market_analysis(ticker, lookback_days)
        
        # Step 2: Strategy Development
        strategies = self.get_strategies(ticker, risk_attitude, horizon)
        
        # Step 3: Execution Planning (truncate strategies if too long)
        execution_plan = self.get_execution_plan(ticker, strategies[:2000])
        
        # Step 4: Risk Assessment (truncate inputs if too long)
        risk_assessment = self.get_risk_assessment(
            ticker=ticker,
            market_summary=market_analysis[:2000],
            strategies_summary=strategies[:2000],
            execution_plan=execution_plan[:2000]
        )
        
        return {
            "ticker": ticker,
            "risk_attitude": risk_attitude,
            "horizon": horizon,
            "market_analysis": market_analysis,
            "strategies": strategies,
            "execution_plan": execution_plan,
            "risk_assessment": risk_assessment
        }


# ============================================================
# Main Interface and Initialization
# ============================================================

def initialize_system(model: str = DEFAULT_MODEL) -> FinancialAdvisorOrchestrator:
    """
    Initialize the complete financial advisory system.
    
    Args:
        model: Model identifier to use for all agents
        
    Returns:
        FinancialAdvisorOrchestrator: Initialized orchestrator instance
    """
    orchestrator = FinancialAdvisorOrchestrator(model=model)
    
    print("✅ Multi-Agent Financial Advisory System initialized")
    print(f"   Orchestrator: FinancialAdvisorOrchestrator")
    print(f"   Model: {model}")
    print(f"   Tools mounted: {len(orchestrator.tools)}")
    for i, tool in enumerate(orchestrator.tools, 1):
        tool_name = getattr(tool, "__name__", getattr(tool, "name", "unknown_tool"))
        print(f"   {i}. {tool_name}")
    
    return orchestrator


# ============================================================
# Example Usage and Testing
# ============================================================

def example_usage():
    """Demonstrate basic usage of the financial advisory system."""
    
    # Initialize the system
    advisor = initialize_system()
    
    # Example 1: Simple query through orchestrator
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Query")
    print("="*60)
    
    user_query = """
    I'm interested in getting financial advice for AAPL stock. 
    I have a moderate risk tolerance and am looking at a medium-term investment horizon.
    """
    
    response = advisor.analyze(user_query)
    print(response)
    
    # Example 2: Complete analysis workflow
    print("\n" + "="*60)
    print("EXAMPLE 2: Complete Analysis Workflow")
    print("="*60)
    
    results = advisor.run_complete_analysis(
        ticker="AAPL",
        risk_attitude="Moderate",
        horizon="Medium-term",
        lookback_days=7
    )
    
    for section, content in results.items():
        if section not in ["ticker", "risk_attitude", "horizon"]:
            print(f"\n--- {section.upper().replace('_', ' ')} ---")
            print(content[:500] + "..." if len(content) > 500 else content)


if __name__ == "__main__":
    # Initialize system when run as main module
    advisor = initialize_system()
    
    # Uncomment to run examples
    # example_usage()
    
    print("\n" + "="*60)
    print("SYSTEM READY")
    print("="*60)
    print("The financial advisory system is now ready for use.")
    print("Use the 'advisor' instance to interact with the system.")
    print("\nExample usage:")
    print("  response = advisor.analyze('Analyze TSLA stock for aggressive investor')")
    print("  results = advisor.run_complete_analysis('MSFT', 'Conservative', 'Long-term')")
    print("\n**Important:** This system is for educational purposes only.")