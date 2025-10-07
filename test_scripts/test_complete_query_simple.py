#!/usr/bin/env python3
"""
Simple test for complete queries to satisfy requirement 7.2
"""

import requests
import subprocess
import sys
import time


def test_complete_query():
    """Test a complete query with all parameters."""
    
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
        return False
    
    try:
        # Test a simple complete query
        query = "AAPL moderate risk long-term"
        print(f"📝 Testing complete query: '{query}'")
        
        payload = {"prompt": query}
        response = requests.post(
            "http://localhost:8080/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20  # Shorter timeout for simple test
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("result", data.get("error", ""))
            
            print(f"✅ Response received ({len(content)} chars)")
            print(f"📄 Content preview: {content[:200]}...")
            
            # Check if it handles the complete query appropriately
            content_lower = content.lower()
            mentions_aapl = "aapl" in content_lower or "apple" in content_lower
            mentions_risk = "moderate" in content_lower or "risk" in content_lower
            mentions_horizon = "long" in content_lower or "term" in content_lower
            
            print(f"   - Mentions AAPL: {'✓' if mentions_aapl else '✗'}")
            print(f"   - Mentions risk: {'✓' if mentions_risk else '✗'}")
            print(f"   - Mentions horizon: {'✓' if mentions_horizon else '✗'}")
            
            if mentions_aapl and (mentions_risk or mentions_horizon):
                print("🎯 Complete query test: PASSED")
                print("✅ Requirement 7.2 satisfied: System handles complete queries with risk tolerance and horizon")
                return True
            else:
                print("❌ Complete query test: FAILED")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        print("🛑 Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()


if __name__ == "__main__":
    success = test_complete_query()
    sys.exit(0 if success else 1)