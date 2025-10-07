#!/usr/bin/env python3
"""
Local AgentCore Server Test Script

This script starts the financial_advisor_agentcore.py locally and verifies
that the server starts correctly on localhost:8080. It provides basic
validation that the AgentCore server is running and ready to accept requests.

Requirements addressed:
- 5.1: Test local server startup
- 5.2: Verify server starts on localhost:8080

Usage:
    python test_local_agentcore_server.py

The script will:
1. Start the AgentCore server in a subprocess
2. Wait for server startup (up to 30 seconds)
3. Verify server is listening on localhost:8080
4. Test basic connectivity with ping endpoint
5. Test invocations endpoint structure
6. Provide instructions for manual testing
7. Keep server running for interactive testing
8. Gracefully shutdown on Ctrl+C

Prerequisites:
- financial_advisor_agentcore.py must be in the current directory
- All dependencies from requirements.txt must be installed
- Python 3.8+ with requests library

Exit codes:
- 0: Success (server started and tested successfully)
- 1: Failure (server failed to start or critical error)
"""

import subprocess
import time
import sys
import signal
import os
import requests
from typing import Optional

# Server configuration
SERVER_HOST = "localhost"
SERVER_PORT = 8080
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
STARTUP_TIMEOUT = 30  # seconds
PING_ENDPOINT = f"{SERVER_URL}/ping"
INVOCATIONS_ENDPOINT = f"{SERVER_URL}/invocations"

class AgentCoreServerTester:
    """Test harness for local AgentCore server startup and validation."""
    
    def __init__(self):
        self.server_process: Optional[subprocess.Popen] = None
        self.server_started = False
        
    def start_server(self) -> bool:
        """
        Start the AgentCore server in a subprocess.
        
        Returns:
            bool: True if server started successfully, False otherwise
        """
        print("=" * 60)
        print("AgentCore Local Server Test")
        print("=" * 60)
        print(f"Starting financial_advisor_agentcore.py on {SERVER_HOST}:{SERVER_PORT}")
        
        try:
            # Check if the AgentCore file exists
            if not os.path.exists("financial_advisor_agentcore.py"):
                print("❌ ERROR: financial_advisor_agentcore.py not found in current directory")
                print("   Please ensure you're running this script from the project root")
                return False
            
            # Start the server process
            print("🚀 Starting AgentCore server subprocess...")
            self.server_process = subprocess.Popen(
                [sys.executable, "financial_advisor_agentcore.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"   Server process started with PID: {self.server_process.pid}")
            return True
            
        except Exception as e:
            print(f"❌ ERROR: Failed to start server process: {e}")
            return False
    
    def wait_for_server_startup(self) -> bool:
        """
        Wait for the server to start and become ready to accept connections.
        
        Returns:
            bool: True if server is ready, False if timeout or error
        """
        print(f"⏳ Waiting for server startup (timeout: {STARTUP_TIMEOUT}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < STARTUP_TIMEOUT:
            # Check if process is still running
            if self.server_process and self.server_process.poll() is not None:
                print("❌ ERROR: Server process terminated unexpectedly")
                self._print_server_output()
                return False
            
            # Try to connect to the server
            try:
                response = requests.get(PING_ENDPOINT, timeout=2)
                if response.status_code == 200:
                    print(f"✅ Server is ready! Responded to ping in {time.time() - start_time:.1f}s")
                    self.server_started = True
                    return True
            except requests.exceptions.RequestException:
                # Server not ready yet, continue waiting
                pass
            
            # Show progress
            elapsed = time.time() - start_time
            print(f"   Waiting... ({elapsed:.1f}s elapsed)")
            time.sleep(2)
        
        print(f"❌ ERROR: Server startup timeout after {STARTUP_TIMEOUT}s")
        self._print_server_output()
        return False
    
    def test_server_endpoints(self) -> bool:
        """
        Test basic server endpoints to verify functionality.
        
        Returns:
            bool: True if endpoints respond correctly, False otherwise
        """
        print("\n" + "=" * 40)
        print("Testing Server Endpoints")
        print("=" * 40)
        
        success = True
        
        # Test ping endpoint
        print("🔍 Testing GET /ping endpoint...")
        try:
            response = requests.get(PING_ENDPOINT, timeout=5)
            if response.status_code == 200:
                print("✅ Ping endpoint working correctly")
                print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Ping endpoint returned status {response.status_code}")
                success = False
        except Exception as e:
            print(f"❌ Ping endpoint test failed: {e}")
            success = False
        
        # Test invocations endpoint structure (without full analysis)
        print("\n🔍 Testing POST /invocations endpoint structure...")
        try:
            test_payload = {"prompt": "Test connectivity"}
            response = requests.post(
                INVOCATIONS_ENDPOINT, 
                json=test_payload, 
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("✅ Invocations endpoint accepting requests")
                try:
                    response_data = response.json()
                    if "result" in response_data or "error" in response_data:
                        print("✅ Response format is correct (contains 'result' or 'error')")
                    else:
                        print("⚠️  Response format may be incorrect (missing 'result' or 'error')")
                        print(f"   Response keys: {list(response_data.keys())}")
                except Exception as e:
                    print(f"⚠️  Could not parse JSON response: {e}")
            else:
                print(f"❌ Invocations endpoint returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                success = False
                
        except Exception as e:
            print(f"❌ Invocations endpoint test failed: {e}")
            success = False
        
        return success
    
    def _print_server_output(self):
        """Print server stdout and stderr for debugging."""
        if not self.server_process:
            return
            
        print("\n" + "=" * 40)
        print("Server Output (for debugging)")
        print("=" * 40)
        
        try:
            # Get any available output
            stdout, stderr = self.server_process.communicate(timeout=1)
            
            if stdout:
                print("STDOUT:")
                print(stdout)
            
            if stderr:
                print("STDERR:")
                print(stderr)
                
        except subprocess.TimeoutExpired:
            print("Server process still running, output not available")
        except Exception as e:
            print(f"Could not retrieve server output: {e}")
    
    def stop_server(self):
        """Stop the server process gracefully."""
        if self.server_process and self.server_process.poll() is None:
            print(f"\n🛑 Stopping server process (PID: {self.server_process.pid})...")
            
            try:
                # Try graceful shutdown first
                self.server_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.server_process.wait(timeout=5)
                    print("✅ Server stopped gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    print("⚠️  Graceful shutdown timeout, forcing termination...")
                    self.server_process.kill()
                    self.server_process.wait()
                    print("✅ Server terminated")
                    
            except Exception as e:
                print(f"❌ Error stopping server: {e}")
    
    def print_usage_instructions(self):
        """Print instructions for manual testing."""
        print("\n" + "=" * 60)
        print("Manual Testing Instructions")
        print("=" * 60)
        print("The AgentCore server is now running and ready for testing.")
        print(f"Server URL: {SERVER_URL}")
        print()
        print("Available endpoints:")
        print(f"  GET  {PING_ENDPOINT}")
        print(f"  POST {INVOCATIONS_ENDPOINT}")
        print()
        print("Example curl commands for manual testing:")
        print()
        print("1. Health check:")
        print(f'   curl {PING_ENDPOINT}')
        print()
        print("2. Simple financial query:")
        print(f'   curl -X POST {INVOCATIONS_ENDPOINT} \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"prompt": "Analyze AAPL stock for moderate risk investor"}\'')
        print()
        print("3. Complete financial analysis:")
        print(f'   curl -X POST {INVOCATIONS_ENDPOINT} \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"prompt": "Provide comprehensive analysis for TSLA with aggressive risk tolerance and long-term horizon"}\'')
        print()
        print("Press Ctrl+C to stop the server when done testing.")


def main():
    """Main test execution function."""
    tester = AgentCoreServerTester()
    
    # Set up signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\n\n🛑 Received interrupt signal, shutting down...")
        tester.stop_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Step 1: Start the server
        if not tester.start_server():
            print("❌ Failed to start server")
            return 1
        
        # Step 2: Wait for server to be ready
        if not tester.wait_for_server_startup():
            print("❌ Server failed to start properly")
            return 1
        
        # Step 3: Test basic endpoints
        if not tester.test_server_endpoints():
            print("⚠️  Some endpoint tests failed, but server is running")
        
        # Step 4: Provide usage instructions
        tester.print_usage_instructions()
        
        # Step 5: Keep server running for manual testing
        print("\n" + "=" * 60)
        print("Server Running - Ready for Testing")
        print("=" * 60)
        print("The server will continue running for manual testing.")
        print("Use the curl commands above to test functionality.")
        print("Press Ctrl+C when done to stop the server.")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if server process is still alive
            if tester.server_process and tester.server_process.poll() is not None:
                print("\n❌ Server process terminated unexpectedly")
                tester._print_server_output()
                return 1
    
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
        return 0
    
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        return 1
    
    finally:
        tester.stop_server()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)