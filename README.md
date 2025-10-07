# Financial Advisor Multiagent System

A comprehensive educational financial advisory platform built with the Strands Agents framework, featuring both standalone Python modules and a modern web interface for interactive financial guidance.

## Project Structure

```
├── financial_advisor_multiagent.ipynb  # Interactive Jupyter notebook system
├── financial_advisor_multiagent.py     # Standalone Python module
├── frontend/                           # React TypeScript web interface
├── backend/                            # FastAPI Python backend
├── basic-strands-information/          # Learning materials and examples
├── docker-compose.yml                  # Development environment
└── .github/workflows/                  # CI/CD pipeline
```

## Core Components

### 1. Standalone Python Module (`financial_advisor_multiagent.py`)
A production-ready Python module implementing the complete multi-agent financial advisory system:

```python
from financial_advisor_multiagent import initialize_system

# Initialize the system
advisor = initialize_system()

# Simple analysis
response = advisor.analyze("Analyze AAPL stock for moderate risk investor")

# Complete workflow
results = advisor.run_complete_analysis(
    ticker="AAPL", 
    risk_attitude="Moderate", 
    horizon="Medium-term"
)
```

### 2. Interactive Jupyter Notebook (`financial_advisor_multiagent.ipynb`)
Educational notebook demonstrating the multi-agent architecture with live examples and detailed explanations.

### 3. Web Application (Frontend + Backend)
Modern web interface providing real-time interaction with the financial advisory system through WebSocket connections.

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.12+
- Docker and Docker Compose (optional)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial-advisor-multiagent
   ```

2. **Python Environment Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install strands-agents strands-agents-tools
   pip install duckduckgo-search boto3
   ```

3. **Standalone Python Module Usage**
   ```bash
   python financial_advisor_multiagent.py
   ```

4. **Jupyter Notebook Usage**
   ```bash
   jupyter notebook financial_advisor_multiagent.ipynb
   ```

5. **Web Application Setup** (Optional)
   ```bash
   # Backend setup
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   
   # Frontend setup
   cd ../frontend
   npm install
   ```

6. **Start Web Application**
   ```bash
   # Terminal 1 - Backend
   cd backend && python main.py

   # Terminal 2 - Frontend  
   cd frontend && npm run dev
   ```

### Docker Development

```bash
# Start all services
docker-compose up

# Build and start
docker-compose up --build

# Stop services
docker-compose down
```

## Available Scripts

### Python Module
- `python financial_advisor_multiagent.py` - Run standalone system
- `jupyter notebook financial_advisor_multiagent.ipynb` - Interactive notebook
- `python -c "from financial_advisor_multiagent import initialize_system; advisor = initialize_system()"` - Import and use

### AgentCore Deployment
- `python financial_advisor_agentcore.py` - Run AgentCore-compatible version locally
- `agentcore configure --entrypoint financial_advisor_agentcore.py` - Configure for AWS deployment
- `agentcore launch` - Deploy to Amazon Bedrock AgentCore Runtime
- `agentcore invoke '{"prompt": "your query"}'` - Test deployed agent

### Web Application Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

### Web Application Backend
- `python main.py` - Start development server
- `black .` - Format code
- `isort .` - Sort imports
- `mypy .` - Type checking

## Python Module API

### Quick Start
```python
from financial_advisor_multiagent import initialize_system

# Initialize the system
advisor = initialize_system()

# Simple query analysis
response = advisor.analyze("I want to invest in TSLA with aggressive risk tolerance")
print(response)

# Complete analysis workflow
results = advisor.run_complete_analysis(
    ticker="AAPL",
    risk_attitude="Moderate",  # Conservative, Moderate, Aggressive
    horizon="Medium-term",     # Short-term, Medium-term, Long-term
    lookback_days=7
)

# Access individual components
market_analysis = results["market_analysis"]
strategies = results["strategies"] 
execution_plan = results["execution_plan"]
risk_assessment = results["risk_assessment"]
```

### Individual Agent Access
```python
# Get specific analysis components
market_report = advisor.get_market_analysis("MSFT", lookback_days=14)
strategies = advisor.get_strategies("MSFT", "Conservative", "Long-term")
execution_plan = advisor.get_execution_plan("MSFT", strategies)
risk_assessment = advisor.get_risk_assessment("MSFT", market_report, strategies, execution_plan)
```

### Available Classes and Functions
- `FinancialAdvisorOrchestrator`: Main orchestrator class
- `FinancialAdvisoryAgents`: Container for specialist agents
- `initialize_system(model)`: Initialize the complete system
- `market_intel_tool()`: Market research and analysis
- `strategy_architect_tool()`: Trading strategy generation
- `execution_planner_tool()`: Implementation planning
- `risk_assessor_tool()`: Risk assessment and mitigation

## Environment Configuration

### Python Module
The standalone Python module works out-of-the-box with default settings. For custom model configuration:

```python
# Use different model
advisor = initialize_system(model="your-model-id")
```

### Web Application
Copy `backend/.env.example` to `backend/.env` and configure:

- AWS credentials for Bedrock access (use IAM roles when possible)
- Model provider settings
- CORS origins (never use "*" in production)
- Session configuration
- **Security**: Change the default secret key for production

⚠️ **Security Warning**: Never commit real credentials to version control. See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## Architecture

### Multi-Agent System
- **Framework**: Strands Agents SDK with "Agents as Tools" pattern
- **Model**: Amazon Bedrock Claude 3.5 Sonnet
- **Orchestration**: Hierarchical coordination with specialist agents
- **Token Management**: Conservative 2000-token limits with fallback mechanisms
- **Web Search**: DuckDuckGo integration with comprehensive error handling

### Specialist Agents
- **Market Intelligence Agent**: Research and market analysis
- **Strategy Architect Agent**: Trading strategy development  
- **Execution Planner Agent**: Implementation planning
- **Risk Assessor Agent**: Risk analysis and alignment
- **Financial Coordinator Agent**: Primary orchestrator

### Deployment Options
- **Standalone Python Module**: Direct import and usage
- **Jupyter Notebook**: Interactive educational environment
- **Web Application**: React frontend + FastAPI backend
- **AgentCore Runtime**: AWS-managed serverless deployment

### Web Application (Optional)
- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: FastAPI + Python 3.12
- **Real-time Communication**: WebSockets
- **Database**: SQLite with SQLAlchemy ORM
- **Containerization**: Docker + Docker Compose

### AgentCore Deployment (AWS)
- **Runtime**: Amazon Bedrock AgentCore managed infrastructure
- **Scaling**: Automatic horizontal scaling and load balancing
- **Integration**: Native AWS service integration
- **Monitoring**: Built-in CloudWatch observability

## AgentCore Deployment

The financial advisor system can be deployed to Amazon Bedrock AgentCore Runtime for managed, scalable hosting. See the comprehensive guides:

- **[AgentCore Deployment Guide](AGENTCORE_DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[Security Guidelines](SECURITY_GUIDELINES.md)** - Security best practices and considerations

### Quick AgentCore Setup

1. **Install AgentCore dependencies**
   ```bash
   pip install bedrock-agentcore-starter-toolkit
   ```

2. **Create AgentCore wrapper** (see full guide for complete implementation)
   ```python
   from bedrock_agentcore.runtime import BedrockAgentCoreApp
   from financial_advisor_multiagent import FinancialAdvisorOrchestrator
   
   app = BedrockAgentCoreApp()
   advisor = FinancialAdvisorOrchestrator()
   
   @app.entrypoint
   def invoke(payload):
       user_query = payload.get("prompt", "")
       response = advisor.analyze(user_query)
       return {"result": response}
   
   if __name__ == "__main__":
       app.run()
   ```

3. **Deploy to AWS**
   ```bash
   agentcore configure --entrypoint financial_advisor_agentcore.py
   agentcore launch
   agentcore invoke '{"prompt": "Analyze AAPL for moderate risk investor"}'
   ```

## Security

This project implements comprehensive security measures:

- **Credential Management**: IAM roles and secure credential handling (no hardcoded credentials)
- **Input Validation**: Sanitization, type checking, and length limits (5000 characters max)
- **Error Handling**: Secure error responses without information disclosure
- **API Security**: Rate limiting recommendations and secure external API integration
- **Token Management**: Conservative 2000-token limits to prevent resource exhaustion
- **Monitoring**: Token usage monitoring and security event logging

### Security Features in AgentCore Deployment
- **Payload Validation**: Comprehensive input validation with length limits
- **Error Sanitization**: Structured error responses without sensitive information
- **Logging Integration**: Detailed security event logging through AgentCore
- **Graceful Degradation**: System continues operating with partial functionality during failures

See [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md) for detailed security information and [SECURITY_VALIDATION_CHECKLIST.md](SECURITY_VALIDATION_CHECKLIST.md) for pre-deployment security validation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Important Disclaimers

### Educational Purpose Only
- **All financial advice is for educational purposes only**
- **No licensed financial advice provided**
- **Users should consult qualified financial advisors for real investment decisions**
- **No guarantee of strategy performance or outcomes**

### Responsible AI Practices
- **Comprehensive disclaimers**: All agent outputs include educational disclaimers
- **Source attribution**: Complete source tracking for research findings
- **Conservative token limits**: 2000-token caps prevent hallucination
- **Robust error handling**: Graceful degradation when agents or tools fail
- **Web search dependency**: Relies on DuckDuckGo (not real-time market feeds)

### Technical Limitations
- **Model constraints**: Subject to AI model limitations and potential inaccuracies
- **Token constraints**: 2000-token limits may truncate complex analyses
- **Public data only**: Limited to publicly available information sources
- **Rate limiting**: Web search may be rate-limited during high usage

## License

This project is for educational purposes only. All financial advice provided is educational and should not be considered as professional financial advice.