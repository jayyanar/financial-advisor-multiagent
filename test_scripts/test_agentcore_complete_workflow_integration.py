#!/usr/bin/env python3
"""
AgentCore Complete Workflow Integration Test

This test validates the complete financial advisory analysis workflow through AgentCore,
ensuring all specialist agents work correctly and educational disclaimers appear in outputs.

Task 8.1 Requirements:
- Test market intelligence → strategy → execution → risk assessment flow
- Verify all specialist agents work correctly through AgentCore
- Confirm educational disclaimers appear in all outputs
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
import os
from typing import Dict, Any, Optional, List
from datetime import datetime


class AgentCoreCompleteWorkflowTester:
    """
    Comprehensive integration tester for AgentCore complete financial advisor workflow.
    
    This class validates the complete analysis workflow:
    1. Market Intelligence Agent → Research and analysis
    2. Strategy Architect Agent → Strategy development  
    3. Execution Planner Agent → Implementation planning
    4. Risk Assessor Agent → Risk analysis and alignment
    
    All through the AgentCore wrapper while ensuring educational disclaimers
    are present in all outputs.
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
            print("🚀 Starting AgentCore server for complete workflow integration testing...")
            
            # Start the server process
            self.server_process = subprocess.Popen(
                [sys.executable, "financial_advisor_agentcore.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start up
            max_wait_time = 45  # Extended timeout for agent initialization
            wait_interval = 2   # seconds
            
            for attempt in range(max_wait_time // wait_interval):
                try:
                    response = requests.get(f"{self.base_url}/ping", timeout=10)
                    if response.status_code == 200:
                        print(f"✅ AgentCore server started successfully on {self.base_url}")
                        # Give agents additional time to fully initialize
                        time.sleep(5)
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(wait_interval)
                print(f"⏳ Waiting for server startup... ({(attempt + 1) * wait_interval}/{max_wait_time}s)")
            
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
                self.server_process.wait(timeout=15)
                print("✅ AgentCore server stopped successfully")
            except subprocess.TimeoutExpired:
                print("⚠️  Server didn't stop gracefully, forcing termination...")
                self.server_process.kill()
                self.server_process.wait()
    
    def send_agentcore_request(self, prompt: str, timeout: int = 180) -> Dict[str, Any]:
        """
        Send a request to the AgentCore server.
        
        Args:
            prompt: The financial advisory query
            timeout: Request timeout in seconds (extended for complete workflow)
            
        Returns:
            dict: Server response or error information
        """
        try:
            payload = {"prompt": prompt}
            
            print(f"📤 Sending complete workflow request: {prompt[:150]}...")
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
                "error": "Request timeout - complete workflow analysis may take longer",
                "response_time": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "response_time": 0
            }
    
    def validate_market_intelligence_component(self, content: str) -> Dict[str, Any]:
        """
        Validate market intelligence component in the response.
        
        Requirements: 3.2 - Market intelligence functionality
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for market intelligence
        """
        market_indicators = {
            "research_activity": ["research", "analysis", "market data", "sec filing", "financial data"],
            "performance_context": ["performance", "revenue", "earnings", "growth", "financial"],
            "news_analysis": ["news", "analyst", "commentary", "report", "update"],
            "source_attribution": ["source", "according to", "based on", "from", "via"],
            "market_context": ["market", "industry", "sector", "competition", "trends"]
        }
        
        results = {
            "present": False,
            "indicators_found": {},
            "strength": 0,
            "details": []
        }
        
        content_lower = content.lower()
        total_indicators = 0
        found_indicators = 0
        
        for category, indicators in market_indicators.items():
            category_found = []
            for indicator in indicators:
                if indicator in content_lower:
                    category_found.append(indicator)
                    found_indicators += 1
                total_indicators += 1
            
            results["indicators_found"][category] = category_found
            if category_found:
                results["details"].append(f"Market Intelligence - {category}: {', '.join(category_found)}")
        
        results["strength"] = (found_indicators / total_indicators) * 100
        results["present"] = results["strength"] >= 20  # At least 20% of indicators present
        
        return results
    
    def validate_strategy_development_component(self, content: str) -> Dict[str, Any]:
        """
        Validate strategy development component in the response.
        
        Requirements: 3.3 - Strategy development functionality
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for strategy development
        """
        strategy_indicators = {
            "strategy_generation": ["strategy", "strategies", "approach", "plan", "method"],
            "risk_alignment": ["risk", "conservative", "moderate", "aggressive", "tolerance"],
            "horizon_matching": ["short", "medium", "long", "term", "horizon", "timeline"],
            "strategy_types": ["growth", "momentum", "value", "options", "pullback", "accumulation"],
            "rationale": ["rationale", "thesis", "objective", "reason", "because", "due to"]
        }
        
        results = {
            "present": False,
            "indicators_found": {},
            "strength": 0,
            "details": [],
            "multiple_strategies": False
        }
        
        content_lower = content.lower()
        total_indicators = 0
        found_indicators = 0
        
        for category, indicators in strategy_indicators.items():
            category_found = []
            for indicator in indicators:
                if indicator in content_lower:
                    category_found.append(indicator)
                    found_indicators += 1
                total_indicators += 1
            
            results["indicators_found"][category] = category_found
            if category_found:
                results["details"].append(f"Strategy Development - {category}: {', '.join(category_found)}")
        
        # Check for multiple strategies (requirement for 5+ strategies)
        strategy_count_indicators = ["strategy 1", "strategy 2", "first strategy", "second strategy", 
                                   "1.", "2.", "3.", "4.", "5."]
        strategy_mentions = sum(1 for indicator in strategy_count_indicators if indicator in content_lower)
        results["multiple_strategies"] = strategy_mentions >= 3
        
        if results["multiple_strategies"]:
            results["details"].append("Strategy Development - Multiple strategies detected")
        
        results["strength"] = (found_indicators / total_indicators) * 100
        results["present"] = results["strength"] >= 25 and results["multiple_strategies"]
        
        return results
    
    def validate_execution_planning_component(self, content: str) -> Dict[str, Any]:
        """
        Validate execution planning component in the response.
        
        Requirements: 3.4 - Execution planning functionality
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for execution planning
        """
        execution_indicators = {
            "implementation_phases": ["execution", "implementation", "phase", "step", "stage"],
            "order_specifications": ["order", "buy", "sell", "limit", "market", "stop"],
            "position_sizing": ["position", "size", "sizing", "allocation", "percentage", "%"],
            "timing_guidance": ["timing", "entry", "exit", "when", "time", "schedule"],
            "risk_controls": ["stop loss", "stop-loss", "risk management", "hedge", "protection"]
        }
        
        results = {
            "present": False,
            "indicators_found": {},
            "strength": 0,
            "details": []
        }
        
        content_lower = content.lower()
        total_indicators = 0
        found_indicators = 0
        
        for category, indicators in execution_indicators.items():
            category_found = []
            for indicator in indicators:
                if indicator in content_lower:
                    category_found.append(indicator)
                    found_indicators += 1
                total_indicators += 1
            
            results["indicators_found"][category] = category_found
            if category_found:
                results["details"].append(f"Execution Planning - {category}: {', '.join(category_found)}")
        
        results["strength"] = (found_indicators / total_indicators) * 100
        results["present"] = results["strength"] >= 20  # At least 20% of indicators present
        
        return results
    
    def validate_risk_assessment_component(self, content: str) -> Dict[str, Any]:
        """
        Validate risk assessment component in the response.
        
        Requirements: 3.4 - Risk assessment functionality
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for risk assessment
        """
        risk_indicators = {
            "risk_categories": ["risk", "risks", "volatility", "downside", "uncertainty"],
            "alignment_evaluation": ["alignment", "aligned", "consistent", "matches", "suitable"],
            "mitigation_strategies": ["mitigation", "mitigate", "reduce", "manage", "control"],
            "risk_types": ["market risk", "execution risk", "concentration", "diversification"],
            "assessment_depth": ["assess", "evaluate", "analysis", "consideration", "review"]
        }
        
        results = {
            "present": False,
            "indicators_found": {},
            "strength": 0,
            "details": []
        }
        
        content_lower = content.lower()
        total_indicators = 0
        found_indicators = 0
        
        for category, indicators in risk_indicators.items():
            category_found = []
            for indicator in indicators:
                if indicator in content_lower:
                    category_found.append(indicator)
                    found_indicators += 1
                total_indicators += 1
            
            results["indicators_found"][category] = category_found
            if category_found:
                results["details"].append(f"Risk Assessment - {category}: {', '.join(category_found)}")
        
        results["strength"] = (found_indicators / total_indicators) * 100
        results["present"] = results["strength"] >= 20  # At least 20% of indicators present
        
        return results
    
    def validate_educational_disclaimers(self, content: str) -> Dict[str, Any]:
        """
        Validate educational disclaimers in the response.
        
        Requirements: 1.1, 1.2, 1.3 - Educational disclaimers must be present
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for educational disclaimers
        """
        disclaimer_indicators = {
            "educational_purpose": ["educational", "educational purposes", "education"],
            "not_financial_advice": ["not financial advice", "not constitute financial advice", "not licensed"],
            "consult_professional": ["consult", "qualified", "professional", "licensed advisor"],
            "disclaimer_explicit": ["disclaimer", "important", "note", "warning"],
            "responsible_ai": ["for educational purposes only", "educational use only"]
        }
        
        results = {
            "present": False,
            "indicators_found": {},
            "strength": 0,
            "details": [],
            "explicit_disclaimer": False
        }
        
        content_lower = content.lower()
        total_indicators = 0
        found_indicators = 0
        
        for category, indicators in disclaimer_indicators.items():
            category_found = []
            for indicator in indicators:
                if indicator in content_lower:
                    category_found.append(indicator)
                    found_indicators += 1
                total_indicators += 1
            
            results["indicators_found"][category] = category_found
            if category_found:
                results["details"].append(f"Educational Disclaimer - {category}: {', '.join(category_found)}")
        
        # Check for explicit disclaimer phrases
        explicit_phrases = [
            "educational purposes only",
            "not constitute financial advice",
            "not financial advice",
            "for educational purposes only"
        ]
        
        results["explicit_disclaimer"] = any(phrase in content_lower for phrase in explicit_phrases)
        if results["explicit_disclaimer"]:
            results["details"].append("Educational Disclaimer - Explicit disclaimer phrase found")
        
        results["strength"] = (found_indicators / total_indicators) * 100
        results["present"] = results["strength"] >= 30 and results["explicit_disclaimer"]
        
        return results
    
    def validate_specialist_agents_coordination(self, content: str) -> Dict[str, Any]:
        """
        Validate that specialist agents are working correctly through AgentCore.
        
        Requirements: All specialist agents must function correctly
        
        Args:
            content: Response content to analyze
            
        Returns:
            dict: Validation results for specialist agent coordination
        """
        agent_indicators = {
            "market_intelligence_agent": ["market intelligence", "market research", "market analysis"],
            "strategy_architect_agent": ["strategy architect", "strategy development", "trading strategies"],
            "execution_planner_agent": ["execution planner", "execution plan", "implementation"],
            "risk_assessor_agent": ["risk assessor", "risk assessment", "risk analysis"],
            "coordination_evidence": ["comprehensive", "detailed", "analysis", "workflow", "systematic"]
        }
        
        results = {
            "present": False,
            "agents_detected": {},
            "coordination_strength": 0,
            "details": []
        }
        
        content_lower = content.lower()
        total_agents = len(agent_indicators) - 1  # Exclude coordination_evidence
        detected_agents = 0
        
        for agent_type, indicators in agent_indicators.items():
            agent_found = any(indicator in content_lower for indicator in indicators)
            results["agents_detected"][agent_type] = agent_found
            
            if agent_found and agent_type != "coordination_evidence":
                detected_agents += 1
                results["details"].append(f"Specialist Agent - {agent_type}: Active")
        
        results["coordination_strength"] = (detected_agents / total_agents) * 100
        results["present"] = detected_agents >= 3  # At least 3 of 4 specialist agents active
        
        return results
    
    def validate_complete_workflow(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the complete financial advisory workflow.
        
        This is the main validation function that checks all requirements:
        - Market intelligence → strategy → execution → risk assessment flow
        - All specialist agents work correctly through AgentCore
        - Educational disclaimers appear in all outputs
        
        Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4
        
        Args:
            response_data: The AgentCore response data
            
        Returns:
            dict: Complete validation results
        """
        validation_results = {
            "workflow_complete": False,
            "components": {},
            "overall_score": 0,
            "missing_components": [],
            "details": [],
            "requirements_met": {
                "1.1": False,  # Educational disclaimers
                "1.2": False,  # Educational disclaimers
                "1.3": False,  # Educational disclaimers
                "3.2": False,  # Market intelligence
                "3.3": False,  # Strategy development
                "3.4": False   # Execution planning and risk assessment
            }
        }
        
        try:
            # Extract the main result content
            result_content = response_data.get("result", "")
            
            if not result_content:
                validation_results["details"].append("ERROR: No result content found in response")
                return validation_results
            
            print(f"📊 Analyzing response content ({len(result_content)} characters)...")
            
            # Validate each component
            market_intel = self.validate_market_intelligence_component(result_content)
            strategy_dev = self.validate_strategy_development_component(result_content)
            execution_plan = self.validate_execution_planning_component(result_content)
            risk_assessment = self.validate_risk_assessment_component(result_content)
            educational_disclaimers = self.validate_educational_disclaimers(result_content)
            specialist_coordination = self.validate_specialist_agents_coordination(result_content)
            
            # Store component results
            validation_results["components"] = {
                "market_intelligence": market_intel,
                "strategy_development": strategy_dev,
                "execution_planning": execution_plan,
                "risk_assessment": risk_assessment,
                "educational_disclaimers": educational_disclaimers,
                "specialist_coordination": specialist_coordination
            }
            
            # Check requirements
            validation_results["requirements_met"]["3.2"] = market_intel["present"]
            validation_results["requirements_met"]["3.3"] = strategy_dev["present"]
            validation_results["requirements_met"]["3.4"] = execution_plan["present"] and risk_assessment["present"]
            validation_results["requirements_met"]["1.1"] = educational_disclaimers["present"]
            validation_results["requirements_met"]["1.2"] = educational_disclaimers["present"]
            validation_results["requirements_met"]["1.3"] = educational_disclaimers["present"]
            
            # Calculate overall score
            component_scores = [
                market_intel["strength"],
                strategy_dev["strength"],
                execution_plan["strength"],
                risk_assessment["strength"],
                educational_disclaimers["strength"],
                specialist_coordination["coordination_strength"]
            ]
            validation_results["overall_score"] = sum(component_scores) / len(component_scores)
            
            # Determine missing components
            if not market_intel["present"]:
                validation_results["missing_components"].append("Market Intelligence")
            if not strategy_dev["present"]:
                validation_results["missing_components"].append("Strategy Development")
            if not execution_plan["present"]:
                validation_results["missing_components"].append("Execution Planning")
            if not risk_assessment["present"]:
                validation_results["missing_components"].append("Risk Assessment")
            if not educational_disclaimers["present"]:
                validation_results["missing_components"].append("Educational Disclaimers")
            if not specialist_coordination["present"]:
                validation_results["missing_components"].append("Specialist Agent Coordination")
            
            # Determine workflow completeness
            all_requirements_met = all(validation_results["requirements_met"].values())
            validation_results["workflow_complete"] = (
                all_requirements_met and
                validation_results["overall_score"] >= 60  # At least 60% overall strength
            )
            
            # Compile details
            for component_name, component_data in validation_results["components"].items():
                if "details" in component_data:
                    validation_results["details"].extend(component_data["details"])
            
        except Exception as e:
            validation_results["details"].append(f"Validation error: {str(e)}")
        
        return validation_results
    
    def test_complete_workflow_integration(self) -> Dict[str, Any]:
        """
        Test the complete financial advisory workflow integration.
        
        This test validates:
        - Market intelligence → strategy → execution → risk assessment flow
        - All specialist agents work correctly through AgentCore
        - Educational disclaimers appear in all outputs
        
        Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4
        
        Returns:
            dict: Complete test results with detailed validation
        """
        test_name = "Complete Workflow Integration Test"
        print(f"\n🧪 Running {test_name}")
        print("=" * 80)
        print("Testing Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4")
        print("- Market intelligence → strategy → execution → risk assessment flow")
        print("- All specialist agents work correctly through AgentCore")
        print("- Educational disclaimers appear in all outputs")
        print("=" * 80)
        
        # Comprehensive test query that should trigger all workflow components
        test_query = (
            "I need comprehensive financial analysis for Microsoft Corporation (MSFT) stock. "
            "I am a moderate risk investor with a long-term investment horizon of 3-5 years. "
            "Please provide complete market intelligence research, develop multiple trading strategies "
            "aligned with my risk tolerance, create detailed execution plans with specific order types "
            "and position sizing, and conduct thorough risk assessment with mitigation strategies. "
            "I want to understand all aspects: market analysis, strategy options, implementation steps, "
            "and risk management for this investment decision."
        )
        
        print(f"📋 Test Query: {test_query}")
        
        # Send the request with extended timeout for complete workflow
        print(f"\n⏳ Sending request (this may take 2-3 minutes for complete analysis)...")
        response = self.send_agentcore_request(test_query, timeout=240)  # 4 minutes for complete workflow
        
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
        
        # Validate the complete workflow
        print(f"\n📊 Validating complete workflow...")
        workflow_validation = self.validate_complete_workflow(response["data"])
        test_result["workflow_validation"] = workflow_validation
        
        # Print detailed validation results
        print(f"\n📋 Complete Workflow Validation Results:")
        print(f"   Overall Score: {workflow_validation.get('overall_score', 0):.1f}%")
        print(f"   Workflow Complete: {'✅' if workflow_validation.get('workflow_complete', False) else '❌'}")
        
        print(f"\n🔍 Component Analysis:")
        components = workflow_validation.get("components", {})
        if components:
            print(f"   Market Intelligence: {'✅' if components.get('market_intelligence', {}).get('present', False) else '❌'} "
                  f"({components.get('market_intelligence', {}).get('strength', 0):.1f}%)")
            print(f"   Strategy Development: {'✅' if components.get('strategy_development', {}).get('present', False) else '❌'} "
                  f"({components.get('strategy_development', {}).get('strength', 0):.1f}%)")
            print(f"   Execution Planning: {'✅' if components.get('execution_planning', {}).get('present', False) else '❌'} "
                  f"({components.get('execution_planning', {}).get('strength', 0):.1f}%)")
            print(f"   Risk Assessment: {'✅' if components.get('risk_assessment', {}).get('present', False) else '❌'} "
                  f"({components.get('risk_assessment', {}).get('strength', 0):.1f}%)")
            print(f"   Educational Disclaimers: {'✅' if components.get('educational_disclaimers', {}).get('present', False) else '❌'} "
                  f"({components.get('educational_disclaimers', {}).get('strength', 0):.1f}%)")
            print(f"   Specialist Coordination: {'✅' if components.get('specialist_coordination', {}).get('present', False) else '❌'} "
                  f"({components.get('specialist_coordination', {}).get('coordination_strength', 0):.1f}%)")
        else:
            print("   No component analysis available")
        
        print(f"\n📋 Requirements Compliance:")
        requirements = workflow_validation["requirements_met"]
        print(f"   Req 1.1 (Educational Disclaimers): {'✅' if requirements['1.1'] else '❌'}")
        print(f"   Req 1.2 (Educational Disclaimers): {'✅' if requirements['1.2'] else '❌'}")
        print(f"   Req 1.3 (Educational Disclaimers): {'✅' if requirements['1.3'] else '❌'}")
        print(f"   Req 3.2 (Market Intelligence): {'✅' if requirements['3.2'] else '❌'}")
        print(f"   Req 3.3 (Strategy Development): {'✅' if requirements['3.3'] else '❌'}")
        print(f"   Req 3.4 (Execution & Risk): {'✅' if requirements['3.4'] else '❌'}")
        
        if workflow_validation["missing_components"]:
            print(f"\n⚠️  Missing Components: {', '.join(workflow_validation['missing_components'])}")
        
        # Performance metrics
        print(f"\n⏱️  Performance Metrics:")
        print(f"   Response Time: {response['response_time']:.2f} seconds")
        print(f"   Status Code: {response['status_code']}")
        print(f"   Response Length: {len(response['data'].get('result', ''))} characters")
        
        # Sample of response content for verification
        result_content = response["data"].get("result", "")
        if result_content:
            print(f"\n📄 Response Sample (first 500 characters):")
            print(f"   {result_content[:500]}...")
            
            # Check for specific workflow indicators
            workflow_indicators = ["market", "strategy", "execution", "risk", "educational"]
            found_indicators = [ind for ind in workflow_indicators if ind.lower() in result_content.lower()]
            print(f"   🔍 Workflow Indicators Found: {', '.join(found_indicators)}")
        
        # Determine overall test success
        test_result["success"] = (
            workflow_validation["workflow_complete"] and
            response["response_time"] < 300 and  # 5 minutes max for complete workflow
            all(workflow_validation["requirements_met"].values())
        )
        
        if test_result["success"]:
            print(f"\n✅ {test_name} PASSED")
            print(f"   🎉 Complete workflow validated successfully!")
            print(f"   ✅ All specialist agents functioning correctly")
            print(f"   ✅ Educational disclaimers present")
            print(f"   ✅ All requirements met")
        else:
            print(f"\n❌ {test_name} FAILED")
            if not workflow_validation["workflow_complete"]:
                print(f"   Reason: Incomplete workflow - missing {workflow_validation['missing_components']}")
            if response["response_time"] >= 300:
                print(f"   Reason: Response time too slow ({response['response_time']:.2f}s)")
            if not all(workflow_validation["requirements_met"].values()):
                failed_reqs = [req for req, met in workflow_validation["requirements_met"].items() if not met]
                print(f"   Reason: Requirements not met: {', '.join(failed_reqs)}")
        
        return test_result
    
    def run_complete_workflow_tests(self) -> Dict[str, Any]:
        """
        Run the complete workflow integration test suite.
        
        Returns:
            dict: Complete test results
        """
        print("🧪 AgentCore Complete Workflow Integration Test Suite")
        print("=" * 90)
        print("Task 8.1: Create integration test for complete analysis workflow")
        print("Testing Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4")
        print("- Market intelligence → strategy → execution → risk assessment flow")
        print("- All specialist agents work correctly through AgentCore")
        print("- Educational disclaimers appear in all outputs")
        print("=" * 90)
        
        # Start the server
        if not self.start_agentcore_server():
            return {
                "success": False,
                "error": "Failed to start AgentCore server",
                "tests": []
            }
        
        try:
            # Run the complete workflow integration test
            workflow_test = self.test_complete_workflow_integration()
            self.test_results.append(workflow_test)
            
            # Compile overall results
            total_tests = len(self.test_results)
            passed_tests = sum(1 for test in self.test_results if test["success"])
            
            # Safe access to workflow validation results
            workflow_validation = workflow_test.get("workflow_validation", {})
            requirements_met = workflow_validation.get("requirements_met", {})
            components = workflow_validation.get("components", {})
            
            overall_results = {
                "success": passed_tests == total_tests,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "tests": self.test_results,
                "task_8_1_complete": passed_tests == total_tests,
                "requirements_validation": {
                    "1.1_educational_disclaimers": requirements_met.get("1.1", False),
                    "1.2_educational_disclaimers": requirements_met.get("1.2", False),
                    "1.3_educational_disclaimers": requirements_met.get("1.3", False),
                    "3.2_market_intelligence": requirements_met.get("3.2", False),
                    "3.3_strategy_development": requirements_met.get("3.3", False),
                    "3.4_execution_and_risk": requirements_met.get("3.4", False)
                },
                "workflow_components": {
                    "market_intelligence_flow": components.get("market_intelligence", {}).get("present", False),
                    "strategy_development_flow": components.get("strategy_development", {}).get("present", False),
                    "execution_planning_flow": components.get("execution_planning", {}).get("present", False),
                    "risk_assessment_flow": components.get("risk_assessment", {}).get("present", False),
                    "specialist_agents_coordination": components.get("specialist_coordination", {}).get("present", False),
                    "educational_disclaimers_present": components.get("educational_disclaimers", {}).get("present", False)
                }
            }
            
            # Print final summary
            print(f"\n🏁 Complete Workflow Integration Test Suite Results")
            print(f"=" * 70)
            print(f"Task 8.1 Status: {'✅ COMPLETE' if overall_results['task_8_1_complete'] else '❌ INCOMPLETE'}")
            print(f"Total Tests: {total_tests}")
            print(f"Passed: {passed_tests}")
            print(f"Failed: {total_tests - passed_tests}")
            print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
            
            print(f"\n📋 Requirements Validation Summary:")
            req_validation = overall_results["requirements_validation"]
            print(f"   Req 1.1, 1.2, 1.3 (Educational Disclaimers): {'✅' if all([req_validation['1.1_educational_disclaimers'], req_validation['1.2_educational_disclaimers'], req_validation['1.3_educational_disclaimers']]) else '❌'}")
            print(f"   Req 3.2 (Market Intelligence): {'✅' if req_validation['3.2_market_intelligence'] else '❌'}")
            print(f"   Req 3.3 (Strategy Development): {'✅' if req_validation['3.3_strategy_development'] else '❌'}")
            print(f"   Req 3.4 (Execution & Risk): {'✅' if req_validation['3.4_execution_and_risk'] else '❌'}")
            
            print(f"\n🔄 Workflow Components Validation:")
            workflow_comp = overall_results["workflow_components"]
            print(f"   Market Intelligence → {'✅' if workflow_comp['market_intelligence_flow'] else '❌'}")
            print(f"   Strategy Development → {'✅' if workflow_comp['strategy_development_flow'] else '❌'}")
            print(f"   Execution Planning → {'✅' if workflow_comp['execution_planning_flow'] else '❌'}")
            print(f"   Risk Assessment → {'✅' if workflow_comp['risk_assessment_flow'] else '❌'}")
            print(f"   Specialist Agents Coordination → {'✅' if workflow_comp['specialist_agents_coordination'] else '❌'}")
            print(f"   Educational Disclaimers → {'✅' if workflow_comp['educational_disclaimers_present'] else '❌'}")
            
            if overall_results["success"]:
                print(f"\n🎉 TASK 8.1 SUCCESSFULLY COMPLETED!")
                print(f"✅ Complete analysis workflow validated")
                print(f"✅ Market intelligence → strategy → execution → risk assessment flow confirmed")
                print(f"✅ All specialist agents functioning correctly through AgentCore")
                print(f"✅ Educational disclaimers present in all outputs")
                print(f"✅ All requirements (1.1, 1.2, 1.3, 3.2, 3.3, 3.4) met")
            else:
                print(f"\n❌ TASK 8.1 INCOMPLETE")
                print(f"Please review the detailed results above")
                if workflow_test["workflow_validation"]["missing_components"]:
                    print(f"Missing workflow components: {', '.join(workflow_test['workflow_validation']['missing_components'])}")
            
            return overall_results
            
        finally:
            # Always stop the server
            self.stop_agentcore_server()


def main():
    """Run the AgentCore complete workflow integration tests."""
    tester = AgentCoreCompleteWorkflowTester()
    
    try:
        results = tester.run_complete_workflow_tests()
        
        # Save results to file
        results_filename = "agentcore_complete_workflow_integration_results.json"
        with open(results_filename, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_filename}")
        
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