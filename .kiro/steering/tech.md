# Technology Stack

## Core Framework
- **Strands Agents SDK**: Primary framework for building multi-agent AI systems
- **Python**: Main programming language (Python 3.12+)
- **Jupyter Notebooks**: Interactive development and demonstration environment
- **FastAPI**: Production web framework for backend services
- **React + TypeScript**: Frontend framework for web application

## AI/ML Components
- **Amazon Bedrock**: Primary model provider (Claude 3.5 Sonnet)
  - Model ID: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
  - Token Management: 2000-token conservative limits
  - Multi-parameter format support for different providers
- **Anthropic Claude**: Alternative model provider support
- **OpenAI**: Supported model provider
- **Model Context Protocol (MCP)**: For tool integration

## Web Application Stack

### Frontend Technologies
```typescript
// Core React + TypeScript setup
"react": "^18.3.1"
"typescript": "^5.6.2"
"vite": "^5.4.8"

// Build and development tools
"@vitejs/plugin-react": "^4.3.2"
"eslint": "^9.11.1"
"prettier": "^3.3.3"
```

### Backend Technologies
```python
# Web framework and API
fastapi>=0.115.4
uvicorn>=0.32.0
python-multipart>=0.0.12

# Database and ORM
sqlalchemy>=2.0.36
sqlite3  # Built into Python

# WebSocket support
websockets>=13.1
python-socketio>=5.11.4

# CORS and middleware
fastapi-cors>=0.0.6
```

## Key Dependencies

### Core Strands Packages
```python
# Primary agent framework
strands-agents>=1.10.0
strands-agents-tools>=0.2.9

# AWS integration
boto3>=1.40.0
botocore>=1.40.0
```

### Web Search and Data Tools
```python
# Market data and web search
duckduckgo-search>=6.3.4  # Primary web search tool
aiohttp>=3.12.0           # Async HTTP client
requests>=2.32.0          # Synchronous HTTP client
```

### Utilities and Support
```python
# Data validation and parsing
pydantic>=2.11.0

# CLI and logging
rich>=14.0.0              # Rich terminal output
tenacity>=9.1.0           # Retry mechanisms

# Environment and configuration
python-dotenv>=1.0.1      # Environment variable management
```

## Development Environment
- **Virtual Environment**: `.venv` directory for isolated dependencies
- **VS Code**: Preferred IDE with Python, TypeScript, and Jupyter extensions
- **macOS**: Primary development platform
- **Docker**: Containerization for development and production
- **Docker Compose**: Multi-service orchestration

## Architecture Patterns

### Multi-Agent System Design
- **"Agents as Tools" Pattern**: Specialist agents wrapped as tools for orchestrator
- **Hierarchical Orchestration**: Single coordinator managing multiple specialists
- **Token Management**: Conservative 2000-token limits with fallback mechanisms
- **Error Resilience**: Multiple parameter format attempts for model compatibility

### Agent Implementation Pattern
```python
# Standard agent creation pattern
def invoke_agent(agent: Agent, prompt: str, max_tokens: int = 2000) -> str:
    """Conservative token-capped agent invocation with fallbacks"""
    for kwargs in (
        {"max_output_tokens": max_tokens},               # Anthropic-style
        {"max_tokens": max_tokens},                      # OpenAI-style
        {"generation_config": {"max_output_tokens": max_tokens}},  # Generic
        {"inference_params": {"max_tokens": max_tokens}},          # Alternative
    ):
        try:
            return str(agent(prompt, **kwargs))
        except TypeError:
            continue
    return str(agent(prompt))  # Fallback without kwargs
```

### Tool Integration Pattern
```python
@tool
def specialist_agent_tool(param1: str, param2: int = 7) -> str:
    """Delegate to specialist agent with typed parameters"""
    prompt = f"Process {param1} with {param2} parameters..."
    return invoke_agent(SpecialistAgent, prompt, max_tokens=TOKEN_CAP)
```

### Web Search Integration
```python
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    """Robust web search with comprehensive error handling"""
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

## Common Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install core dependencies
pip install strands-agents strands-agents-tools
pip install duckduckgo-search boto3 fastapi uvicorn

# Install web application dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### Development Commands
```bash
# Start Jupyter notebook for prototyping
jupyter notebook

# Run specific notebook
jupyter nbconvert --execute financial_advisor_multiagent.ipynb

# Start web application (development)
make dev  # Uses docker-compose.yml

# Start backend only
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend only
cd frontend && npm run dev
```

### Production Commands
```bash
# Build and start production environment
make prod  # Uses docker-compose.prod.yml

# Build Docker images
docker build -t financial-advisor-backend ./backend
docker build -t financial-advisor-frontend ./frontend

# Run production containers
docker-compose -f docker-compose.prod.yml up -d
```

### Testing Commands
```bash
# Test agent connectivity
python -c "from strands import Agent; print('Strands installed successfully')"

# Test model connectivity
python -c "from strands.models import BedrockModel; print('Bedrock available')"

# Run backend tests
cd backend && python -m pytest test_*.py

# Test WebSocket functionality
cd backend && python test_websocket.py

# Test agent integration
cd backend && python test_agent_integration.py
```

## Configuration Management

### Environment Variables
```bash
# Backend configuration (.env)
DATABASE_URL=sqlite:///./financial_advisor.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO

# AWS Bedrock configuration (if using)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### Docker Configuration
```yaml
# docker-compose.yml (development)
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./financial_advisor.db
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
```

## Error Handling and Resilience

### Agent Invocation Resilience
- **Multiple Parameter Formats**: Attempts various model provider parameter styles
- **Graceful Fallbacks**: Falls back to basic agent calls if parameterized calls fail
- **Error Message Capture**: Comprehensive error reporting for debugging

### Web Search Resilience
- **Rate Limit Handling**: Graceful degradation when search APIs are rate-limited
- **Exception Handling**: Comprehensive exception catching for various failure modes
- **Fallback Responses**: Meaningful error messages when search fails

### Token Management
- **Conservative Limits**: 2000-token caps to prevent truncation and hallucination
- **Input Truncation**: Automatic truncation when passing data between agents
- **Efficient Prompting**: Optimized prompt engineering for maximum information density

## Performance Considerations

### Token Optimization
- **Conservative Caps**: 2000-token limits balance quality and performance
- **Efficient Prompts**: Structured prompts maximize information density
- **Strategic Truncation**: Intelligent truncation when passing data between agents

### Caching Strategies
- **Session Management**: Persistent conversation history in database
- **Agent Response Caching**: Potential for caching common queries (future enhancement)
- **Database Optimization**: SQLite with proper indexing for session retrieval

### Scalability Patterns
- **Stateless Agents**: Agents designed for horizontal scaling
- **Database Abstraction**: SQLAlchemy ORM for easy database migration
- **Container Architecture**: Docker-based deployment for easy scaling