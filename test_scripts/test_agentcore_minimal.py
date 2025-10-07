#!/usr/bin/env python3
"""
Minimal AgentCore Test

This script creates a minimal AgentCore application to test basic functionality
without the complex financial advisor system.
"""

from datetime import datetime, timezone
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Initialize AgentCore app
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Simple test entry point."""
    try:
        prompt = payload.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided"}
        
        # Simple response without using Strands agents
        response = f"Received prompt: {prompt}. This is a test response from AgentCore."
        
        return {
            "result": response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "minimal-test"
        }
        
    except Exception as e:
        return {
            "error": f"Error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

if __name__ == "__main__":
    print("Starting minimal AgentCore test...")
    app.run()