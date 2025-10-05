# Technology Stack

## Core Framework
- **Strands Agents SDK**: Primary framework for building multi-agent AI systems
- **Python**: Main programming language (Python 3.12+)
- **Jupyter Notebooks**: Development and demonstration environment

## AI/ML Components
- **Amazon Bedrock**: Primary model provider (Claude 3.5 Sonnet, Nova Lite)
- **Anthropic Claude**: Alternative model provider support
- **OpenAI**: Supported model provider
- **Model Context Protocol (MCP)**: For tool integration

## Key Dependencies
```python
# Core Strands packages
strands-agents>=1.10.0
strands-agents-tools>=0.2.9

# AWS integration
boto3>=1.40.0
botocore>=1.40.0

# Web tools
aiohttp>=3.12.0
requests>=2.32.0
duckduckgo-search  # For market data

# Utilities
pydantic>=2.11.0
rich>=14.0.0
tenacity>=9.1.0
```

## Development Environment
- **Virtual Environment**: `.venv` directory for isolated dependencies
- **VS Code**: Preferred IDE with Python and Jupyter extensions
- **macOS**: Primary development platform

## Common Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install strands-agents strands-agents-tools

# Install additional tools
pip install duckduckgo-search boto3
```

### Running Examples
```bash
# Start Jupyter notebook
jupyter notebook

# Run specific notebook
jupyter nbconvert --execute financial_advisor_multiagent.ipynb
```

### Testing
```bash
# Run agent diagnostics
python -c "from strands import Agent; print('Strands installed successfully')"

# Test model connectivity
python -c "from strands.models import BedrockModel; print('Bedrock available')"
```

## Architecture Patterns
- **Multi-Agent Systems**: "Agents as Tools" pattern
- **State Management**: Output keys for inter-agent communication
- **Tool Integration**: MCP and native tool support
- **Error Handling**: Comprehensive try-catch with graceful degradation