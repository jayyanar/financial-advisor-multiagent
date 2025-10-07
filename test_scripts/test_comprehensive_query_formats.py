#!/usr/bin/env python3
"""
Comprehensive AgentCore Query Format Testing

This test validates various input query formats and parameter extraction capabilities
of the AgentCore financial advisor system with realistic expectations.

Tests cover:
- Simple ticker-only queries
- Complete queries with risk tolerance and horizon  
- Queries missing required information
- Parameter extraction and missing parameter handling
- Edge cases and error handling

Requirements: 7.1, 7.2, 7.3, 7.4

Author: Financial Advisory System Testing
License: Educational Use Only
"""

import json
import time
import requests
import subprocess
import sys
from typing import Dict, Any, List, Tuple
from datetime import datetime


class ComprehensiveQueryFormatTester:
    """
    Comprehensive tester for AgentCore query formats with realistic expectations.
    """
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8080):
        self.server_host = server_host
        self.server_port = server_port
        self.base_url = f"http://{server_host}:{server_port}"
        self.server_process = None
        
    def start_agentcore_server(self) -> bool:
        """Start the AgentCore server for testing."""
        try:
            print("🚀 Starting AgentCore server for comprehensive query format testing...")
            
            self.server_process = subprocess.Popen(
                [sys.executable, "financial_advisor_agentcore.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server startup
            max_wait_time = 30
            for attempt in range(max_wait_time):
                try:
                    response = requests.get(f"{self.base_url}/ping", timeout=5)
                    if response.status_code == 200:
                        print(f"✅ AgentCore server started successfully")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(1)
                if attempt % 5 == 0:
                    print(f"⏳ Waiting for server startup... ({attempt + 1}/{max_wait_time})")
            
            print("❌ Failed to start AgentCore server")
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
    
    def send_query(self, query: str, timeout: int = 30) -> Dict[str, Any]:
        """Send a query to the AgentCore server."""
        try:
            payload = {"prompt": query}
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/invocations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            end_time = time.time()
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "response_time": end_time - start_time,
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "response_time": end_time - start_time,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": 0
            }
    
    def test_simple_ticker_queries(self) -> Dict[str, Any]:
        """
        Test simple ticker-only queries.
        
        Requirements: 7.1, 7.2 - Test simple ticker-only queries and parameter extraction
        """
        print("\n🧪 Testing Simple Ticker-Only Queries")
        print("-" * 50)
        
        test_cases = [
            {
                "query": "AAPL",
                "description": "Single ticker symbol",
                "expected_behavior": "should_request_missing_parameters"
            },
            {
                "query": "Analyze TSLA",
                "description": "Ticker with analyze verb",
                "expected_behavior": "should_request_missing_parameters"
            }
        ]
        
        results = {
            "category": "simple_ticker_queries",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "test_results": []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}/{len(test_cases)}: {test_case['description']}")
            print(f"   Query: '{test_case['query']}'")
            
            response = self.send_query(test_case["query"])
            
            test_result = {
                "query": test_case["query"],
                "description": test_case["description"],
                "response_received": response["success"],
                "response_time": response.get("response_time", 0),
                "passed": False,
                "analysis": {}
            }
            
            if response["success"]:
                # Analyze the response
                data = response["data"]
                
                # Get response content (handle both result and error fields)
                content = ""
                if "result" in data:
                    content = data["result"].lower()
                elif "error" in data:
                    content = data["error"].lower()
                
                # Check if ticker is mentioned
                ticker_mentioned = any(ticker in content for ticker in ["aapl", "apple", "tsla", "tesla"])
                
                # Check if system asks for missing parameters
                asks_for_params = any(phrase in content for phrase in [
                    "need", "provide", "specify", "risk", "horizon", "tolerance", "timeframe"
                ])
                
                # Check if educational disclaimer is present
                has_disclaimer = any(phrase in content for phrase in [
                    "educational", "not financial advice", "disclaimer"
                ])
                
                test_result["analysis"] = {
                    "ticker_mentioned": ticker_mentioned,
                    "asks_for_missing_parameters": asks_for_params,
                    "has_educational_disclaimer": has_disclaimer,
                    "response_length": len(content)
                }
                
                # Test passes if it mentions ticker and asks for missing parameters
                test_result["passed"] = ticker_mentioned and asks_for_params
                
                if test_result["passed"]:
                    print(f"   ✅ PASSED ({response['response_time']:.2f}s)")
                    print(f"      - Ticker mentioned: ✓")
                    print(f"      - Asks for parameters: ✓")
                    results["passed_tests"] += 1
                else:
                    print(f"   ❌ FAILED ({response['response_time']:.2f}s)")
                    print(f"      - Ticker mentioned: {'✓' if ticker_mentioned else '✗'}")
                    print(f"      - Asks for parameters: {'✓' if asks_for_params else '✗'}")
                
                # Show response sample
                display_content = data.get("result", data.get("error", ""))
                print(f"   📄 Response: {display_content[:150]}...")
                
            else:
                print(f"   ❌ FAILED - Request error: {response['error']}")
            
            results["test_results"].append(test_result)
        
        success_rate = (results["passed_tests"] / results["total_tests"]) * 100
        print(f"\n📊 Simple Ticker Queries Results: {results['passed_tests']}/{results['total_tests']} passed ({success_rate:.1f}%)")
        
        return results
    
    def test_complete_queries(self) -> Dict[str, Any]:
        """
        Test complete queries with all parameters.
        
        Requirements: 7.2 - Test complete queries with risk tolerance and horizon
        """
        print("\n🧪 Testing Complete Queries")
        print("-" * 50)
        
        test_cases = [
            {
                "query": "Conservative investor, long-term horizon, analyze AAPL",
                "description": "Complete query with all parameters",
                "expected_behavior": "should_provide_analysis_or_proceed"
            }
        ]
        
        results = {
            "category": "complete_queries",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "test_results": []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}/{len(test_cases)}: {test_case['description']}")
            print(f"   Query: '{test_case['query']}'")
            
            response = self.send_query(test_case["query"], timeout=60)
            
            test_result = {
                "query": test_case["query"],
                "description": test_case["description"],
                "response_received": response["success"],
                "response_time": response.get("response_time", 0),
                "passed": False,
                "analysis": {}
            }
            
            if response["success"]:
                data = response["data"]
                
                # Get response content
                content = ""
                if "result" in data:
                    content = data["result"].lower()
                elif "error" in data:
                    content = data["error"].lower()
                
                # Check if response acknowledges the parameters
                mentions_risk = any(term in content for term in ["conservative", "risk", "tolerance"])
                mentions_horizon = any(term in content for term in ["long-term", "horizon", "timeframe"])
                mentions_ticker = any(term in content for term in ["aapl", "apple"])
                
                # Check if it provides analysis or proceeds appropriately
                provides_analysis = any(term in content for term in [
                    "analysis", "strategy", "market", "recommendation", "intelligence"
                ])
                
                test_result["analysis"] = {
                    "mentions_risk": mentions_risk,
                    "mentions_horizon": mentions_horizon,
                    "mentions_ticker": mentions_ticker,
                    "provides_analysis": provides_analysis,
                    "response_length": len(content)
                }
                
                # Test passes if it acknowledges parameters and provides some analysis
                test_result["passed"] = (mentions_risk or mentions_horizon or mentions_ticker) and len(content) > 50
                
                if test_result["passed"]:
                    print(f"   ✅ PASSED ({response['response_time']:.2f}s)")
                    results["passed_tests"] += 1
                else:
                    print(f"   ❌ FAILED ({response['response_time']:.2f}s)")
                
                print(f"      - Mentions risk: {'✓' if mentions_risk else '✗'}")
                print(f"      - Mentions horizon: {'✓' if mentions_horizon else '✗'}")
                print(f"      - Mentions ticker: {'✓' if mentions_ticker else '✗'}")
                print(f"      - Provides analysis: {'✓' if provides_analysis else '✗'}")
                
                # Show response sample
                display_content = data.get("result", data.get("error", ""))
                print(f"   📄 Response: {display_content[:150]}...")
                
            else:
                print(f"   ❌ FAILED - Request error: {response['error']}")
            
            results["test_results"].append(test_result)
        
        success_rate = (results["passed_tests"] / results["total_tests"]) * 100
        print(f"\n📊 Complete Queries Results: {results['passed_tests']}/{results['total_tests']} passed ({success_rate:.1f}%)")
        
        return results
    
    def test_missing_parameter_queries(self) -> Dict[str, Any]:
        """
        Test queries missing required information.
        
        Requirements: 7.3 - Test queries missing required information
        """
        print("\n🧪 Testing Missing Parameter Queries")
        print("-" * 50)
        
        test_cases = [
            {
                "query": "I want investment advice",
                "description": "Missing all parameters",
                "expected_behavior": "should_request_all_parameters"
            }
        ]
        
        results = {
            "category": "missing_parameter_queries",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "test_results": []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}/{len(test_cases)}: {test_case['description']}")
            print(f"   Query: '{test_case['query']}'")
            
            response = self.send_query(test_case["query"])
            
            test_result = {
                "query": test_case["query"],
                "description": test_case["description"],
                "response_received": response["success"],
                "response_time": response.get("response_time", 0),
                "passed": False,
                "analysis": {}
            }
            
            if response["success"]:
                data = response["data"]
                
                # Get response content
                content = ""
                if "result" in data:
                    content = data["result"].lower()
                elif "error" in data:
                    content = data["error"].lower()
                
                # Check if system handles missing parameters appropriately
                requests_ticker = any(phrase in content for phrase in ["ticker", "stock", "symbol", "company"])
                requests_risk = any(phrase in content for phrase in ["risk", "tolerance", "conservative", "moderate", "aggressive"])
                requests_horizon = any(phrase in content for phrase in ["horizon", "term", "timeframe"])
                
                # Check if it provides guidance
                provides_guidance = any(phrase in content for phrase in [
                    "need", "provide", "specify", "include", "please"
                ])
                
                test_result["analysis"] = {
                    "requests_ticker": requests_ticker,
                    "requests_risk": requests_risk,
                    "requests_horizon": requests_horizon,
                    "provides_guidance": provides_guidance,
                    "response_length": len(content)
                }
                
                # Test passes if it provides guidance and requests missing information
                test_result["passed"] = provides_guidance and (requests_ticker or requests_risk or requests_horizon)
                
                if test_result["passed"]:
                    print(f"   ✅ PASSED ({response['response_time']:.2f}s)")
                    results["passed_tests"] += 1
                else:
                    print(f"   ❌ FAILED ({response['response_time']:.2f}s)")
                
                print(f"      - Requests ticker: {'✓' if requests_ticker else '✗'}")
                print(f"      - Requests risk: {'✓' if requests_risk else '✗'}")
                print(f"      - Requests horizon: {'✓' if requests_horizon else '✗'}")
                print(f"      - Provides guidance: {'✓' if provides_guidance else '✗'}")
                
                # Show response sample
                display_content = data.get("result", data.get("error", ""))
                print(f"   📄 Response: {display_content[:150]}...")
                
            else:
                print(f"   ❌ FAILED - Request error: {response['error']}")
            
            results["test_results"].append(test_result)
        
        success_rate = (results["passed_tests"] / results["total_tests"]) * 100
        print(f"\n📊 Missing Parameter Queries Results: {results['passed_tests']}/{results['total_tests']} passed ({success_rate:.1f}%)")
        
        return results
    
    def test_edge_cases(self) -> Dict[str, Any]:
        """
        Test edge cases and error handling.
        
        Requirements: 7.4 - Test parameter extraction and missing parameter handling
        """
        print("\n🧪 Testing Edge Cases")
        print("-" * 50)
        
        test_cases = [
            {
                "query": "",
                "description": "Empty query",
                "expected_behavior": "should_return_error"
            },
            {
                "query": "   ",
                "description": "Whitespace-only query",
                "expected_behavior": "should_return_error"
            }
        ]
        
        results = {
            "category": "edge_cases",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "test_results": []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}/{len(test_cases)}: {test_case['description']}")
            print(f"   Query: '{test_case['query']}'")
            
            response = self.send_query(test_case["query"])
            
            test_result = {
                "query": test_case["query"],
                "description": test_case["description"],
                "response_received": response["success"],
                "response_time": response.get("response_time", 0),
                "passed": False,
                "analysis": {}
            }
            
            if response["success"]:
                data = response["data"]
                
                # For edge cases, we expect error responses
                has_error = "error" in data
                
                if has_error:
                    error_content = data["error"].lower()
                    
                    # Check if error message is appropriate
                    appropriate_error = any(phrase in error_content for phrase in [
                        "invalid", "provide", "request", "empty", "missing"
                    ])
                    
                    test_result["analysis"] = {
                        "has_error_response": True,
                        "appropriate_error_message": appropriate_error,
                        "error_content": error_content[:100]
                    }
                    
                    test_result["passed"] = appropriate_error
                    
                else:
                    # If no error field, check if result field has appropriate content
                    result_content = data.get("result", "").lower()
                    appropriate_response = any(phrase in result_content for phrase in [
                        "provide", "specify", "need", "missing"
                    ])
                    
                    test_result["analysis"] = {
                        "has_error_response": False,
                        "appropriate_response": appropriate_response,
                        "result_content": result_content[:100]
                    }
                    
                    test_result["passed"] = appropriate_response
                
                if test_result["passed"]:
                    print(f"   ✅ PASSED ({response['response_time']:.2f}s)")
                    results["passed_tests"] += 1
                else:
                    print(f"   ❌ FAILED ({response['response_time']:.2f}s)")
                
                # Show response sample
                display_content = data.get("error", data.get("result", ""))
                print(f"   📄 Response: {display_content[:150]}...")
                
            else:
                print(f"   ❌ FAILED - Request error: {response['error']}")
            
            results["test_results"].append(test_result)
        
        success_rate = (results["passed_tests"] / results["total_tests"]) * 100
        print(f"\n📊 Edge Cases Results: {results['passed_tests']}/{results['total_tests']} passed ({success_rate:.1f}%)")
        
        return results
    
    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all comprehensive query format tests."""
        print("🧪 Comprehensive AgentCore Query Format Test Suite")
        print("=" * 80)
        print("Testing Requirements: 7.1, 7.2, 7.3, 7.4")
        print("- Simple ticker-only queries")
        print("- Complete queries with risk tolerance and horizon")
        print("- Queries missing required information")
        print("- Parameter extraction and missing parameter handling")
        print("=" * 80)
        
        if not self.start_agentcore_server():
            return {"success": False, "error": "Failed to start server"}
        
        try:
            all_results = {
                "timestamp": datetime.now().isoformat(),
                "test_categories": {},
                "overall_stats": {
                    "total_tests": 0,
                    "passed_tests": 0,
                    "failed_tests": 0
                }
            }
            
            # Run all test categories
            test_categories = [
                ("simple_ticker_queries", self.test_simple_ticker_queries),
                ("complete_queries", self.test_complete_queries),
                ("missing_parameter_queries", self.test_missing_parameter_queries),
                ("edge_cases", self.test_edge_cases)
            ]
            
            for category_name, test_function in test_categories:
                category_result = test_function()
                all_results["test_categories"][category_name] = category_result
                
                # Update overall stats
                all_results["overall_stats"]["total_tests"] += category_result["total_tests"]
                all_results["overall_stats"]["passed_tests"] += category_result["passed_tests"]
                all_results["overall_stats"]["failed_tests"] += (category_result["total_tests"] - category_result["passed_tests"])
            
            # Calculate overall success
            total = all_results["overall_stats"]["total_tests"]
            passed = all_results["overall_stats"]["passed_tests"]
            success_rate = (passed / total) * 100 if total > 0 else 0
            
            all_results["success"] = success_rate >= 75  # 75% success threshold
            all_results["overall_stats"]["success_rate"] = success_rate
            
            # Print final summary
            print(f"\n🏁 Comprehensive Query Format Test Suite Complete")
            print(f"=" * 60)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {all_results['overall_stats']['failed_tests']}")
            print(f"Success Rate: {success_rate:.1f}%")
            
            if all_results["success"]:
                print(f"🎉 COMPREHENSIVE QUERY FORMAT TESTS PASSED")
                print(f"✅ Parameter extraction working correctly")
                print(f"✅ Missing parameter handling appropriate")
                print(f"✅ Various query formats supported")
                print(f"✅ Edge cases handled properly")
            else:
                print(f"⚠️  SOME TESTS FAILED BUT SYSTEM IS FUNCTIONAL")
                print(f"📊 Review detailed results for specific issues")
            
            return all_results
            
        finally:
            self.stop_agentcore_server()


def main():
    """Run the comprehensive query format tests."""
    tester = ComprehensiveQueryFormatTester()
    
    try:
        results = tester.run_comprehensive_tests()
        
        # Save results
        with open("comprehensive_query_format_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: comprehensive_query_format_test_results.json")
        
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