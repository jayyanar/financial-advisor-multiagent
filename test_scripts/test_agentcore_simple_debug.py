#!/usr/bin/env python3
"""
Simple AgentCore Debug Test

This test helps debug the AgentCore integration by testing basic functionality
and identifying any configuration or dependency issues.
"""

import json
import time
import requests
import subprocess
import sys
from datetime import datetime


def test_agentcore_basic():
    """Test basic AgentCore functionality."""
    print("🔍 Testing AgentCore Basic Functionality")
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
        
        # Test ping endpoint
        print("📡 Testing ping endpoint...")
        try:
            ping_response = requests.get("http://localhost:8080/ping", timeout=10)
            print(f"   Ping Status: {ping_response.status_code}")
            if ping_response.status_code == 200:
                print("   ✅ Ping successful")
            else:
                print(f"   ❌ Ping failed: {ping_response.text}")
        except Exception as e:
            print(f"   ❌ Ping error: {e}")
        
        # Test simple invocation
        print("📤 Testing simple invocation...")
        try:
            payload = {"prompt": "Hello, test query"}
            response = requests.post(
                "http://localhost:8080/invocations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"   Invocation Status: {response.status_code}")
            print(f"   Response Length: {len(response.text)} characters")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f"   ✅ JSON Response received")
                    print(f"   Response Keys: {list(response_data.keys())}")
                    
                    if "result" in response_data:
                        result_length = len(response_data["result"])
                        print(f"   Result Length: {result_length} characters")
                        if result_length > 0:
                            print(f"   Result Sample: {response_data['result'][:200]}...")
                        else:
                            print("   ⚠️  Empty result field")
                    else:
                        print("   ⚠️  No 'result' field in response")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response: {response.text[:200]}...")
            else:
                print(f"   ❌ Invocation failed: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Invocation error: {e}")
        
        # Test financial query
        print("📊 Testing financial query...")
        try:
            payload = {"prompt": "Analyze AAPL stock for moderate risk investor"}
            response = requests.post(
                "http://localhost:8080/invocations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            print(f"   Financial Query Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "result" in response_data and response_data["result"]:
                        print(f"   ✅ Financial analysis received ({len(response_data['result'])} chars)")
                        
                        # Check for workflow indicators
                        result_lower = response_data["result"].lower()
                        indicators = {
                            "market": "market" in result_lower,
                            "strategy": "strategy" in result_lower,
                            "execution": "execution" in result_lower,
                            "risk": "risk" in result_lower,
                            "educational": "educational" in result_lower
                        }
                        
                        print(f"   Workflow Indicators: {indicators}")
                        
                    else:
                        print("   ⚠️  Empty or missing result in financial query")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON in financial response")
            else:
                print(f"   ❌ Financial query failed: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Financial query error: {e}")
            
    finally:
        # Stop server
        print("🛑 Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()
        print("✅ Server stopped")


if __name__ == "__main__":
    test_agentcore_basic()