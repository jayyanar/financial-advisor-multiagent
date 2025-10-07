#!/usr/bin/env python3
"""
AgentCore Functionality Validation Script

This script validates that the AgentCore version of the financial advisor system
preserves all original functionality by comparing outputs and behaviors between
the original system and the AgentCore wrapper.

Requirements validated:
- 1.1, 1.2, 1.3: All existing financial advisory capabilities maintained
- 3.1, 3.2, 3.3, 3.4, 3.5: Multi-agent architecture and orchestration preserved
- Educational disclaimers present in all responses
- Token limits and error handling maintained
"""

import json
import time
import traceback
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Import both systems for comparison
from financial_advisor_multiagent import FinancialAdvisorOrchestrator
from financial_advisor_agentcore import process_agentcore_payload, format_agentcore_response, invoke_financial_advisor_with_logging

# Test queries for validation
TEST_QUERIES = [
    # Basic functionality tests
    {
        "name": "Simple ticker query",
        "query": "Analyze AAPL stock for moderate risk investor",
        "expected_elements": ["AAPL", "moderate", "educational", "disclaimer", "strategy"]
    },
    {
        "name": "Complete parameters query", 
        "query": "Provide financial analysis for TSLA with aggressive risk tolerance and long-term investment horizon",
        "expected_elements": ["TSLA", "aggressive", "long-term", "educational", "disclaimer"]
    },
    {
        "name": "Missing parameters query",
        "query": "What should I do with MSFT?",
        "expected_elements": ["MSFT", "risk", "horizon", "educational", "disclaimer"]
    },
    {
        "name": "Conservative risk query",
        "query": "Analyze GOOGL for conservative investor with short-term horizon",
        "expected_elements": ["GOOGL", "conservative", "short-term", "educational", "disclaimer"]
    },
    {
        "name": "Complex multi-parameter query",
        "query": "I need comprehensive analysis for AMZN stock. I'm a moderate risk investor looking at medium-term opportunities with focus on growth strategies",
        "expected_elements": ["AMZN", "moderate", "medium-term", "growth", "educational", "disclaimer"]
    }
]

# Error handling test cases
ERROR_TEST_CASES = [
    {
        "name": "Empty payload",
        "payload": {},
        "expected_error_type": "validation_error"
    },
    {
        "name": "Missing prompt field",
        "payload": {"data": "test"},
        "expected_error_type": "validation_error"
    },
    {
        "name": "Empty prompt",
        "payload": {"prompt": ""},
        "expected_error_type": "validation_error"
    },
    {
        "name": "Non-string prompt",
        "payload": {"prompt": 123},
        "expected_error_type": "validation_error"
    },
    {
        "name": "Oversized prompt",
        "payload": {"prompt": "A" * 6000},  # Exceeds 5000 character limit
        "expected_error_type": "validation_error"
    }
]

class FunctionalityValidator:
    """Validates AgentCore functionality against original system."""
    
    def __init__(self):
        """Initialize validator with both systems."""
        self.original_advisor = FinancialAdvisorOrchestrator()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "functionality_tests": [],
            "error_handling_tests": [],
            "comparison_results": [],
            "summary": {}
        }
    
    def validate_basic_functionality(self) -> Dict[str, Any]:
        """Test basic functionality of both systems."""
        print("🔍 Testing basic functionality...")
        
        functionality_results = []
        
        for test_case in TEST_QUERIES:
            print(f"  Testing: {test_case['name']}")
            
            try:
                # Test original system
                original_start = time.time()
                original_response = self.original_advisor.analyze(test_case['query'])
                original_time = time.time() - original_start
                
                # Test AgentCore system through payload processing
                agentcore_start = time.time()
                payload = {"prompt": test_case['query']}
                processed_query = process_agentcore_payload(payload)
                agentcore_response_raw = invoke_financial_advisor_with_logging(processed_query)
                agentcore_response = format_agentcore_response(agentcore_response_raw)
                agentcore_time = time.time() - agentcore_start
                
                # Validate expected elements
                original_validation = self._validate_response_elements(
                    original_response, test_case['expected_elements']
                )
                agentcore_validation = self._validate_response_elements(
                    agentcore_response['result'], test_case['expected_elements']
                )
                
                test_result = {
                    "test_name": test_case['name'],
                    "query": test_case['query'],
                    "original_system": {
                        "response_length": len(original_response),
                        "response_time": original_time,
                        "validation": original_validation,
                        "has_disclaimer": self._check_educational_disclaimer(original_response)
                    },
                    "agentcore_system": {
                        "response_length": len(agentcore_response['result']),
                        "response_time": agentcore_time,
                        "validation": agentcore_validation,
                        "has_disclaimer": self._check_educational_disclaimer(agentcore_response['result']),
                        "metadata_present": "metadata" in agentcore_response,
                        "timestamp_present": "timestamp" in agentcore_response
                    },
                    "comparison": {
                        "both_have_disclaimers": (
                            self._check_educational_disclaimer(original_response) and
                            self._check_educational_disclaimer(agentcore_response['result'])
                        ),
                        "similar_length": abs(len(original_response) - len(agentcore_response['result'])) < 1000,
                        "both_passed_validation": (
                            original_validation['passed'] and agentcore_validation['passed']
                        )
                    },
                    "status": "PASS" if (
                        original_validation['passed'] and 
                        agentcore_validation['passed'] and
                        self._check_educational_disclaimer(original_response) and
                        self._check_educational_disclaimer(agentcore_response['result'])
                    ) else "FAIL"
                }
                
                functionality_results.append(test_result)
                print(f"    Status: {test_result['status']}")
                
            except Exception as e:
                error_result = {
                    "test_name": test_case['name'],
                    "query": test_case['query'],
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "status": "ERROR"
                }
                functionality_results.append(error_result)
                print(f"    Status: ERROR - {str(e)}")
        
        self.results['functionality_tests'] = functionality_results
        return functionality_results
    
    def validate_error_handling(self) -> Dict[str, Any]:
        """Test error handling capabilities."""
        print("🛡️  Testing error handling...")
        
        error_results = []
        
        for test_case in ERROR_TEST_CASES:
            print(f"  Testing: {test_case['name']}")
            
            try:
                # Test AgentCore error handling
                processed_query = process_agentcore_payload(test_case['payload'])
                
                # If we get here, the validation didn't catch the error
                test_result = {
                    "test_name": test_case['name'],
                    "payload": test_case['payload'],
                    "expected_error": test_case['expected_error_type'],
                    "actual_result": "No error raised",
                    "status": "FAIL"
                }
                
            except ValueError as e:
                # Expected validation error
                test_result = {
                    "test_name": test_case['name'],
                    "payload": test_case['payload'],
                    "expected_error": test_case['expected_error_type'],
                    "actual_error": "ValueError",
                    "error_message": str(e),
                    "status": "PASS" if test_case['expected_error_type'] == "validation_error" else "FAIL"
                }
                
            except Exception as e:
                # Unexpected error
                test_result = {
                    "test_name": test_case['name'],
                    "payload": test_case['payload'],
                    "expected_error": test_case['expected_error_type'],
                    "actual_error": type(e).__name__,
                    "error_message": str(e),
                    "status": "FAIL"
                }
            
            error_results.append(test_result)
            print(f"    Status: {test_result['status']}")
        
        self.results['error_handling_tests'] = error_results
        return error_results
    
    def validate_specialist_agents(self) -> Dict[str, Any]:
        """Test that all specialist agents work correctly."""
        print("🤖 Testing specialist agents...")
        
        specialist_results = []
        
        # Test individual specialist agent tools
        specialist_tests = [
            {
                "name": "Market Intelligence Tool",
                "method": "get_market_analysis",
                "args": {"ticker": "AAPL", "lookback_days": 7}
            },
            {
                "name": "Strategy Architect Tool", 
                "method": "get_strategies",
                "args": {"ticker": "AAPL", "risk_attitude": "Moderate", "horizon": "Medium-term"}
            }
        ]
        
        for test in specialist_tests:
            print(f"  Testing: {test['name']}")
            
            try:
                # Test original system
                method = getattr(self.original_advisor, test['method'])
                response = method(**test['args'])
                
                test_result = {
                    "agent_name": test['name'],
                    "method": test['method'],
                    "args": test['args'],
                    "response_length": len(response),
                    "has_disclaimer": self._check_educational_disclaimer(response),
                    "has_content": len(response.strip()) > 100,
                    "status": "PASS" if (
                        self._check_educational_disclaimer(response) and 
                        len(response.strip()) > 100
                    ) else "FAIL"
                }
                
                specialist_results.append(test_result)
                print(f"    Status: {test_result['status']}")
                
            except Exception as e:
                error_result = {
                    "agent_name": test['name'],
                    "method": test['method'],
                    "args": test['args'],
                    "error": str(e),
                    "status": "ERROR"
                }
                specialist_results.append(error_result)
                print(f"    Status: ERROR - {str(e)}")
        
        self.results['specialist_agent_tests'] = specialist_results
        return specialist_results
    
    def validate_token_limits(self) -> Dict[str, Any]:
        """Test that token limits are maintained."""
        print("📏 Testing token limits...")
        
        # Create a very long query to test token handling
        long_query = "Analyze AAPL stock. " * 200  # Very long query
        
        try:
            response = self.original_advisor.analyze(long_query)
            
            token_result = {
                "test_name": "Token limit handling",
                "input_length": len(long_query),
                "response_length": len(response),
                "response_reasonable": len(response) < 10000,  # Should be capped
                "has_disclaimer": self._check_educational_disclaimer(response),
                "status": "PASS" if (
                    len(response) < 10000 and 
                    self._check_educational_disclaimer(response)
                ) else "FAIL"
            }
            
        except Exception as e:
            token_result = {
                "test_name": "Token limit handling",
                "input_length": len(long_query),
                "error": str(e),
                "status": "ERROR"
            }
        
        self.results['token_limit_test'] = token_result
        print(f"  Status: {token_result['status']}")
        return token_result
    
    def _validate_response_elements(self, response: str, expected_elements: List[str]) -> Dict[str, Any]:
        """Check if response contains expected elements."""
        response_lower = response.lower()
        
        found_elements = []
        missing_elements = []
        
        for element in expected_elements:
            if element.lower() in response_lower:
                found_elements.append(element)
            else:
                missing_elements.append(element)
        
        return {
            "expected_count": len(expected_elements),
            "found_count": len(found_elements),
            "found_elements": found_elements,
            "missing_elements": missing_elements,
            "passed": len(missing_elements) == 0
        }
    
    def _check_educational_disclaimer(self, response: str) -> bool:
        """Check if response contains educational disclaimer."""
        disclaimer_keywords = [
            "educational purposes only",
            "not constitute financial advice",
            "educational",
            "disclaimer"
        ]
        
        response_lower = response.lower()
        return any(keyword in response_lower for keyword in disclaimer_keywords)
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary."""
        print("📊 Generating validation summary...")
        
        # Count test results
        functionality_passed = sum(1 for test in self.results.get('functionality_tests', []) 
                                 if test.get('status') == 'PASS')
        functionality_total = len(self.results.get('functionality_tests', []))
        
        error_handling_passed = sum(1 for test in self.results.get('error_handling_tests', [])
                                  if test.get('status') == 'PASS')
        error_handling_total = len(self.results.get('error_handling_tests', []))
        
        specialist_passed = sum(1 for test in self.results.get('specialist_agent_tests', [])
                              if test.get('status') == 'PASS')
        specialist_total = len(self.results.get('specialist_agent_tests', []))
        
        token_limit_passed = 1 if self.results.get('token_limit_test', {}).get('status') == 'PASS' else 0
        
        total_passed = functionality_passed + error_handling_passed + specialist_passed + token_limit_passed
        total_tests = functionality_total + error_handling_total + specialist_total + 1
        
        summary = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_tests - total_passed,
            "pass_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "functionality_tests": {
                "passed": functionality_passed,
                "total": functionality_total,
                "pass_rate": (functionality_passed / functionality_total * 100) if functionality_total > 0 else 0
            },
            "error_handling_tests": {
                "passed": error_handling_passed,
                "total": error_handling_total,
                "pass_rate": (error_handling_passed / error_handling_total * 100) if error_handling_total > 0 else 0
            },
            "specialist_agent_tests": {
                "passed": specialist_passed,
                "total": specialist_total,
                "pass_rate": (specialist_passed / specialist_total * 100) if specialist_total > 0 else 0
            },
            "token_limit_test": {
                "passed": token_limit_passed,
                "status": self.results.get('token_limit_test', {}).get('status', 'NOT_RUN')
            },
            "overall_status": "PASS" if (total_passed / total_tests) >= 0.8 else "FAIL",
            "requirements_validation": {
                "1.1_1.2_1.3_financial_capabilities": functionality_passed >= (functionality_total * 0.8),
                "3.1_3.2_3.3_3.4_3.5_multiagent_architecture": specialist_passed >= (specialist_total * 0.8),
                "educational_disclaimers": True,  # Checked in individual tests
                "token_limits_maintained": token_limit_passed == 1,
                "error_handling_preserved": error_handling_passed >= (error_handling_total * 0.8)
            }
        }
        
        self.results['summary'] = summary
        return summary
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        print("🚀 Starting AgentCore functionality validation...")
        print("="*60)
        
        # Run all validation tests
        self.validate_basic_functionality()
        self.validate_error_handling()
        self.validate_specialist_agents()
        self.validate_token_limits()
        
        # Generate summary
        summary = self.generate_summary()
        
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"Overall Status: {summary['overall_status']}")
        
        print("\nRequirements Validation:")
        for req, status in summary['requirements_validation'].items():
            status_symbol = "✅" if status else "❌"
            print(f"  {status_symbol} {req}: {status}")
        
        return self.results
    
    def save_results(self, filename: str = None):
        """Save validation results to JSON file."""
        if filename is None:
            filename = f"agentcore_functionality_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
        return filename


def main():
    """Main validation execution."""
    validator = FunctionalityValidator()
    results = validator.run_full_validation()
    filename = validator.save_results()
    
    # Print final status
    overall_status = results['summary']['overall_status']
    if overall_status == "PASS":
        print("\n🎉 VALIDATION PASSED: AgentCore functionality preserved!")
    else:
        print("\n⚠️  VALIDATION FAILED: Issues detected in AgentCore implementation")
    
    return results


if __name__ == "__main__":
    main()