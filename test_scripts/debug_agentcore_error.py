#!/usr/bin/env python3
"""
Debug AgentCore Error Response

This script helps identify the specific error occurring in the AgentCore system.
"""

import json
import time
import requests
import subprocess
import sys


def debug_agentcore_error():
    """Debug the specific error in AgentCore."""
    print("🔍 Debugging AgentCore Error Response")
    print("=" * 50)
    
    # Start server
    print("🚀 Starting AgentCore server...")
    server_process = subprocess.Popen(
        [sys.executable, "financial_advisor_agentcore.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for startup
        time.sleep(10)
        
        # Test simple query and examine error
        print("📤 Testing query and examining error response...")
        payload = {"prompt": "Test query"}
        response = requests.post(
            "http://localhost:8080/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print("\nParsed Response:")
                print(json.dumps(response_data, indent=2))
                
                if "error" in response_data:
                    print(f"\n❌ Error Details:")
                    print(f"   Error: {response_data.get('error', 'Unknown')}")
                    print(f"   Error Type: {response_data.get('error_type', 'Unknown')}")
                    print(f"   Error Class: {response_data.get('metadata', {}).get('error_class', 'Unknown')}")
                    
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
        
        # Check server stdout/stderr
        print("\n📋 Server Output:")
        stdout, stderr = server_process.communicate(timeout=1)
        if stdout:
            print("STDOUT:")
            print(stdout)
        if stderr:
            print("STDERR:")
            print(stderr)
            
    except subprocess.TimeoutExpired:
        # Server is still running, that's expected
        pass
    except Exception as e:
        print(f"Debug error: {e}")
        
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()
        print("✅ Server stopped")


if __name__ == "__main__":
    debug_agentcore_error()