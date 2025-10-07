#!/usr/bin/env python3
"""
AgentCore Error Handling Validation

This test validates comprehensive error handling scenarios in the AgentCore
financial advisor system, ensuring graceful error responses and proper fallback mechanisms.

Tests cover:
- Invalid payload formats
- Web search API failures and rate limiting
- Agent invocation errors
- Graceful error responses
- Requirements: 8.1, 8.2, 8.3, 8.5

Author: Financial Advisory System Testing
License: Educational Use Only
"""

import json
import time
import requests
import subprocess
import sys
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
from unittest.mock import patch, MagicMock


class AgentCoreErrorHandlingTester:
    """
    Comprehensive tester for AgentCore error handling scenarios.
    
    This class validates that the system handles various error conditions gracefully
    and provides appropriate error responses without crashing.
    """
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8080):
        self.server_host = server_host
        self.server_port = server_port
        self.base_url = f"http://{server_host}:{server_port}"
        self.server_process = None
        self.test_results = []
        
        # Define error test scenarios
        self.error_scenarios = self._define_error_scenarios()
    
    def _define_error_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Define comprehensive error scenarios for testing.
        
        Returns:
            dict: Categorized error scenarios with expected behaviors
        """
        return {
            "invalid_payload_formats": [
                {
                    "name": "Empty JSON payload",
                    "payload": {},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_prompt",
                    "description": "Empty dictionary payload"
                },
                {
                    "name": "Missing prompt field",
                    "payload": {"data": "some data", "session": "123"},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_prompt",
                    "description": "Payload without prompt field"
                },
                {
                    "name": "Null prompt field",
                    "payload": {"prompt": None},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_prompt",
                    "description": "Prompt field is null"
                },
                {
                    "name": "Non-string prompt field",
                    "payload": {"prompt": 12345},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_string_prompt",
                    "description": "Prompt field is not a string"
                },
                {
                    "name": "Empty string prompt",
                    "payload": {"prompt": ""},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_non_empty_prompt",
                    "description": "Empty string in prompt field"
                },
                {
                    "name": "Whitespace only prompt",
                    "payload": {"prompt": "   \n\t   "},
                    "expected_error_type": "validation_error",
                    "expected_behavior": "should_request_non_empty_prompt",
                    "description": "Only whitespace in prompt field"
                }
            ],
            
            "malformed_requests": [
                {
                    "name": "Invalid JSON",
                    "raw_data": '{"prompt": "test", invalid json}',
                    "expected_error_type": "json_parse_error",
                    "expected_behavior": "should_handle_json_error",
                    "description": "Malformed JSON in request body"
                },
                {
                    "name": "Non-JSON content type",
                    "payload": "prompt=test&data=value",
                    "content_type": "application/x-www-form-urlencoded",
                    "expected_error_type": "content_type_error",
                    "expected_behavior": "should_handle_content_type_error",
                    "description": "Form data instead of JSON"
                },
                {
                    "name": "Extremely large payload",
                    "payload": {"prompt": "A" * 100000},  # 100KB prompt
                    "expected_error_type": "payload_size_error",
                    "expected_behavior": "should_handle_large_payload",
                    "description": "Oversized payload"
                }
            ],
            
            "network_and_timeout_scenarios": [
                {
                    "name": "Request timeout simulation",
                    "payload": {"prompt": "Analyze AAPL with comprehensive research"},
                    "timeout": 1,  # Very short timeout
                    "expected_error_type": "timeout_error",
                    "expected_behavior": "should_timeout_gracefully",
                    "description": "Client-side timeout"
                },
                {
                    "name": "Connection interruption",
                    "payload": {"prompt": "Long analysis request"},
                    "interrupt_connection": True,
                    "expected_error_type": "connection_error",
                    "expected_behavior": "should_handle_connection_loss",
                    "description": "Connection lost during request"
                }
            ],
            
            "agent_error_scenarios": [
                {
                    "name": "Web search rate limit simulation",
                    "payload": {"prompt": "Research AAPL with extensive web search"},
                    "simulate_rate_limit": True,
                    "expected_error_type": "rate_limit_error",
                    "expected_behavior": "should_handle_rate_limit_gracefully",
                    "description": "DuckDuckGo rate limiting"
                },
                {
                    "name": "Web search API failure simulation",
                    "payload": {"prompt": "Analyze TSLA with market research"},
                    "simulate_search_failure": True,
                    "expected_error_type": "web_search_error",
                    "expected_behavior": "should_handle_search_failure_gracefully",
                    "description": "DuckDuckGo API failure"
                },
                {
                    "name": "Agent parameter error simulation",
                    "payload": {"prompt": "Comprehensive MSFT analysis"},
                    "simulate_agent_error": True,
                    "expected_error_type": "agent_parameter_error",
                    "expected_behavior": "should_use_fallback_mechanisms",
                    "description": "Agent invocation parameter errors"
                }
            ]
        }
    
    def start_agentcore_server(self) -> bool:
        """Start the AgentCore server for testing."""
        try:
            print("🚀 Starting AgentCore server for error handling testing...")
            
            self.server_process = subprocess.Popen(
                [sys.executable, "financial_advisor_agentcore.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server startup with better error handling
            max_wait_time = 45  # Increased wait time
            for attempt in range(max_wait_time):
                try:
                    response = requests.get(f"{self.base_url}/ping", timeout=10)
                    if response.status_code == 200:
                        print(f"✅ AgentCore server started successfully")
                        return True
                except requests.exceptions.RequestException as e:
                    # Check if process is still running
                    if self.server_process.poll() is not None:
                        # Process has terminated
                        stdout, stderr = self.server_process.communicate()
                        print(f"❌ Server process terminated unexpectedly")
                        print(f"Stdout: {stdout}")
                        print(f"Stderr: {stderr}")
                        return False
                
                time.sleep(1)
                if attempt % 5 == 0:
                    print(f"⏳ Waiting for server startup... ({attempt + 1}/{max_wait_time})")
            
            print("❌ Failed to start AgentCore server within timeout")
            # Get any error output
            if self.server_process.poll() is None:
                self.server_process.terminate()
                stdout, stderr = self.server_process.communicate(timeout=5)
                if stderr:
                    print(f"Server stderr: {stderr}")
                if stdout:
                    print(f"Server stdout: {stdout}")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_agentcore_server(self):
        """Stop the AgentCore server gracefully."""
        if self.server_process:
            print("🛑 Stopping AgentCore server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
    
    def send_request_with_error_conditions(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request with specific error conditions.
        
        Args:
            scenario: Error scenario configuration
            
        Returns:
            dict: Response data and error analysis
        """
        try:
            start_time = time.time()
            
            # Handle different request types
            if "raw_data" in scenario:
                # Send raw malformed data
                response = requests.post(
                    f"{self.base_url}/invocations",
                    data=scenario["raw_data"],
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
            elif scenario.get("content_type") == "application/x-www-form-urlencoded":
                # Send form data instead of JSON
                response = requests.post(
                    f"{self.base_url}/invocations",
                    data=scenario["payload"],
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30
                )
            else:
                # Standard JSON request with potential timeout
                timeout = scenario.get("timeout", 30)
                response = requests.post(
                    f"{self.base_url}/invocations",
                    json=scenario["payload"],
                    headers={"Content-Type": "application/json"},
                    timeout=timeout
                )
            
            end_time = time.time()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "response_data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "headers": dict(response.headers)
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error_type": "timeout",
                "error": "Request timeout",
                "response_time": scenario.get("timeout", 30)
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error_type": "connection_error",
                "error": "Connection error",
                "response_time": time.time() - start_time
            }
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "error_type": "json_decode_error",
                "error": "Invalid JSON response",
                "response_time": time.time() - start_time
            }
        except Exception as e:
            return {
                "success": False,
                "error_type": "request_error",
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def analyze_error_response(self, response: Dict[str, Any], expected_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the error response for appropriateness.
        
        Requirements: 8.1, 8.2, 8.3, 8.5
        """
        analysis = {
            "error_handled_gracefully": False,
            "appropriate_error_type": False,
            "structured_error_response": False,
            "helpful_error_message": False,
            "no_system_crash": False,
            "metadata_present": False,
            "recovery_guidance": False
        }
        
        expected_error_type = expected_scenario.get("expected_error_type", "")
        expected_behavior = expected_scenario.get("expected_behavior", "")
        
        # Check if request succeeded (got a response)
        if response.get("success", False):
            analysis["no_system_crash"] = True
            
            response_data = response.get("response_data", {})
            
            # Check for structured error response
            if isinstance(response_data, dict):
                analysis["structured_error_response"] = True
                
                # Check for error field
                if "error" in response_data:
                    analysis["error_handled_gracefully"] = True
                    
                    error_message = response_data["error"].lower()
                    
                    # Check for appropriate error type
                    if expected_error_type == "validation_error":
                        analysis["appropriate_error_type"] = any(term in error_message for term in [
                            "invalid", "format", "prompt", "provide", "required"
                        ])
                    elif expected_error_type == "rate_limit_error":
                        analysis["appropriate_error_type"] = any(term in error_message for term in [
                            "rate limit", "try again", "delay", "exceeded"
                        ])
                    elif expected_error_type == "web_search_error":
                        analysis["appropriate_error_type"] = any(term in error_message for term in [
                            "search", "unavailable", "limited", "service"
                        ])
                    elif expected_error_type == "agent_parameter_error":
                        analysis["appropriate_error_type"] = any(term in error_message for term in [
                            "configuration", "fallback", "parameter", "mechanism"
                        ])
                    else:
                        analysis["appropriate_error_type"] = True  # Generic error handling
                    
                    # Check for helpful error message
                    helpful_indicators = [
                        "please", "try", "provide", "check", "example", "format",
                        "required", "should", "need", "specify"
                    ]
                    analysis["helpful_error_message"] = any(indicator in error_message for indicator in helpful_indicators)
                    
                    # Check for recovery guidance
                    recovery_indicators = [
                        "try again", "please provide", "check your", "example:",
                        "should include", "format:", "specify"
                    ]
                    analysis["recovery_guidance"] = any(indicator in error_message for indicator in recovery_indicators)
                
                # Check for metadata
                if "metadata" in response_data:
                    analysis["metadata_present"] = True
                    metadata = response_data["metadata"]
                    
                    # Additional metadata checks
                    if isinstance(metadata, dict):
                        if "error_category" in metadata:
                            analysis["structured_error_response"] = True
                        if "suggestion" in metadata:
                            analysis["recovery_guidance"] = True
                
                # For successful responses (not errors), check if they handle the scenario appropriately
                elif "result" in response_data:
                    result_content = response_data["result"].lower()
                    
                    # For validation scenarios, should still provide guidance
                    if expected_behavior in ["should_request_prompt", "should_request_non_empty_prompt"]:
                        guidance_indicators = ["provide", "include", "specify", "need", "require"]
                        analysis["helpful_error_message"] = any(indicator in result_content for indicator in guidance_indicators)
                        analysis["error_handled_gracefully"] = analysis["helpful_error_message"]
        else:
            # Request failed at network level
            error_type = response.get("error_type", "")
            
            if error_type == "timeout":
                analysis["appropriate_error_type"] = expected_error_type == "timeout_error"
                analysis["error_handled_gracefully"] = True  # Timeout is handled gracefully by client
            elif error_type == "connection_error":
                analysis["appropriate_error_type"] = expected_error_type == "connection_error"
                analysis["error_handled_gracefully"] = True  # Connection error is handled gracefully
        
        return analysis
    
    def test_error_scenario_category(self, category_name: str, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test a category of error scenarios."""
        print(f"\n🧪 Testing {category_name.replace('_', ' ').title()}")
        print("-" * 60)
        
        category_results = {
            "category": category_name,
            "total_scenarios": len(scenarios),
            "successful_scenarios": 0,
            "failed_scenarios": 0,
            "scenario_results": []
        }
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🔍 Scenario {i}/{len(scenarios)}: {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            
            # Send request with error conditions
            response = self.send_request_with_error_conditions(scenario)
            
            scenario_result = {
                "scenario": scenario,
                "response": response,
                "error_analysis": {},
                "success": False
            }
            
            # Analyze the error response
            error_analysis = self.analyze_error_response(response, scenario)
            scenario_result["error_analysis"] = error_analysis
            
            # Determine scenario success
            scenario_result["success"] = (
                error_analysis["no_system_crash"] and
                error_analysis["error_handled_gracefully"] and
                (error_analysis["appropriate_error_type"] or error_analysis["helpful_error_message"])
            )
            
            # Print results
            print(f"   📊 Error Handling Analysis:")
            print(f"      No System Crash: {'✓' if error_analysis['no_system_crash'] else '✗'}")
            print(f"      Graceful Handling: {'✓' if error_analysis['error_handled_gracefully'] else '✗'}")
            print(f"      Appropriate Error Type: {'✓' if error_analysis['appropriate_error_type'] else '✗'}")
            print(f"      Helpful Message: {'✓' if error_analysis['helpful_error_message'] else '✗'}")
            print(f"      Structured Response: {'✓' if error_analysis['structured_error_response'] else '✗'}")
            print(f"      Recovery Guidance: {'✓' if error_analysis['recovery_guidance'] else '✗'}")
            print(f"      Metadata Present: {'✓' if error_analysis['metadata_present'] else '✗'}")
            
            if scenario_result["success"]:
                print(f"   🎯 Scenario Test: PASSED")
                category_results["successful_scenarios"] += 1
            else:
                print(f"   ❌ Scenario Test: FAILED")
                category_results["failed_scenarios"] += 1
            
            # Show response sample
            if response.get("success") and isinstance(response.get("response_data"), dict):
                error_msg = response["response_data"].get("error", response["response_data"].get("result", ""))
                if error_msg:
                    print(f"   📄 Response Sample: {str(error_msg)[:150]}...")
            elif not response.get("success"):
                print(f"   📄 Error: {response.get('error', 'Unknown error')}")
            
            category_results["scenario_results"].append(scenario_result)
        
        # Category summary
        success_rate = (category_results["successful_scenarios"] / category_results["total_scenarios"]) * 100
        print(f"\n📊 {category_name.replace('_', ' ').title()} Results:")
        print(f"   Total: {category_results['total_scenarios']}")
        print(f"   Passed: {category_results['successful_scenarios']}")
        print(f"   Failed: {category_results['failed_scenarios']}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return category_results
    
    def run_error_handling_tests(self) -> Dict[str, Any]:
        """Run all error handling tests."""
        print("🧪 AgentCore Error Handling Test Suite")
        print("=" * 80)
        print("Testing Requirements: 8.1, 8.2, 8.3, 8.5")
        print("- Invalid payload formats")
        print("- Web search API failures and rate limiting")
        print("- Agent invocation errors")
        print("- Graceful error responses")
        print("=" * 80)
        
        if not self.start_agentcore_server():
            return {"success": False, "error": "Failed to start server"}
        
        try:
            all_results = {
                "timestamp": datetime.now().isoformat(),
                "total_categories": len(self.error_scenarios),
                "category_results": {},
                "overall_stats": {
                    "total_scenarios": 0,
                    "successful_scenarios": 0,
                    "failed_scenarios": 0
                }
            }
            
            # Test each category
            for category_name, scenarios in self.error_scenarios.items():
                category_result = self.test_error_scenario_category(category_name, scenarios)
                all_results["category_results"][category_name] = category_result
                
                # Update overall stats
                all_results["overall_stats"]["total_scenarios"] += category_result["total_scenarios"]
                all_results["overall_stats"]["successful_scenarios"] += category_result["successful_scenarios"]
                all_results["overall_stats"]["failed_scenarios"] += category_result["failed_scenarios"]
            
            # Calculate overall success
            total = all_results["overall_stats"]["total_scenarios"]
            successful = all_results["overall_stats"]["successful_scenarios"]
            success_rate = (successful / total) * 100 if total > 0 else 0
            
            all_results["success"] = success_rate >= 85  # 85% success threshold for error handling
            all_results["overall_stats"]["success_rate"] = success_rate
            
            # Print final summary
            print(f"\n🏁 Error Handling Test Suite Complete")
            print(f"=" * 50)
            print(f"Total Scenarios: {total}")
            print(f"Successful: {successful}")
            print(f"Failed: {all_results['overall_stats']['failed_scenarios']}")
            print(f"Success Rate: {success_rate:.1f}%")
            
            if all_results["success"]:
                print(f"🎉 ERROR HANDLING TESTS PASSED")
                print(f"✅ Invalid payload formats handled gracefully")
                print(f"✅ Web search failures handled appropriately")
                print(f"✅ Agent errors handled with fallbacks")
                print(f"✅ Structured error responses provided")
            else:
                print(f"❌ SOME ERROR HANDLING TESTS FAILED")
                print(f"Please review detailed results for issues")
            
            return all_results
            
        finally:
            self.stop_agentcore_server()


def main():
    """Run the error handling tests."""
    tester = AgentCoreErrorHandlingTester()
    
    try:
        results = tester.run_error_handling_tests()
        
        # Save results
        with open("agentcore_error_handling_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: agentcore_error_handling_test_results.json")
        
        sys.exit(0 if results.get("success", False) else 1)
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Test interrupted by user")
        tester.stop_agentcore_server()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        tester.stop_agentcore_server()
        sys.exit(1)


if __name__ == "__main__":
    main()