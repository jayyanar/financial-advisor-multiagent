# Product Overview

This repository contains AI-powered financial advisory systems built with the Strands Agents framework, demonstrating sophisticated multi-agent architectures for educational financial guidance. The system has evolved into a comprehensive platform with both notebook-based prototypes and production-ready web applications.

## Core Products

### 1. Financial Advisor Multiagent System (Notebook)
A comprehensive educational financial advisory system that orchestrates multiple specialized AI agents to provide structured financial guidance through market analysis, trading strategy development, execution planning, and risk assessment.

**Architecture Pattern**: "Agents as Tools" with hierarchical orchestration
```
Financial Coordinator Agent (Orchestrator)
├── Market Intelligence Agent (Research & Analysis)
├── Strategy Architect Agent (Strategy Development)  
├── Execution Planner Agent (Implementation Planning)
└── Risk Assessor Agent (Risk Analysis & Alignment)
```

**Key Features:**
- **Dynamic Ticker Support**: Accepts any stock ticker symbol with adaptive analysis
- **Risk Tolerance Alignment**: Conservative/Moderate/Aggressive risk profiling
- **Investment Horizon Matching**: Short/Medium/Long-term strategy alignment
- **Comprehensive Market Research**: Web-based research using DuckDuckGo Search
- **Multi-Strategy Generation**: Minimum 5 distinct trading strategies per request
- **Detailed Execution Planning**: Phase-based implementation with specific order types
- **Risk Assessment Framework**: Multi-category risk evaluation with mitigation recommendations
- **Token Management**: Conservative 2000-token limits with robust error handling
- **Educational Focus**: Comprehensive disclaimers and responsible AI practices

**Technical Specifications:**
- **Model**: Amazon Bedrock Claude 3.5 Sonnet (`us.anthropic.claude-3-7-sonnet-20250219-v1:0`)
- **Web Search**: DuckDuckGo Search (ddgs) with rate limit handling
- **Token Cap**: 2000 tokens per agent call with fallback mechanisms
- **Error Resilience**: Multi-parameter format attempts for different model providers

### 2. Financial Advisor Web Application (Production)
A full-stack web application providing the financial advisory system through a modern web interface with real-time communication and session management.

**Frontend Architecture:**
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Modern CSS with responsive design
- **Real-time Communication**: WebSocket integration

**Backend Architecture:**
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Session Management**: Persistent user sessions with conversation history
- **WebSocket Support**: Real-time agent communication
- **Agent Management**: Centralized agent orchestration with error handling

**Key Components:**
- **Session Management**: Persistent conversation tracking across user interactions
- **WebSocket Manager**: Real-time bidirectional communication between frontend and agents
- **Agent Manager**: Centralized coordination of all financial advisory agents
- **Database Models**: User sessions, conversation history, and advisory context storage
- **API Routers**: RESTful endpoints for sessions, advisory services, and WebSocket connections

### 3. Strands Agents Learning Materials
Educational resources and examples for working with the Strands Agents SDK, including setup instructions, basic agent creation, and tool integration examples.

**Contents:**
- **Basic Setup**: Installation and environment configuration
- **Agent Creation**: Step-by-step agent development examples
- **Tool Integration**: MCP and native tool implementation patterns
- **Model Provider Setup**: Configuration for various AI model providers

## System Capabilities

### Market Intelligence
- **Web-based Research**: Real-time market data gathering via DuckDuckGo
- **SEC Filing Analysis**: Automated extraction of regulatory filing insights
- **News Aggregation**: Recent developments and analyst commentary synthesis
- **Source Attribution**: Complete source tracking for all research findings
- **Performance Context**: Historical performance analysis with market comparisons

### Strategy Development
- **Multi-Strategy Generation**: Minimum 5 distinct approaches per request
- **Risk Alignment**: Strategies matched to user risk tolerance (Conservative/Moderate/Aggressive)
- **Horizon Matching**: Time-based strategy optimization (Short/Medium/Long-term)
- **Strategy Categories**: Growth, momentum, value, options-enhanced, pullback accumulation
- **Rationale Documentation**: Clear thesis and risk assessment for each strategy

### Execution Planning
- **Phase-based Implementation**: Structured rollout with defined milestones
- **Order Specifications**: Detailed order types, sizing, and timing guidance
- **Risk Controls**: Comprehensive stop-loss, limit orders, and hedging strategies
- **Performance Monitoring**: Framework for tracking strategy effectiveness
- **Technical Analysis**: Support/resistance levels and entry/exit criteria

### Risk Assessment
- **Multi-category Analysis**: Market, competitive, execution, and strategy-specific risks
- **Alignment Evaluation**: Assessment against user preferences and constraints
- **Misalignment Detection**: Identification of strategy-preference conflicts
- **Mitigation Recommendations**: Actionable risk reduction strategies
- **Portfolio Context**: Concentration and diversification considerations

## Target Audience

### Primary Users
- **Developers**: Learning multi-agent AI system architecture and implementation
- **Financial Technology Enthusiasts**: Educational exploration of AI-powered financial analysis
- **AI Researchers**: Studying agent orchestration patterns and tool integration
- **Students**: Understanding practical applications of AI in financial services

### Use Cases
- **Educational Financial Analysis**: Learning market research and strategy development
- **Multi-Agent System Development**: Understanding "Agents as Tools" patterns
- **AI Tool Integration**: Implementing web search and external API integration
- **Responsible AI Development**: Best practices for disclaimers and ethical AI use

## Deployment Options

### Development Environment
- **Jupyter Notebook**: Interactive development and testing
- **Local Web Application**: Full-stack development with hot reload
- **Docker Compose**: Containerized development environment

### Production Deployment
- **Docker Containers**: Frontend and backend containerization
- **Production Docker Compose**: Optimized production configuration
- **Environment Configuration**: Secure credential and configuration management

## Important Notes

### Educational Purpose
- **All financial advice is for educational purposes only**
- **No licensed financial advice provided**
- **Users encouraged to consult qualified financial advisors**
- **No guarantee of strategy performance or outcomes**

### Responsible AI Practices
- **Comprehensive disclaimers in all outputs**
- **Source attribution for all research findings**
- **Conservative token limits to prevent hallucination**
- **Robust error handling and graceful degradation**
- **Educational emphasis throughout user interactions**

### Technical Limitations
- **Web search dependency**: Relies on DuckDuckGo for market data (not real-time feeds)
- **Token constraints**: 2000-token limits may truncate complex analyses
- **Model limitations**: Subject to AI model constraints and potential inaccuracies
- **No proprietary data**: Limited to publicly available information sources