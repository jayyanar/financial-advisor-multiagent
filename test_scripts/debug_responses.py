#!/usr/bin/env python3
"""
Debug script to check actual AgentCore responses
"""

import subprocess
import time
import requests
import json
from typing import Optional

def debug_responses():
    """Debug the actual responses from AgentCore server."""
    server_process: Optional[subprocess.Popen] = None
    
    try:
        print("🚀 Starting server for debugging...")
        server_process = subprocess.Popen(
            ["python", "financial_advisor_agentcore.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        for _ in range(30):
            try:
                response = requests.get("http://localhost:8080/ping", timeout=2)
                if response.status_code == 200:
                    print("✅ Server started")
                    break
            except:
                pass
            time.sleep(1)
        else:
            print("❌ Server startup failed")
            return
        
        # Test cases
        test_cases = [
            {"prompt": "Analyze AAPL stock for moderate risk investor"},
            {"prompt": ""},  # Empty prompt
            {},  # Missing prompt
        ]
        
        for i, payload in enumerate(test_cases):
            print(f"\n🔍 Test {i+1}: {payload}")
            try:
                response = requests.post(
                    "http://localhost:8080/invocations",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                print(f"Status: {response.status_code}")
                print(f"Headers: {dict(response.headers)}")
                
                try:
                    data = response.json()
                    print(f"Response keys: {list(data.keys())}")
                    print(f"Response (first 500 chars): {json.dumps(data, indent=2)[:500]}...")
                except:
                    print(f"Raw response: {response.text[:500]}...")
                    
            except Exception as e:
                print(f"Error: {e}")
        
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except:
                server_process.kill()

if __name__ == "__main__":
    debug_responses()