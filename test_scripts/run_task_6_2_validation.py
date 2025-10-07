#!/usr/bin/env python3
"""
Task 6.2 HTTP Validation Test Runner

This script runs the focused HTTP validation tests for task 6.2:
- Test POST /invocations endpoint with sample financial queries
- Test GET /ping endpoint for health checks  
- Validate response formats match AgentCore expectations

Requirements addressed: 5.2, 5.3, 5.4
"""

import subprocess
import time
import sys
import signal
import os
from typing import Optional

def run_task_6_2_validation():
    """Run the focused validation tests for task 6.2."""
    server_process: Optional[subprocess.Popen] = None
    
    try:
        print("=" * 80)
        print("🧪 Task 6.2: HTTP Validation Test Suite")
        print("=" * 80)
        print("Requirements being validated:")
        print("- 5.2: Test POST /invocations endpoint with sample financial queries")
        print("- 5.3: Test GET /ping endpoint for health checks")
        print("- 5.4: Validate response formats match AgentCore expectations")
        
        # Step 1: Start the server
        print(f"\n🚀 Starting AgentCore server...")
        server_process = subprocess.Popen(
            [sys.executable, "financial_advisor_agentcore.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        print("   Waiting for server startup...")
        startup_timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < startup_timeout:
            if server_process.poll() is not None:
                stdout, stderr = server_process.communicate()
                print(f"❌ Server failed to start: {stderr}")
                return False
            
            # Test if server is ready
            try:
                import requests
                response = requests.get("http://localhost:8080/ping", timeout=2)
                if response.status_code == 200:
                    print("✅ Server started successfully!")
                    break
            except:
                pass
            
            time.sleep(1)
        else:
            print("❌ Server startup timeout")
            return False
        
        # Step 2: Run focused validation tests
        print(f"\n🔍 Running task 6.2 validation tests...")
        test_result = subprocess.run(
            [sys.executable, "test_agentcore_validation_focused.py"],
            capture_output=True,
            text=True
        )
        
        print(test_result.stdout)
        if test_result.stderr:
            print("STDERR:", test_result.stderr)
        
        success = test_result.returncode == 0
        
        if success:
            print("\n🎉 Task 6.2 validation PASSED!")
            print("✅ All HTTP validation requirements satisfied")
        else:
            print("\n❌ Task 6.2 validation FAILED!")
            print("⚠️  Some HTTP validation requirements not met")
        
        return success
        
    except KeyboardInterrupt:
        print("\n🛑 Validation interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Validation runner error: {e}")
        return False
    finally:
        # Always stop the server
        if server_process and server_process.poll() is None:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=10)
                print("✅ Server stopped gracefully")
            except subprocess.TimeoutExpired:
                server_process.kill()
                print("✅ Server terminated forcefully")

if __name__ == "__main__":
    success = run_task_6_2_validation()
    sys.exit(0 if success else 1)