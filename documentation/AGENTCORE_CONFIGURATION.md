# AgentCore CLI Configuration Guide

This guide explains how to configure the AgentCore CLI for deploying the financial advisor agent to Amazon Bedrock AgentCore Runtime.

## Overview

The AgentCore CLI configuration sets up the necessary parameters for deploying the financial advisor multiagent system to AWS. This includes specifying the entry point file, agent name, and description.

## Prerequisites

Before configuring AgentCore CLI, ensure you have:

1. **AgentCore CLI installed** - Install from AWS documentation
2. **AWS credentials configured** - Use `aws configure` or environment variables
3. **Entry point file ready** - `financial_advisor_agentcore.py` should exist and be properly configured
4. **Python environment** - Virtual environment with all dependencies installed

## Configuration Script

Use the `configure_agentcore.py` script to set up the AgentCore CLI configuration:

### Basic Usage

```bash
# Configure with default settings
python configure_agentcore.py
```

This will configure AgentCore with:
- **Entry Point**: `financial_advisor_agentcore.py`
- **Agent Name**: `financial-advisor-multiagent`
- **Description**: AI-powered financial advisory system with multi-agent orchestration for educational purposes

### Custom Configuration

```bash
# Configure with custom entry point
python configure_agentcore.py --entry-point my_custom_agent.py

# Configure with custom agent name
python configure_agentcore.py --name my-financial-advisor

# Configure with custom description
python configure_agentcore.py --description "My custom financial advisor agent"

# Configure with all custom parameters
python configure_agentcore.py \
  --entry-point my_agent.py \
  --name my-agent \
  --description "Custom agent description"
```

## Configuration Process

The configuration script performs the following steps:

### 1. Entry Point Validation
- Verifies that the entry point file exists
- Checks for required AgentCore components:
  - `BedrockAgentCoreApp` import
  - `@app.entrypoint` decorator
  - `app.run()` execution

### 2. AgentCore CLI Check
- Verifies AgentCore CLI is installed and accessible
- Displays version information

### 3. AWS Credentials Check
- Validates AWS credentials are configured
- Shows account and user information

### 4. AgentCore Configuration
- Runs `agentcore configure` command with specified parameters
- Sets up the agent for deployment

### 5. Configuration Verification
- Checks configuration status
- Displays any configuration output

## Manual Configuration

If you prefer to configure AgentCore manually, use the following command:

```bash
agentcore configure \
  --entrypoint financial_advisor_agentcore.py \
  --name financial-advisor-multiagent \
  --description "AI-powered financial advisory system with multi-agent orchestration for educational purposes"
```

## Configuration Parameters

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `--entrypoint` | `financial_advisor_agentcore.py` | Python file containing the AgentCore app |
| `--name` | `financial-advisor-multiagent` | Name for the deployed agent |
| `--description` | Educational financial advisory system | Description of the agent's purpose |

## Next Steps After Configuration

Once configuration is complete, you can:

### 1. Deploy the Agent
```bash
agentcore launch
```

### 2. Test the Deployed Agent
```bash
agentcore invoke '{"prompt": "Analyze AAPL for moderate risk investor"}'
```

### 3. Check Deployment Status
```bash
agentcore status
```

### 4. View Agent Logs
```bash
agentcore logs
```

### 5. Use Automated Deployment
```bash
python deploy_agentcore.py
```

## Troubleshooting

### Common Issues

#### AgentCore CLI Not Found
```
❌ AgentCore CLI not found or not working
```
**Solution**: Install AgentCore CLI following AWS documentation

#### AWS Credentials Not Configured
```
❌ AWS credentials not configured or invalid
```
**Solution**: Run `aws configure` or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### Entry Point File Missing
```
❌ Entry point file 'financial_advisor_agentcore.py' not found
```
**Solution**: Ensure the entry point file exists in the current directory

#### Missing AgentCore Components
```
❌ Entry point missing required components: ['BedrockAgentCoreApp', '@app.entrypoint', 'app.run()']
```
**Solution**: Verify the entry point file is properly configured with AgentCore components

### Configuration Verification

To verify your configuration is working:

1. **Check AgentCore Status**:
   ```bash
   agentcore status
   ```

2. **Validate Entry Point**:
   ```bash
   python -c "from configure_agentcore import AgentCoreConfigurator; AgentCoreConfigurator().validate_entry_point()"
   ```

3. **Test Local Server**:
   ```bash
   python financial_advisor_agentcore.py
   ```

## Security Considerations

- **AWS Credentials**: Ensure AWS credentials have appropriate permissions for AgentCore
- **Entry Point Security**: Review entry point code for security best practices
- **Network Access**: AgentCore agents may need internet access for web search functionality
- **Cost Monitoring**: Monitor AWS costs when deploying agents

## Educational Use Only

**Important**: This financial advisor system is for educational purposes only and does not provide licensed financial advice. All outputs include appropriate disclaimers and users are encouraged to consult qualified financial advisors for actual investment decisions.

## Support

For issues with:
- **AgentCore CLI**: Refer to AWS AgentCore documentation
- **AWS Credentials**: Refer to AWS CLI documentation
- **Financial Advisor Agent**: Check the agent logs and error messages
- **Configuration Script**: Review script output and error messages

## Related Files

- `configure_agentcore.py` - Configuration script
- `financial_advisor_agentcore.py` - AgentCore entry point
- `deploy_agentcore.py` - Automated deployment script
- `requirements.txt` - Python dependencies
- `AGENTCORE_DEPLOYMENT_GUIDE.md` - Complete deployment guide