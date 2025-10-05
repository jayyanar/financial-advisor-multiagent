# Project Structure

## Root Directory Layout
```
├── .kiro/                          # Kiro IDE configuration
│   ├── specs/                      # Feature specifications
│   │   └── financial-advisor-multiagent/
│   │       ├── requirements.md     # User stories and acceptance criteria
│   │       ├── design.md          # Architecture and component design
│   │       └── tasks.md           # Implementation checklist
│   └── steering/                   # AI assistant guidance (this folder)
├── .venv/                          # Python virtual environment
├── .vscode/                        # VS Code workspace settings
├── basic-strands-information/      # Learning materials and examples
│   ├── basic_info.ipynb          # Strands SDK setup and basic examples
│   └── fin_refactor.md            # Financial advisor refactoring notes
├── nba-stastics-dashboard/         # Future NBA analytics project (empty)
├── financial_advisor_multiagent.ipynb        # Main financial advisor system
└── financial_advisor_multiagent_backup.ipynb # Backup of main system
```

## Key Files and Their Purpose

### Main Implementation
- **`financial_advisor_multiagent.ipynb`**: Complete multi-agent financial advisory system
  - Financial Coordinator Agent (orchestrator)
  - Data Analyst Agent (market research)
  - Trading Analyst Agent (strategy development)
  - Execution Analyst Agent (implementation planning)
  - Risk Analyst Agent (risk assessment)
  - Helper functions and example usage

### Learning Materials
- **`basic-strands-information/basic_info.ipynb`**: Strands SDK introduction
  - Installation instructions
  - Basic agent creation
  - Tool integration examples
  - Model provider setup

### Specifications
- **`.kiro/specs/financial-advisor-multiagent/`**: Complete feature documentation
  - Requirements with user stories
  - System architecture and design
  - Implementation task tracking

## Naming Conventions

### Agents
- Use descriptive names ending in `_agent`: `data_analyst_agent`, `trading_analyst_agent`
- Output keys follow pattern: `{purpose}_output` (e.g., `market_data_analysis_output`)

### Files
- Jupyter notebooks: `snake_case.ipynb`
- Documentation: `kebab-case.md` for specs, `snake_case.md` for general docs
- Use descriptive names that indicate purpose

### Variables and Functions
- Python snake_case for functions: `query_agent()`, `print_response()`
- Constants in UPPER_CASE: `FINANCIAL_COORDINATOR_PROMPT`
- Agent instances in snake_case: `financial_coordinator`

## Code Organization Patterns

### Agent Structure
```python
# 1. Define prompt constant
AGENT_PROMPT = """..."""

# 2. Create agent instance
agent = LlmAgent(
    model=MODEL,
    name="agent_name",
    description="Agent purpose",
    instruction=AGENT_PROMPT,
    output_key="unique_output_key",
    tools=[relevant_tools]
)
```

### Multi-Agent Coordination
- Primary coordinator agent with sub-agents as tools
- State management through output keys
- Clear separation of concerns between agents
- Comprehensive error handling at each level

## Development Workflow
1. Start with specifications in `.kiro/specs/`
2. Implement in Jupyter notebooks for rapid prototyping
3. Use helper functions for common operations
4. Test with example scenarios
5. Document with markdown cells in notebooks