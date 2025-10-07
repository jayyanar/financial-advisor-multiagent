# Project Structure

## Root Directory Layout
```
├── .kiro/                          # Kiro IDE configuration
│   ├── specs/                      # Feature specifications
│   │   ├── financial-advisor-multiagent/  # Notebook system specs
│   │   │   ├── requirements.md     # User stories and acceptance criteria
│   │   │   ├── design.md          # Architecture and component design
│   │   │   └── tasks.md           # Implementation checklist
│   │   └── financial-advisor-ui/   # Web application specs
│   │       ├── requirements.md     # Web UI requirements
│   │       ├── design.md          # Web application design
│   │       └── tasks.md           # Web implementation tasks
│   └── steering/                   # AI assistant guidance (this folder)
├── .venv/                          # Python virtual environment
├── .vscode/                        # VS Code workspace settings
├── backend/                        # FastAPI backend application
│   ├── routers/                    # API route handlers
│   │   ├── advisory.py            # Financial advisory endpoints
│   │   ├── sessions.py            # Session management endpoints
│   │   └── websocket.py           # WebSocket connection handler
│   ├── __pycache__/               # Python bytecode cache
│   ├── .env.example               # Environment configuration template
│   ├── agent_manager.py           # Centralized agent orchestration
│   ├── config.py                  # Application configuration
│   ├── database.py                # Database connection and setup
│   ├── Dockerfile                 # Backend container configuration
│   ├── financial_advisor.db       # SQLite database file
│   ├── main.py                    # FastAPI application entry point
│   ├── middleware.py              # Custom middleware components
│   ├── models.py                  # SQLAlchemy database models
│   ├── pyproject.toml             # Python project configuration
│   ├── requirements.txt           # Python dependencies
│   ├── session_manager.py         # Session state management
│   ├── ticker_service.py          # Stock ticker validation service
│   ├── websocket_manager.py       # WebSocket connection management
│   └── test_*.py                  # Test files for various components
├── frontend/                       # React TypeScript frontend
│   ├── src/                       # Source code
│   │   ├── App.tsx                # Main application component
│   │   ├── App.css                # Application styles
│   │   ├── index.css              # Global styles
│   │   └── main.tsx               # Application entry point
│   ├── .eslintrc.cjs              # ESLint configuration
│   ├── .prettierrc                # Prettier configuration
│   ├── Dockerfile                 # Frontend container configuration
│   ├── Dockerfile.prod            # Production frontend container
│   ├── index.html                 # HTML template
│   ├── nginx.conf                 # Nginx configuration for production
│   ├── package.json               # Node.js dependencies and scripts
│   ├── tsconfig.json              # TypeScript configuration
│   ├── tsconfig.node.json         # TypeScript Node.js configuration
│   └── vite.config.ts             # Vite build configuration
├── basic-strands-information/      # Learning materials and examples
│   ├── basic_info.ipynb           # Strands SDK setup and basic examples
│   └── fin_refactor.md            # Financial advisor refactoring notes
├── docker-compose.yml              # Development environment orchestration
├── docker-compose.prod.yml         # Production environment orchestration
├── financial_advisor_multiagent.ipynb        # Main financial advisor system
├── Makefile                        # Build and deployment commands
├── README.md                       # Project documentation and quick start
├── API_REFERENCE.md                # Python module API documentation
├── API_DOCUMENTATION.md            # Web API endpoint documentation
├── DEPLOYMENT_CHECKLIST.md         # Production deployment guide
├── FINANCIAL_ADVISOR_DOCUMENTATION.md # Comprehensive system documentation
└── SECURITY.md                     # Security considerations and guidelines
```

## Key Files and Their Purpose

### Core Implementation Files

#### Multi-Agent System Core
- **`financial_advisor_multiagent.py`**: Production-ready Python module
  - **FinancialAdvisorOrchestrator**: Main orchestrator class with complete API
  - **FinancialAdvisoryAgents**: Container class for all specialist agents
  - **Agent Tools**: market_intel_tool, strategy_architect_tool, execution_planner_tool, risk_assessor_tool
  - **Utility Functions**: invoke_agent, initialize_system, websearch
  - **Error Handling**: Robust fallback mechanisms and exception handling
  - **Token Management**: Conservative 2000-token limits with multiple parameter format support

- **`financial_advisor_multiagent.ipynb`**: Interactive educational notebook
  - **AdvisoryOrchestratorAgent**: Primary coordinator managing all specialist agents
  - **MarketIntelligenceAgent**: Market research and analysis specialist
  - **StrategyArchitectAgent**: Trading strategy development specialist
  - **ExecutionPlannerAgent**: Implementation planning specialist
  - **RiskAssessorAgent**: Risk analysis and alignment specialist
  - **Live Examples**: Interactive demonstrations and educational content
  - **Web Search Integration**: DuckDuckGo search with comprehensive error handling

#### Web Application Backend
- **`backend/main.py`**: FastAPI application entry point with CORS and middleware setup
- **`backend/agent_manager.py`**: Centralized agent orchestration and management
- **`backend/session_manager.py`**: User session state management and persistence
- **`backend/websocket_manager.py`**: Real-time WebSocket connection management
- **`backend/database.py`**: SQLAlchemy database setup and connection management
- **`backend/models.py`**: Database models for sessions and conversation history
- **`backend/config.py`**: Application configuration and environment variable management

#### API Routers
- **`backend/routers/advisory.py`**: Financial advisory service endpoints
- **`backend/routers/sessions.py`**: Session management API endpoints
- **`backend/routers/websocket.py`**: WebSocket connection handling

#### Web Application Frontend
- **`frontend/src/App.tsx`**: Main React application component with WebSocket integration
- **`frontend/src/main.tsx`**: Application entry point and React DOM rendering
- **`frontend/package.json`**: Node.js dependencies and build scripts
- **`frontend/vite.config.ts`**: Vite build tool configuration

### Documentation Files
- **`FINANCIAL_ADVISOR_DOCUMENTATION.md`**: Comprehensive system architecture and implementation guide
- **`API_DOCUMENTATION.md`**: Complete API endpoint documentation with examples
- **`DEPLOYMENT_CHECKLIST.md`**: Production deployment guide and checklist
- **`SECURITY.md`**: Security considerations and best practices
- **`README.md`**: Project overview and quick start guide

### Configuration Files
- **`docker-compose.yml`**: Development environment with hot reload
- **`docker-compose.prod.yml`**: Production environment with optimized builds
- **`Makefile`**: Simplified build and deployment commands
- **`backend/.env.example`**: Environment variable template
- **`backend/requirements.txt`**: Python dependency specifications
- **`frontend/package.json`**: Node.js dependency specifications

### Learning Materials
- **`basic-strands-information/basic_info.ipynb`**: Strands SDK introduction
  - Installation instructions
  - Basic agent creation
  - Tool integration examples
  - Model provider setup
- **`basic-strands-information/fin_refactor.md`**: Financial advisor refactoring notes

### Specifications
- **`.kiro/specs/financial-advisor-multiagent/`**: Notebook system documentation
  - Requirements with user stories and acceptance criteria
  - System architecture and component design
  - Implementation task tracking
- **`.kiro/specs/financial-advisor-ui/`**: Web application documentation
  - Web UI requirements and user stories
  - Frontend/backend architecture design
  - Web implementation task tracking

## Naming Conventions

### Agents (Notebook System)
- **Professional Names**: `MarketIntelligenceAgent`, `StrategyArchitectAgent`, `ExecutionPlannerAgent`
- **Tool Wrappers**: `market_intel_tool`, `strategy_architect_tool`, `execution_planner_tool`
- **Orchestrator**: `AdvisoryOrchestratorAgent` (primary coordinator)

### Files and Directories
- **Jupyter notebooks**: `snake_case.ipynb`
- **Python modules**: `snake_case.py`
- **Documentation**: `UPPER_CASE.md` for project docs, `kebab-case.md` for specs
- **Frontend components**: `PascalCase.tsx`
- **Configuration files**: `lowercase.extension`

### Variables and Functions
- **Python snake_case**: `invoke_agent()`, `websearch()`, `market_intel_tool()`
- **Constants**: `UPPER_CASE` - `TOKEN_CAP`, `FINANCIAL_COORDINATOR_SYSTEM_PROMPT`
- **Agent instances**: `snake_case` - `AdvisoryOrchestratorAgent`
- **TypeScript camelCase**: `sessionId`, `websocketConnection`, `handleMessage`

### Database Models
```python
# SQLAlchemy model naming
class UserSession(Base):
    __tablename__ = "user_sessions"
    
class ConversationHistory(Base):
    __tablename__ = "conversation_history"
```

## Code Organization Patterns

### Agent Structure (Notebook)
```python
# 1. Define system prompt
AGENT_SYSTEM_PROMPT = """You are a specialized [Role] Agent..."""

# 2. Create agent instance
SpecialistAgent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt=AGENT_SYSTEM_PROMPT,
    tools=[websearch],
)

# 3. Create tool wrapper
@tool
def specialist_tool(param: str) -> str:
    """Delegate to specialist agent with typed parameters"""
    prompt = f"Process {param}..."
    return invoke_agent(SpecialistAgent, prompt, max_tokens=TOKEN_CAP)
```

### Token Management Pattern
```python
TOKEN_CAP = 2000

def invoke_agent(agent: Agent, prompt: str, max_tokens: int = TOKEN_CAP) -> str:
    """Conservative token-capped invocation with multiple fallback attempts"""
    for kwargs in (
        {"max_output_tokens": max_tokens},               # Anthropic-style
        {"max_tokens": max_tokens},                      # OpenAI-style
        {"generation_config": {"max_output_tokens": max_tokens}},
        {"inference_params": {"max_tokens": max_tokens}},
    ):
        try:
            return str(agent(prompt, **kwargs))
        except TypeError:
            continue
    return str(agent(prompt))  # Final fallback
```

### Web Application Structure (Backend)
```python
# FastAPI router pattern
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1", tags=["advisory"])

@router.post("/analyze")
async def analyze_stock(request: AnalysisRequest, db: Session = Depends(get_db)):
    """Financial analysis endpoint with session management"""
    # Implementation with error handling
```

### WebSocket Management Pattern
```python
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Manage WebSocket connections with session tracking"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    async def send_message(self, session_id: str, message: dict):
        """Send structured messages to specific sessions"""
        # Implementation with error handling
```

### Frontend Component Structure
```typescript
// React component with WebSocket integration
interface AppProps {
  sessionId: string;
}

const App: React.FC<AppProps> = ({ sessionId }) => {
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  
  // WebSocket connection management
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    // Connection handling
  }, [sessionId]);
  
  return (
    // Component JSX
  );
};
```

## Multi-Agent Coordination Patterns

### Hierarchical Orchestration
- **Primary Coordinator**: `AdvisoryOrchestratorAgent` manages all specialist interactions
- **Specialist Agents**: Each handles specific domain expertise (market, strategy, execution, risk)
- **Tool Delegation**: Specialists wrapped as tools for the orchestrator
- **Token Management**: Conservative limits with intelligent truncation between agents

### State Management
- **Session Persistence**: Database storage of conversation history and context
- **WebSocket State**: Real-time connection state management
- **Agent Context**: Passing relevant context between specialist agents
- **Error Recovery**: Graceful degradation when agents or tools fail

## Development Workflow

### Notebook Development
1. **Prototype in Jupyter**: Rapid agent development and testing
2. **Test Individual Agents**: Validate each specialist agent independently
3. **Integration Testing**: Test full orchestration workflow
4. **Documentation**: Document agent behaviors and limitations

### Web Application Development
1. **Backend First**: Implement API endpoints and database models
2. **Agent Integration**: Connect notebook agents to web backend
3. **Frontend Development**: Build React components with WebSocket integration
4. **End-to-End Testing**: Validate complete user workflows

### Production Deployment
1. **Environment Configuration**: Set up production environment variables
2. **Docker Build**: Create optimized production containers
3. **Database Migration**: Set up production database schema
4. **Health Checks**: Implement monitoring and health check endpoints
5. **Security Review**: Validate security configurations and practices

## Testing Strategy

### Unit Testing
- **Agent Testing**: Individual agent response validation
- **API Testing**: Endpoint functionality and error handling
- **Database Testing**: Model operations and data integrity
- **WebSocket Testing**: Connection management and message handling

### Integration Testing
- **Multi-Agent Workflows**: End-to-end agent orchestration
- **API Integration**: Frontend-backend communication
- **Database Integration**: Session management and persistence
- **Error Handling**: Graceful degradation scenarios

### Performance Testing
- **Token Limits**: Validate 2000-token caps and truncation
- **WebSocket Load**: Connection management under load
- **Database Performance**: Query optimization and indexing
- **Agent Response Times**: Latency measurement and optimization