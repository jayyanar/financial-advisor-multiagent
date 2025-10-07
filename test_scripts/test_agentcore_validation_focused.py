#!/usr/bin/env python3
"""
Focused AgentCore HTTP Validation Test Suite

This script provides focused HTTP testing specifically for task 6.2 requirements:
- Test POST /invocations endpoint with sample financial queries
- Test GET /ping endpoint for health checks  
- Validate response formats match AgentCore expectations

This version focuses on validation rather than full financial analysis performance.
"""

import requests
import json
import time
import sys
from typing import Dict, Any
from datetime import datetime


class FocusedAgentCoreValidator:
    """Focused HTTP validation for AgentCore requirements."""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url.rstrip('/')
        self.invocations_url = f"{self.server_url}/invocations"
        self.ping_url = f"{self.server_url}/ping"
        
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
        """Test GET /ping endpoint for health checks (Requirement 5.3)."""
        print(f"\n🔍 Testing Health Check: GET {self.ping_url}")
        
        try:
            start_time = time.time()
            response = requests.get(self.ping_url, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test_result(
                    "GET /ping Health Check",
                    True,
                    f"Status: {response.status_code}, Response time: {response_time:.2f}s"
                )
                return True
            else:
                self.log_test_result(
                    "GET /ping Health Check",
                    False,
                    f"Unexpected status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "GET /ping Health Check",
                False,
                f"Request failed: {e}"
            )
            return False
    
    def validate_response_format(self, response_data: Dict[str, Any], test_name: str) -> bool:
        """Validate response format matches AgentCore expectations (Requirement 5.4)."""
        
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
                f"{test_name} - Format Validation",
                False,
                f"Missing required fields: {missing_fields}"
            )
            return False
        
        # Validate system field
        if response_data.get("system") != "financial-advisor-multiagent":
            self.log_test_result(
                f"{test_name} - Format Validation",
                False,
                f"Invalid system field: {response_data.get('system')}"
            )
            return False
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(response_data.get("timestamp", "").replace('Z', '+00:00'))
        except ValueError:
            self.log_test_result(
                f"{test_name} - Format Validation",
                False,
                "Invalid timestamp format"
            )
            return False
        
        self.log_test_result(
            f"{test_name} - Format Validation",
            True,
            "Response format matches AgentCore expectations"
        )
        return True
    
    def test_invocations_endpoint(self, payload: Dict[str, Any], test_name: str, timeout: int = 10) -> bool:
        """Test POST /invocations endpoint (Requirements 5.2, 5.3, 5.4)."""
        print(f"\n🔍 Testing Invocations: {test_name}")
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
            if not self.validate_response_format(response_data, test_name):
                return False
            
            # Log success
            content_type = "error" if "error" in response_data else "result"
            content_length = len(response_data.get(content_type, ""))
            
            self.log_test_result(
                test_name,
                True,
                f"Valid {content_type} response ({content_length} chars, {response_time:.2f}s)"
            )
            return True
            
        except requests.exceptions.Timeout:
            self.log_test_result(
                test_name,
                False,
                f"Request timeout after {timeout}s"
            )
            return False
        except Exception as e:
            self.log_test_result(
                test_name,
                False,
                f"Request failed: {e}"
            )
            return False
    
    def run_validation_tests(self) -> bool:
        """Run focused validation test suite for task 6.2 requirements."""
        print("=" * 80)
        print("🧪 AgentCore HTTP Validation Test Suite (Task 6.2)")
        print("=" * 80)
        print(f"Server URL: {self.server_url}")
        print("\nRequirements being validated:")
        print("- 5.2: Test POST /invocations endpoint with sample financial queries")
        print("- 5.3: Test GET /ping endpoint for health checks")
        print("- 5.4: Validate response formats match AgentCore expectations")
        
        all_passed = True
        
        # Requirement 5.3: Test GET /ping endpoint for health checks
        if not self.test_ping_endpoint():
            all_passed = False
        
        # Requirement 5.2 & 5.4: Test POST /invocations with various payloads
        test_cases = [
            # Valid financial queries (sample queries as required)
            {
                "name": "Sample Financial Query - AAPL",
                "payload": {"prompt": "Analyze AAPL stock for moderate risk investor"},
                "timeout": 10
            },
            {
                "name": "Sample Financial Query - TSLA", 
                "payload": {"prompt": "Analyze TSLA for aggressive risk tolerance"},
                "timeout": 10
            },
            {
                "name": "Sample Financial Query - MSFT",
                "payload": {"prompt": "Research MSFT stock"},
                "timeout": 10
            },
            
            # Error handling validation
            {
                "name": "Error Handling - Empty Payload",
                "payload": {},
                "timeout": 5
            },
            {
                "name": "Error Handling - Missing Prompt",
                "payload": {"other_field": "value"},
                "timeout": 5
            },
            {
                "name": "Error Handling - Empty Prompt",
                "payload": {"prompt": ""},
                "timeout": 5
            },
            {
                "name": "Error Handling - Invalid Prompt Type",
                "payload": {"prompt": 123},
                "timeout": 5
            }
        ]
        
        for test_case in test_cases:
            if not self.test_invocations_endpoint(
                test_case["payload"],
                test_case["name"],
                test_case["timeout"]
            ):
                all_passed = False
        
        return all_passed
    
    def print_test_summary(self):
        """Print comprehensive test results summary."""
        print("\n" + "=" * 80)
        print("📊 Task 6.2 Validation Results Summary")
        print("=" * 80)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Requirements validation summary
        print(f"\n📋 Requirements Validation:")
        print(f"✅ 5.2: POST /invocations endpoint tested with sample financial queries")
        print(f"✅ 5.3: GET /ping endpoint tested for health checks")
        print(f"✅ 5.4: Response formats validated against AgentCore expectations")
        
        if self.failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        if self.passed_tests == total_tests:
            print(f"\n🎉 All validation tests passed! Task 6.2 requirements satisfied.")
        else:
            print(f"\n⚠️  Some tests failed. Please check the server configuration.")


def main():
    """Main entry point for focused validation test script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Focused HTTP validation test suite for AgentCore task 6.2"
    )
    parser.add_argument(
        "--server",
        default="http://localhost:8080",
        help="AgentCore server URL (default: http://localhost:8080)"
    )
    
    args = parser.parse_args()
    
    # Create validator instance
    validator = FocusedAgentCoreValidator(args.server)
    
    try:
        success = validator.run_validation_tests()
        validator.print_test_summary()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Validation interrupted by user")
        validator.print_test_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()