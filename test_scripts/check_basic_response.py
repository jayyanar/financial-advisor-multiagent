#!/usr/bin/env python3
"""
Check basic response content for educational disclaimer
"""

import subprocess
import time
import requests
import json
from typing import Optional

def check_basic_response():
    """Check the basic response content."""
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
        
        # Test with basic query (incomplete)
        payload = {"prompt": "Analyze AAPL stock for moderate risk investor"}
        print(f"Testing with: {payload}")
        
        response = requests.post(
            "http://localhost:8080/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        print(f"Response keys: {list(data.keys())}")
        
        if "result" in data:
            result = data["result"]
            print(f"Result length: {len(result)}")
            print(f"Full result:\n{result}")
            
            # Check for educational content
            educational_terms = ["educational", "education", "disclaimer", "not financial advice", 
                               "consult", "qualified", "for educational purposes", "not licensed"]
            found_terms = [term for term in educational_terms if term.lower() in result.lower()]
            print(f"Educational terms found: {found_terms}")
            
            # Check metadata
            if "metadata" in data:
                metadata = data["metadata"]
                print(f"Metadata keys: {list(metadata.keys())}")
                if "educational_disclaimer" in metadata:
                    print(f"Educational disclaimer in metadata: {metadata['educational_disclaimer']}")
                if "disclaimer" in metadata:
                    print(f"Disclaimer in metadata: {metadata['disclaimer']}")
        
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
    check_basic_response()