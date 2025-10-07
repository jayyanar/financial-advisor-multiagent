#!/usr/bin/env python3
"""
Simple test to capture actual AgentCore responses for analysis
"""

import json
import time
import requests
import subprocess
import sys
from typing import Dict, Any


def test_actual_responses():
    """Test a few queries and capture actual responses."""
    
    # Start server
    print("🚀 Starting AgentCore server...")
    server_process = subprocess.Popen(
        [sys.executable, "financial_advisor_agentcore.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server startup
    max_wait_time = 30
    for attempt in range(max_wait_time):
        try:
            response = requests.get("http://localhost:8080/ping", timeout=5)
            if response.status_code == 200:
                print(f"✅ Server started successfully")
                break
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"⏳ Waiting for server startup... ({attempt + 1}/{max_wait_time})")
    else:
        print("❌ Server failed to start")
        return
    
    try:
        # Test queries
        test_queries = [
            "AAPL",
            "Analyze TSLA", 
            "I want investment advice",
            "",
            "   "
        ]
        
        results = {}
        
        for query in test_queries:
            print(f"\n📝 Testing: '{query}'")
            
            try:
                payload = {"prompt": query}
                response = requests.post(
                    "http://localhost:8080/invocations",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result_content = data.get("result", "")
                    print(f"✅ Response ({len(result_content)} chars): {result_content[:200]}...")
                    results[query] = {
                        "success": True,
                        "response": data,
                        "content_preview": result_content[:500]
                    }
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text}")
                    results[query] = {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                results[query] = {
                    "success": False,
                    "error": str(e)
                }
        
        # Save results
        with open("actual_responses.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to actual_responses.json")
        
    finally:
        print("🛑 Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()


if __name__ == "__main__":
    test_actual_responses()