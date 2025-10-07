#!/usr/bin/env python3
"""
Check full response content
"""

import subprocess
import time
import requests
import json
from typing import Optional

def check_full_response():
    """Check the full response content."""
    server_process: Optional[subprocess.Popen] = None
    
    try:
        print("🚀 Starting server...")
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
                    break
            except:
                pass
            time.sleep(1)
        
        # Test with complete query
        payload = {"prompt": "Analyze AAPL stock for moderate risk investor with long-term horizon"}
        print(f"Testing with: {payload}")
        
        response = requests.post(
            "http://localhost:8080/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        print(f"Response keys: {list(data.keys())}")
        
        if "result" in data:
            result = data["result"]
            print(f"Result length: {len(result)}")
            print(f"Full result:\n{result}")
            
            # Check for educational content
            educational_terms = ["educational", "education", "disclaimer", "not financial advice", "consult", "qualified"]
            found_terms = [term for term in educational_terms if term.lower() in result.lower()]
            print(f"Educational terms found: {found_terms}")
        
        if "error" in data:
            print(f"Error: {data['error']}")
        
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except:
                server_process.kill()

if __name__ == "__main__":
    check_full_response()