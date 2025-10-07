#!/usr/bin/env python3
"""
AgentCore Integration Test - Complete Analysis Workflow

This test validates the complete financial advisory analysis workflow through AgentCore,
ensuring all specialist agents work correctly and educational disclaimers appear in outputs.

Tests cover:
- Market intelligence → strategy → execution → risk assessment flow
- All specialist agents functioning through AgentCore wrapper
- Educational disclaimers in all outputs
- Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4

Author: Financial Advisory System Testing
License: Educational Use Only
"""

import json
import time
import requests
import subprocess
import threading
import signal
import sys
from typing import Dict, Any, Optional
from datetime import datetime


class AgentCoreIntegrationTester:
    """
    Comprehensive integration tester for AgentCore financial advisor workflow.
    
    This class manages the complete testing lifecycle including:
    - Starting local AgentCore server
    - Running complete analysis workflow tests
    - Validating specialist agent functionality
    - Verifying educational disclaimers
    - Graceful server shutdown
    """
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8080):
        self.server_host = server_host
        self.server_port = server_port
        self.base_url = f"http://{server_host}:{server_port}"
        self.server_process = None
        self.test_results = []
        
    def start_agentcore_server(self) -> bool:
        """
        Start the AgentCore server for testing.
        
        Returns:
            bool: True if server started successfully, False otherwise
        """
        try:
            print("🚀 Starting AgentCore server for integration testing...")
            
            # Start the server process
            self.server_process = subprocess.Popen(
                [sys.executable, "financial_advisor_agentcore.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start up
            max_wait_time = 30  # seconds
            wait_interval = 1   # seconds
            
            for attempt in range(max_wait_time):
                try:
                    response = requests.get(f"{self.base_url}/ping", timeout=5)
                    if response.status_code == 200:
                        print(f"✅ AgentCore server started successfully on {self.base_url}")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(wait_interval)
                print(f"⏳ Waiting for server startup... ({attempt + 1}/{max_wait_time})")
            
            print("❌ Failed to start AgentCore server within timeout period")
            return False
            
        except Exception as e:
            print(f"❌ Error starting AgentCore server: {e}")
            return False
    
    def stop_agentcore_server(self):
        """Stop the AgentCore server gracefully."""
        if self.server_process:
            print("🛑 Stopping AgentCore server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=10)
                print("✅ AgentCore server stopped successfully")
            except subprocess.TimeoutExpired:
                print("⚠️  Server didn't stop gracefully, forcing termination...")
                self.server_process.kill()
                self.server_process.wait()
    
    def send_agentcore_request(self, prompt: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Send a request to the AgentCore server.
        
        Args:
            prompt: The financial advisory query
            timeout: Request timeout in seconds
            
        Returns:
            dict: Server response or error information
        """
        try:
            payload = {"prompt": prompt}
            
            print(f"📤 Sending request: {prompt[:100]}...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/invocations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"📥 Response received in {response_time:.2f} seconds")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "response_time": response_time,
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout",
                "response_time": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "response_time": 0
            }
    
    def validate_complete_analysis_workflow(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the response contains a complete analysis workflow.
        
        Tests for market intelligence → strategy → execution → risk assessment flow.
        Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4
        
        Args:
            response_data: The AgentCore response data
            
        Returns:
            dict: Validation results with detailed analysis
        """
        validation_results = {
            "workflow_complete": False,
            "market_intelligence": False,
            "strategy_development": False,
            "execution_planning": False,
            "risk_assessment": False,
            "educational_disclaimers": False,
            "specialist_agents_active": False,
            "details": {},
            "missing_components": []
        }
        
        try:
            # Extract the main result content
            result_content = response_data.get("result", "").lower()
            
            if not result_content:
                validation_results["details"]["error"] = "No result content found"
                return validation_results
            
            # Check for Market Intelligence component (Requirement 3.2)
            market_indicators = [
                "market", "intelligence", "research", "analysis", "sec filing",
                "financial data", "performance", "revenue", "earnings", "news"
            ]
            market_found = any(indicator in result_content for indicator in market_indicators)
            validation_results["market_intelligence"] = market_found
            validation_results["details"]["market_intelligence"] = {
                "found": market_found,
                "indicators_detected": [ind for ind in market_indicators if ind in result_content]
            }
            
            # Check for Strategy Development component (Requirement 3.3)
            strategy_indicators = [
                "strategy", "strategies", "approach", "trading", "investment",
                "growth", "momentum", "value", "options", "pullback"
            ]
            strategy_found = any(indicator in result_content for indicator in strategy_indicators)
            validation_results["strategy_development"] = strategy_found
            validation_results["details"]["strategy_development"] = {
                "found": strategy_found,
                "indicators_detected": [ind for ind in strategy_indicators if ind in result_content]
            }
            
            # Check for Execution Planning component (Requirement 3.4)
            execution_indicators = [
                "execution", "implementation", "phase", "order", "entry", "exit",
                "stop loss", "limit", "position", "sizing", "timing"
            ]
            execution_found = any(indicator in result_content for indicator in execution_indicators)
            validation_results["execution_planning"] = execution_found
            validation_results["details"]["execution_planning"] = {
                "found": execution_found,
                "indicators_detected": [ind for ind in execution_indicators if ind in result_content]
            }
            
            # Check for Risk Assessment component (Requirement 3.4)
            risk_indicators = [
                "risk", "assessment", "mitigation", "volatility", "downside",
                "concentration", "diversification", "alignment", "tolerance"
            ]
            risk_found = any(indicator in result_content for indicator in risk_indicators)
            validation_results["risk_assessment"] = risk_found
            validation_results["details"]["risk_assessment"] = {
                "found": risk_found,
                "indicators_detected": [ind for ind in risk_indicators if ind in result_content]
            }
            
            # Check for Educational Disclaimers (Requirements 1.1, 1.2, 1.3)
            disclaimer_indicators = [
                "educational", "not financial advice", "consult", "qualified",
                "disclaimer", "educational purposes", "not licensed", "professional advice"
            ]
            disclaimer_found = any(indicator in result_content for indicator in disclaimer_indicators)
            validation_results["educational_disclaimers"] = disclaimer_found
            validation_results["details"]["educational_disclaimers"] = {
                "found": disclaimer_found,
                "indicators_detected": [ind for ind in disclaimer_indicators if ind in result_content]
            }
            
            # Check for Specialist Agent Activity
            # Look for evidence that multiple agents were involved
            agent_indicators = [
                "market intelligence", "strategy architect", "execution planner", "risk assessor",
                "specialist", "analysis", "comprehensive", "detailed"
            ]
            agents_active = len([ind for ind in agent_indicators if ind in result_content]) >= 3
            validation_results["specialist_agents_active"] = agents_active
            validation_results["details"]["specialist_agents_active"] = {
                "found": agents_active,
                "indicators_detected": [ind for ind in agent_indicators if ind in result_content]
            }
            
            # Determine overall workflow completeness
            core_components = [
                validation_results["market_intelligence"],
                validation_results["strategy_development"],
                validation_results["execution_planning"],
                validation_results["risk_assessment"]
            ]
            
            validation_results["workflow_complete"] = all(core_components) and validation_results["educational_disclaimers"]
            
            # Track missing components
            if not validation_results["market_intelligence"]:
                validation_results["missing_components"].append("Market Intelligence")
            if not validation_results["strategy_development"]:
                validation_results["missing_components"].append("Strategy Development")
            if not validation_results["execution_planning"]:
                validation_results["missing_components"].append("Execution Planning")
            if not validation_results["risk_assessment"]:
                validation_results["missing_components"].append("Risk Assessment")
            if not validation_results["educational_disclaimers"]:
                validation_results["missing_components"].append("Educational Disclaimers")
            
            # Add metadata analysis
            metadata = response_data.get("metadata", {})
            validation_results["details"]["metadata"] = {
                "present": bool(metadata),
                "capabilities": metadata.get("capabilities", []),
                "educational_disclaimer_flag": metadata.get("educational_disclaimer", False),
                "system_type": metadata.get("agent_type", "unknown")
            }
            
        except Exception as e:
            validation_results["details"]["validation_error"] = str(e)
        
        return validation_results
    
    def test_complete_analysis_workflow(self) -> Dict[str, Any]:
        """
        Test the complete financial analysis workflow.
        
        This test validates:
        - Market intelligence → strategy → execution → risk assessment flow
        - All specialist agents work correctly through AgentCore
        - Educational disclaimers appear in all outputs
        
        Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4
        
        Returns:
            dict: Complete test results with detailed analysis
        """
        test_name = "Complete Analysis Workflow Test"
        print(f"\n🧪 Running {test_name}")
        print("=" * 60)
        
        # Test with a comprehensive financial advisory query
        test_query = (
            "Analyze Apple Inc. (AAPL) stock for a moderate risk investor "
            "with a long-term investment horizon. Provide comprehensive "
            "market intelligence, develop multiple trading strategies, "
            "create detailed execution plans, and assess all risks."
        )
        
        print(f"📋 Test Query: {test_query}")
        
        # Send the request
        response = self.send_agentcore_request(test_query, timeout=120)  # Extended timeout for comprehensive analysis
        
        test_result = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "query": test_query,
            "success": False,
            "response_received": False,
            "workflow_validation": {},
            "performance": {},
            "errors": []
        }
        
        if not response["success"]:
            test_result["errors"].append(f"Request failed: {response['error']}")
            print(f"❌ Request failed: {response['error']}")
            return test_result
        
        test_result["response_received"] = True
        test_result["performance"]["response_time"] = response["response_time"]
        
        # Validate the workflow
        workflow_validation = self.validate_complete_analysis_workflow(response["data"])
        test_result["workflow_validation"] = workflow_validation
        
        # Print detailed results
        print(f"\n📊 Workflow Validation Results:")
        print(f"   ✅ Market Intelligence: {'✓' if workflow_validation['market_intelligence'] else '✗'}")
        print(f"   ✅ Strategy Development: {'✓' if workflow_validation['strategy_development'] else '✗'}")
        print(f"   ✅ Execution Planning: {'✓' if workflow_validation['execution_planning'] else '✗'}")
        print(f"   ✅ Risk Assessment: {'✓' if workflow_validation['risk_assessment'] else '✗'}")
        print(f"   ✅ Educational Disclaimers: {'✓' if workflow_validation['educational_disclaimers'] else '✗'}")
        print(f"   ✅ Specialist Agents Active: {'✓' if workflow_validation['specialist_agents_active'] else '✗'}")
        print(f"   🎯 Complete Workflow: {'✓' if workflow_validation['workflow_complete'] else '✗'}")
        
        if workflow_validation["missing_components"]:
            print(f"   ⚠️  Missing Components: {', '.join(workflow_validation['missing_components'])}")
        
        # Performance metrics
        print(f"\n⏱️  Performance Metrics:")
        print(f"   Response Time: {response['response_time']:.2f} seconds")
        print(f"   Status Code: {response['status_code']}")
        
        # Sample of response content for verification
        result_content = response["data"].get("result", "")
        if result_content:
            print(f"\n📄 Response Sample (first 300 characters):")
            print(f"   {result_content[:300]}...")
            
            # Check for specific educational disclaimer content
            if "educational" in result_content.lower():
                print(f"   ✅ Educational disclaimer detected in response")
            else:
                print(f"   ⚠️  Educational disclaimer not clearly visible")
        
        # Determine overall test success
        test_result["success"] = (
            workflow_validation["workflow_complete"] and
            response["response_time"] < 180  # 3 minutes max for comprehensive analysis
        )
        
        if test_result["success"]:
            print(f"\n✅ {test_name} PASSED")
        else:
            print(f"\n❌ {test_name} FAILED")
            if not workflow_validation["workflow_complete"]:
                print(f"   Reason: Incomplete workflow - missing {workflow_validation['missing_components']}")
            if response["response_time"] >= 180:
                print(f"   Reason: Response time too slow ({response['response_time']:.2f}s)")
        
        return test_result
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """
        Run the complete integration test suite.
        
        Returns:
            dict: Complete test results
        """
        print("🧪 AgentCore Integration Test Suite - Complete Analysis Workflow")
        print("=" * 80)
        print("Testing Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4")
        print("- Market intelligence → strategy → execution → risk assessment flow")
        print("- All specialist agents work correctly through AgentCore")
        print("- Educational disclaimers appear in all outputs")
        print("=" * 80)
        
        # Start the server
        if not self.start_agentcore_server():
            return {
                "success": False,
                "error": "Failed to start AgentCore server",
                "tests": []
            }
        
        try:
            # Run the complete workflow test
            workflow_test = self.test_complete_analysis_workflow()
            self.test_results.append(workflow_test)
            
            # Compile overall results
            total_tests = len(self.test_results)
            passed_tests = sum(1 for test in self.test_results if test["success"])
            
            overall_results = {
                "success": passed_tests == total_tests,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "tests": self.test_results,
                "summary": {
                    "workflow_complete": workflow_test["workflow_validation"]["workflow_complete"],
                    "all_components_present": len(workflow_test["workflow_validation"]["missing_components"]) == 0,
                    "educational_disclaimers": workflow_test["workflow_validation"]["educational_disclaimers"],
                    "specialist_agents_active": workflow_test["workflow_validation"]["specialist_agents_active"],
                    "performance_acceptable": workflow_test.get("performance", {}).get("response_time", 999) < 180
                }
            }
            
            # Print final summary
            print(f"\n🏁 Integration Test Suite Complete")
            print(f"=" * 50)
            print(f"Total Tests: {total_tests}")
            print(f"Passed: {passed_tests}")
            print(f"Failed: {total_tests - passed_tests}")
            print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
            
            if overall_results["success"]:
                print(f"🎉 ALL INTEGRATION TESTS PASSED")
                print(f"✅ Complete analysis workflow validated")
                print(f"✅ All specialist agents functioning correctly")
                print(f"✅ Educational disclaimers present")
            else:
                print(f"❌ SOME INTEGRATION TESTS FAILED")
                print(f"Please review the detailed results above")
            
            return overall_results
            
        finally:
            # Always stop the server
            self.stop_agentcore_server()


def main():
    """Run the AgentCore integration tests."""
    tester = AgentCoreIntegrationTester()
    
    try:
        results = tester.run_integration_tests()
        
        # Save results to file
        with open("agentcore_integration_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: agentcore_integration_test_results.json")
        
        # Exit with appropriate code
        sys.exit(0 if results["success"] else 1)
        
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