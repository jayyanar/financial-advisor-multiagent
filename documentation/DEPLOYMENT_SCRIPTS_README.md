# AgentCore Deployment Scripts

This directory contains deployment scripts for deploying the financial advisor multiagent system to Amazon Bedrock AgentCore Runtime.

## Scripts Overview

### 1. `deploy_agentcore.py` (Primary Script)
Comprehensive Python deployment script with full error handling, validation, and status reporting.

**Features:**
- Prerequisites checking (CLI, AWS credentials, files)
- AgentCore configuration with proper parameters
- Automated deployment to AWS
- Post-deployment validation with test queries
- Comprehensive error handling and cleanup
- Status reporting and next steps guidance

### 2. `deploy.sh` (Shell Wrapper)
Simple shell script wrapper that ensures proper environment setup and calls the Python script.

**Features:**
- Virtual environment activation
- Basic prerequisite checks
- Simplified command-line interface

## Prerequisites

Before running the deployment scripts, ensure you have:

1. **AgentCore CLI installed and configured**
   ```bash
   # Install AgentCore CLI (follow AWS documentation)
   pip install bedrock-agentcore-cli
   ```

2. **AWS credentials configured**
   ```bash
   aws configure
   # OR set environment variables:
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Required files present:**
   - `financial_advisor_agentcore.py` (AgentCore entry point)
   - `requirements.txt` (Python dependencies)
   - Virtual environment with dependencies installed

4. **Python virtual environment activated**
   ```bash
   source .venv/bin/activate
   ```

## Usage

### Option 1: Python Script (Recommended)

```bash
# Basic deployment with default settings
python deploy_agentcore.py

# Deploy with custom entry point
python deploy_agentcore.py --entry-point my_custom_agent.py

# Validate existing deployment only
python deploy_agentcore.py --validate-only

# Show help
python deploy_agentcore.py --help
```

### Option 2: Shell Script (Simplified)

```bash
# Basic deployment
./deploy.sh

# Pass arguments to Python script
./deploy.sh --validate-only
./deploy.sh --entry-point custom_agent.py
```

## Deployment Process

The deployment script follows these steps:

### 1. Prerequisites Check ✅
- Verifies AgentCore CLI is installed and working
- Checks AWS credentials are configured
- Validates required files exist
- Confirms entry point file is present

### 2. AgentCore Configuration ⚙️
- Runs `agentcore configure` with proper parameters
- Sets entry point to `financial_advisor_agentcore.py`
- Configures agent name and description
- Handles configuration errors gracefully

### 3. Deployment Launch 🚀
- Executes `agentcore launch` to deploy to AWS
- Monitors deployment progress
- Handles timeout and error scenarios
- Provides detailed error messages on failure

### 4. Validation Testing 🧪
- Waits for deployment to stabilize
- Runs test query using `agentcore invoke`
- Validates response format and content
- Confirms agent is working correctly

### 5. Status Reporting 📋
- Shows final deployment status
- Provides next steps and usage instructions
- Offers troubleshooting guidance

## Error Handling

The deployment script includes comprehensive error handling:

### Common Error Scenarios
1. **AgentCore CLI not found**: Install AgentCore CLI
2. **AWS credentials invalid**: Configure AWS credentials
3. **Entry point file missing**: Ensure `financial_advisor_agentcore.py` exists
4. **Deployment timeout**: Check AWS service status
5. **Validation failure**: Review agent logs and configuration

### Automatic Cleanup
- Failed deployments trigger automatic cleanup
- Partial resources are removed to prevent conflicts
- Clean state maintained for retry attempts

### Error Recovery
```bash
# Check deployment status
agentcore status

# View deployment logs
agentcore logs

# Clean up failed deployment
agentcore cleanup

# Retry deployment
python deploy_agentcore.py
```

## Post-Deployment

After successful deployment:

### Testing Your Agent
```bash
# Test with simple query
agentcore invoke '{"prompt": "Analyze AAPL stock for moderate risk investor"}'

# Test with complex query
agentcore invoke '{"prompt": "Provide comprehensive analysis of TSLA with aggressive risk tolerance and long-term horizon"}'
```

### Monitoring
```bash
# Check agent status
agentcore status

# View recent logs
agentcore logs --tail 100

# Monitor performance
agentcore metrics
```

### Management
```bash
# Update agent
agentcore update

# Scale agent
agentcore scale --instances 3

# Stop agent
agentcore stop

# Delete deployment
agentcore delete
```

## Troubleshooting

### Common Issues

1. **"AgentCore CLI not found"**
   - Install AgentCore CLI: `pip install bedrock-agentcore-cli`
   - Verify installation: `agentcore --version`

2. **"AWS credentials not configured"**
   - Run `aws configure` to set up credentials
   - Or set environment variables for AWS access

3. **"Entry point file not found"**
   - Ensure `financial_advisor_agentcore.py` exists
   - Check file permissions and path

4. **"Deployment timeout"**
   - Check AWS service status
   - Verify network connectivity
   - Try deployment during off-peak hours

5. **"Validation failed"**
   - Check agent logs: `agentcore logs`
   - Verify dependencies in requirements.txt
   - Test locally first: `python financial_advisor_agentcore.py`

### Debug Mode
```bash
# Run with verbose output
python deploy_agentcore.py --verbose

# Check detailed status
agentcore status --detailed

# Export deployment logs
agentcore logs --export deployment.log
```

## Security Considerations

- AWS credentials are never stored in the scripts
- All communication uses AWS IAM roles and policies
- Agent code is deployed securely through AgentCore
- No sensitive data is logged or exposed

## Support

For issues with:
- **AgentCore CLI**: Refer to AWS AgentCore documentation
- **Deployment scripts**: Check error messages and logs
- **Agent functionality**: Test locally first, then check AgentCore logs
- **AWS permissions**: Verify IAM roles and policies

## Files Created

The deployment process creates/modifies:
- AgentCore configuration files
- AWS resources (managed by AgentCore)
- Deployment logs and status files

All resources are managed by AgentCore and can be cleaned up using `agentcore cleanup`.