#!/usr/bin/env python3
"""
AgentCore HTTP Request Test Suite

This script provides comprehensive HTTP testing for the AgentCore financial advisor
system. It tests both the /invocations endpoint with sample financial queries and
the /ping endpoint for health checks, validating that response formats match
AgentCore expectations.

Requirements addressed:
- 5.2: Test POST /invocations endpoint with sample financial queries
- 5.3: Test GET /ping endpoint for health checks  
- 5.4: Validate response formats match AgentCore expectations

Usage:
    python test_agentcore_http_requests.py
    python test_agentcore_http_requests.py --server http://localhost:8080
    python test_agentcore_http_requests.py --quick  # Run only basic tests
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


class AgentCoreHTTPTester:
    """Comprehensive HTTP test suite for AgentCore financial advisor system."""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url.rstrip('/')
        self.invocations_url = f"{self.server_url}/invocations"
        self.ping_url = f"{self.server_url}/ping"
        self.timeout = 30  # seconds for financial analysis requests
        self.quick_timeout = 10  # seconds for quick tests
        
        # Test results tracking
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result for summary reporting."""
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if passed:
            self.passed_tests += 1
            print(f"✅ {test_name}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}")
        
        if details:
            print(f"   {details}")
    
    def test_ping_endpoint(self) -> bool:
        """
        Test GET /ping endpoint for health checks.
        
        Validates:
        - Endpoint returns 200 status code
        - Response is received within timeout
        - Basic connectivity to AgentCore server
        
        Returns:
            bool: True if health check passes, False otherwise
        """
        print(f"\n🔍 Testing Health Check Endpoint: GET {self.ping_url}")
        
        try:
            start_time = time.time()
            response = requests.get(self.ping_url, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test_result(
                    "Health Check Endpoint",
                    True,
                    f"Status: {response.status_code}, Response time: {response_time:.2f}s"
                )
                return True
            else:
                self.log_test_result(
                    "Health Check Endpoint",
                    False,
                    f"Unexpected status code: {response.status_code}"
                )
                return False
                
        except requests.exceptions.Timeout:
            self.log_test_result(
                "Health Check Endpoint",
                False,
                "Request timeout - server not responding"
            )
            return False
        except requests.exceptions.ConnectionError:
            self.log_test_result(
                "Health Check Endpoint",
                False,
                "Connection error - server not reachable"
            )
            return False
        except Exception as e:
            self.log_test_result(
                "Health Check Endpoint",
                False,
                f"Unexpected error: {e}"
            )
            return False
    
    def validate_agentcore_response_format(self, response_data: Dict[str, Any], test_name: str) -> bool:
        """
        Validate that response format matches AgentCore expectations.
        
        Expected AgentCore response format for success:
        {
            "result": "string",
            "timestamp": "ISO timestamp",
            "system": "financial-advisor-multiagent",
            "metadata": {...}
        }
        
        Expected AgentCore response format for errors:
        {
            "error": "string",
            "error_type": "string",
            "timestamp": "ISO timestamp",
            "system": "financial-advisor-multiagent",
            "metadata": {...}
        }
        
        Args:
            response_data: Response JSON data to validate
            test_name: Name of test for logging
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        # Check if this is an error response or success response
        is_error_response = "error" in response_data
        
        if is_error_response:
            required_fields = ["error", "timestamp", "system"]
        else:
            required_fields = ["result", "timestamp", "system"]
        
        # Check for required fields
        missing_fields = [field for field in required_fields if field not in response_data]
        if missing_fields:
            self.log_test_result(
                f"{test_name} - Response Format",
                False,
                f"Missing required fields: {missing_fields}"
            )
            return False
        
        # Validate field types and values
        if is_error_response:
            if not isinstance(response_data.get("error"), str):
                self.log_test_result(
                    f"{test_name} - Response Format",
                    False,
                    "Field 'error' must be a string"
                )
                return False
        else:
            if not isinstance(response_data.get("result"), str):
                self.log_test_result(
                    f"{test_name} - Response Format",
                    False,
                    "Field 'result' must be a string"
                )
                return False
        
        if response_data.get("system") != "financial-advisor-multiagent":
            self.log_test_result(
                f"{test_name} - Response Format",
                False,
                f"Field 'system' should be 'financial-advisor-multiagent', got: {response_data.get('system')}"
            )
            return False
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(response_data.get("timestamp", "").replace('Z', '+00:00'))
        except ValueError:
            self.log_test_result(
                f"{test_name} - Response Format",
                False,
                "Field 'timestamp' is not a valid ISO timestamp"
            )
            return False
        
        # Check for metadata (optional but expected)
        if "metadata" in response_data:
            metadata = response_data["metadata"]
            if not isinstance(metadata, dict):
                self.log_test_result(
                    f"{test_name} - Response Format",
                    False,
                    "Field 'metadata' must be a dictionary"
                )
                return False
        
        self.log_test_result(
            f"{test_name} - Response Format",
            True,
            "All required fields present with correct types"
        )
        return True
    
    def test_invocations_endpoint(self, payload: Dict[str, Any], test_name: str, timeout: int = None) -> bool:
        """
        Test POST /invocations endpoint with a specific payload.
        
        Args:
            payload: Request payload to send
            test_name: Name of test for logging
            timeout: Request timeout (uses default if None)
            
        Returns:
            bool: True if test passes, False otherwise
        """
        if timeout is None:
            timeout = self.timeout
        
        print(f"\n🔍 Testing Invocations Endpoint: {test_name}")
        print(f"   POST {self.invocations_url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        try:
            start_time = time.time()
            response = requests.post(
                self.invocations_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            response_time = time.time() - start_time
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Time: {response_time:.2f}s")
            
            # Check status code
            if response.status_code != 200:
                self.log_test_result(
                    test_name,
                    False,
                    f"Unexpected status code: {response.status_code}"
                )
                return False
            
            # Parse response JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError as e:
                self.log_test_result(
                    test_name,
                    False,
                    f"Invalid JSON response: {e}"
                )
                return False
            
            # Validate response format
            if not self.validate_agentcore_response_format(response_data, test_name):
                return False
            
            # Handle error responses vs success responses differently
            if "error" in response_data:
                # This is an expected error response - validate it has proper error format
                error_message = response_data.get("error", "")
                if not error_message or len(error_message.strip()) == 0:
                    self.log_test_result(
                        test_name,
                        False,
                        "Empty error field in error response"
                    )
                    return False
                
                self.log_test_result(
                    test_name,
                    True,
                    f"Valid error response received: {error_message[:100]}..."
                )
                return True
            
            # Validate success response content
            result = response_data.get("result", "")
            if not result or len(result.strip()) == 0:
                self.log_test_result(
                    test_name,
                    False,
                    "Empty result field in response"
                )
                return False
            
            # Check for educational disclaimer (check both result text and metadata)
            educational_terms = ["educational", "education", "disclaimer", "not financial advice", 
                               "consult", "qualified", "for educational purposes", "not licensed"]
            has_educational_content_in_result = any(term.lower() in result.lower() for term in educational_terms)
            
            # Also check metadata for educational disclaimer
            has_educational_metadata = False
            metadata = response_data.get("metadata", {})
            if isinstance(metadata, dict):
                # Check for educational_disclaimer flag
                if metadata.get("educational_disclaimer") is True:
                    has_educational_metadata = True
                # Check for disclaimer text in metadata
                disclaimer_text = metadata.get("disclaimer", "")
                if isinstance(disclaimer_text, str) and any(term.lower() in disclaimer_text.lower() for term in educational_terms):
                    has_educational_metadata = True
            
            has_educational_content = has_educational_content_in_result or has_educational_metadata
            
            if not has_educational_content:
                self.log_test_result(
                    test_name,
                    False,
                    "Response missing educational disclaimer or guidance (checked both result and metadata)"
                )
                return False
            
            self.log_test_result(
                test_name,
                True,
                f"Valid response received ({len(result)} chars, {response_time:.2f}s)"
            )
            return True
            
        except requests.exceptions.Timeout:
            self.log_test_result(
                test_name,
                False,
                f"Request timeout after {timeout}s"
            )
            return False
        except requests.exceptions.ConnectionError:
            self.log_test_result(
                test_name,
                False,
                "Connection error - server not reachable"
            )
            return False
        except Exception as e:
            self.log_test_result(
                test_name,
                False,
                f"Unexpected error: {e}"
            )
            return False
    
    def test_error_handling(self) -> bool:
        """
        Test error handling scenarios with invalid payloads.
        
        Returns:
            bool: True if error handling works correctly, False otherwise
        """
        print(f"\n🔍 Testing Error Handling Scenarios")
        
        error_test_cases = [
            {
                "name": "Empty Payload",
                "payload": {},
                "expected_error": True
            },
            {
                "name": "Missing Prompt Field",
                "payload": {"other_field": "value"},
                "expected_error": True
            },
            {
                "name": "Empty Prompt",
                "payload": {"prompt": ""},
                "expected_error": True
            },
            {
                "name": "Non-string Prompt",
                "payload": {"prompt": 123},
                "expected_error": True
            }
        ]
        
        all_passed = True
        
        for test_case in error_test_cases:
            print(f"\n   Testing: {test_case['name']}")
            
            try:
                response = requests.post(
                    self.invocations_url,
                    json=test_case["payload"],
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Should have error field for invalid requests
                    if test_case["expected_error"]:
                        if "error" in response_data:
                            self.log_test_result(
                                f"Error Handling - {test_case['name']}",
                                True,
                                f"Correctly returned error: {response_data.get('error')[:100]}..."
                            )
                        else:
                            self.log_test_result(
                                f"Error Handling - {test_case['name']}",
                                False,
                                "Expected error response but got success"
                            )
                            all_passed = False
                    else:
                        self.log_test_result(
                            f"Error Handling - {test_case['name']}",
                            True,
                            "Valid request processed successfully"
                        )
                else:
                    self.log_test_result(
                        f"Error Handling - {test_case['name']}",
                        False,
                        f"Unexpected status code: {response.status_code}"
                    )
                    all_passed = False
                    
            except Exception as e:
                self.log_test_result(
                    f"Error Handling - {test_case['name']}",
                    False,
                    f"Request failed: {e}"
                )
                all_passed = False
        
        return all_passed
    
    def run_comprehensive_tests(self) -> bool:
        """
        Run comprehensive test suite with various financial queries.
        
        Returns:
            bool: True if all tests pass, False otherwise
        """
        print("=" * 80)
        print("🧪 AgentCore HTTP Request Comprehensive Test Suite")
        print("=" * 80)
        print(f"Server URL: {self.server_url}")
        print(f"Test timeout: {self.timeout}s")
        
        # Test cases with sample financial queries
        test_cases = [
            {
                "name": "Basic Stock Analysis",
                "payload": {"prompt": "Analyze AAPL stock for moderate risk investor"},
                "timeout": 15  # Shorter timeout for incomplete queries
            },
            {
                "name": "Complete Financial Query",
                "payload": {"prompt": "Provide financial analysis for TSLA with aggressive risk tolerance and long-term investment horizon"},
                "timeout": 60  # Longer timeout for complete analysis
            },
            {
                "name": "Conservative Investment Query",
                "payload": {"prompt": "Analyze MSFT for conservative investor with short-term horizon"},
                "timeout": 60  # Longer timeout for complete analysis
            },
            {
                "name": "Market Research Query",
                "payload": {"prompt": "Research GOOGL stock and provide investment recommendations with moderate risk tolerance and medium-term horizon"},
                "timeout": 60  # Longer timeout and complete query
            }
        ]
        
        all_passed = True
        
        # Test 1: Health check endpoint
        if not self.test_ping_endpoint():
            all_passed = False
        
        # Test 2: Error handling
        if not self.test_error_handling():
            all_passed = False
        
        # Test 3: Valid financial queries
        for test_case in test_cases:
            if not self.test_invocations_endpoint(
                test_case["payload"],
                test_case["name"],
                test_case.get("timeout")
            ):
                all_passed = False
        
        return all_passed
    
    def run_quick_tests(self) -> bool:
        """
        Run quick test suite with basic functionality checks.
        
        Returns:
            bool: True if basic tests pass, False otherwise
        """
        print("=" * 80)
        print("🚀 AgentCore HTTP Request Quick Test Suite")
        print("=" * 80)
        print(f"Server URL: {self.server_url}")
        print(f"Quick test timeout: {self.quick_timeout}s")
        
        all_passed = True
        
        # Test 1: Health check
        if not self.test_ping_endpoint():
            all_passed = False
        
        # Test 2: Basic invocation (incomplete query - should ask for more info)
        if not self.test_invocations_endpoint(
            {"prompt": "Analyze AAPL stock for moderate risk investor"},
            "Quick Stock Analysis (Incomplete Query)",
            self.quick_timeout
        ):
            all_passed = False
        
        # Test 3: Error handling (empty payload)
        if not self.test_invocations_endpoint(
            {},
            "Quick Error Handling (Empty Payload)",
            5
        ):
            all_passed = False
        
        # Test 4: Error handling (missing prompt)
        if not self.test_invocations_endpoint(
            {"other_field": "value"},
            "Quick Error Handling (Missing Prompt)",
            5
        ):
            all_passed = False
        
        return all_passed
    
    def print_test_summary(self):
        """Print comprehensive test results summary."""
        print("\n" + "=" * 80)
        print("📊 Test Results Summary")
        print("=" * 80)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        if self.passed_tests == total_tests:
            print(f"\n🎉 All tests passed! AgentCore server is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Please check the server configuration.")


def main():
    """Main entry point for HTTP test script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="HTTP test suite for AgentCore financial advisor system"
    )
    parser.add_argument(
        "--server",
        default="http://localhost:8080",
        help="AgentCore server URL (default: http://localhost:8080)"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick test suite only"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = AgentCoreHTTPTester(args.server)
    tester.timeout = args.timeout
    
    try:
        if args.quick:
            success = tester.run_quick_tests()
        else:
            success = tester.run_comprehensive_tests()
        
        tester.print_test_summary()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Test suite interrupted by user")
        tester.print_test_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()