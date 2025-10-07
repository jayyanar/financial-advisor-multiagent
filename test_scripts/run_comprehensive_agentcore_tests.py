#!/usr/bin/env python3
"""
Comprehensive AgentCore Testing Suite

This script runs all AgentCore testing workflows in sequence to validate
the complete system functionality, query handling, and error scenarios.

Test Suites:
1. Integration Test - Complete Analysis Workflow (Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4)
2. Query Format Tests - Various Input Formats (Requirements: 7.1, 7.2, 7.3, 7.4)
3. Error Handling Tests - Error Scenarios (Requirements: 8.1, 8.2, 8.3, 8.5)

Author: Financial Advisory System Testing
License: Educational Use Only
"""

import json
import sys
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, List


class ComprehensiveAgentCoreTester:
    """
    Orchestrates all AgentCore test suites and provides comprehensive reporting.
    """
    
    def __init__(self):
        self.test_suites = [
            {
                "name": "Integration Workflow Test",
                "script": "test_agentcore_integration_workflow.py",
                "description": "Complete analysis workflow validation",
                "requirements": ["1.1", "1.2", "1.3", "3.2", "3.3", "3.4"],
                "focus": "Market intelligence → strategy → execution → risk assessment flow"
            },
            {
                "name": "Query Format Test",
                "script": "test_agentcore_query_formats.py",
                "description": "Various input query format handling",
                "requirements": ["7.1", "7.2", "7.3", "7.4"],
                "focus": "Parameter extraction and missing parameter handling"
            },
            {
                "name": "Error Handling Test",
                "script": "test_agentcore_error_handling.py",
                "description": "Error scenarios and graceful degradation",
                "requirements": ["8.1", "8.2", "8.3", "8.5"],
                "focus": "Invalid payloads, API failures, and error responses"
            }
        ]
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_suites": len(self.test_suites),
            "suite_results": [],
            "overall_success": False,
            "summary": {}
        }
    
    def run_test_suite(self, suite_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single test suite and capture results.
        
        Args:
            suite_config: Configuration for the test suite
            
        Returns:
            dict: Test suite results
        """
        print(f"\n🚀 Running {suite_config['name']}")
        print("=" * 80)
        print(f"Description: {suite_config['description']}")
        print(f"Requirements: {', '.join(suite_config['requirements'])}")
        print(f"Focus: {suite_config['focus']}")
        print("=" * 80)
        
        suite_result = {
            "name": suite_config["name"],
            "script": suite_config["script"],
            "requirements": suite_config["requirements"],
            "start_time": datetime.now().isoformat(),
            "success": False,
            "exit_code": None,
            "execution_time": 0,
            "output": "",
            "error": ""
        }
        
        try:
            start_time = time.time()
            
            # Run the test script
            process = subprocess.run(
                [sys.executable, suite_config["script"]],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per suite
            )
            
            end_time = time.time()
            suite_result["execution_time"] = end_time - start_time
            suite_result["exit_code"] = process.returncode
            suite_result["output"] = process.stdout
            suite_result["error"] = process.stderr
            suite_result["success"] = process.returncode == 0
            
            # Print immediate results
            if suite_result["success"]:
                print(f"✅ {suite_config['name']} PASSED")
                print(f"   Execution Time: {suite_result['execution_time']:.2f} seconds")
            else:
                print(f"❌ {suite_config['name']} FAILED")
                print(f"   Exit Code: {process.returncode}")
                print(f"   Execution Time: {suite_result['execution_time']:.2f} seconds")
                if process.stderr:
                    print(f"   Error Output: {process.stderr[:200]}...")
            
        except subprocess.TimeoutExpired:
            suite_result["error"] = "Test suite timed out after 5 minutes"
            suite_result["execution_time"] = 300
            print(f"⏰ {suite_config['name']} TIMED OUT")
            
        except Exception as e:
            suite_result["error"] = str(e)
            print(f"💥 {suite_config['name']} CRASHED: {e}")
        
        suite_result["end_time"] = datetime.now().isoformat()
        return suite_result
    
    def analyze_test_results(self) -> Dict[str, Any]:
        """
        Analyze all test results and generate comprehensive summary.
        
        Returns:
            dict: Analysis summary
        """
        analysis = {
            "total_suites": len(self.results["suite_results"]),
            "passed_suites": 0,
            "failed_suites": 0,
            "timed_out_suites": 0,
            "crashed_suites": 0,
            "total_execution_time": 0,
            "requirements_coverage": {},
            "critical_failures": [],
            "performance_metrics": {}
        }
        
        # Analyze each suite result
        for suite_result in self.results["suite_results"]:
            analysis["total_execution_time"] += suite_result.get("execution_time", 0)
            
            if suite_result["success"]:
                analysis["passed_suites"] += 1
            else:
                analysis["failed_suites"] += 1
                
                # Categorize failure types
                if "timed out" in suite_result.get("error", "").lower():
                    analysis["timed_out_suites"] += 1
                elif suite_result.get("exit_code") is None:
                    analysis["crashed_suites"] += 1
                
                # Track critical failures
                analysis["critical_failures"].append({
                    "suite": suite_result["name"],
                    "error": suite_result.get("error", "Unknown error"),
                    "exit_code": suite_result.get("exit_code")
                })
            
            # Track requirements coverage
            for req in suite_result.get("requirements", []):
                if req not in analysis["requirements_coverage"]:
                    analysis["requirements_coverage"][req] = {"tested": 0, "passed": 0}
                
                analysis["requirements_coverage"][req]["tested"] += 1
                if suite_result["success"]:
                    analysis["requirements_coverage"][req]["passed"] += 1
        
        # Performance metrics
        analysis["performance_metrics"] = {
            "average_execution_time": analysis["total_execution_time"] / analysis["total_suites"] if analysis["total_suites"] > 0 else 0,
            "longest_suite": max(self.results["suite_results"], key=lambda x: x.get("execution_time", 0), default={}).get("name", "None"),
            "total_time_minutes": analysis["total_execution_time"] / 60
        }
        
        return analysis
    
    def generate_comprehensive_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a comprehensive test report.
        
        Args:
            analysis: Test analysis results
            
        Returns:
            str: Formatted report
        """
        report = []
        report.append("🧪 COMPREHENSIVE AGENTCORE TEST REPORT")
        report.append("=" * 80)
        report.append(f"Test Execution Date: {self.results['timestamp']}")
        report.append(f"Total Test Suites: {analysis['total_suites']}")
        report.append(f"Total Execution Time: {analysis['performance_metrics']['total_time_minutes']:.2f} minutes")
        report.append("")
        
        # Overall Results
        report.append("📊 OVERALL RESULTS")
        report.append("-" * 40)
        report.append(f"✅ Passed Suites: {analysis['passed_suites']}")
        report.append(f"❌ Failed Suites: {analysis['failed_suites']}")
        report.append(f"⏰ Timed Out: {analysis['timed_out_suites']}")
        report.append(f"💥 Crashed: {analysis['crashed_suites']}")
        
        success_rate = (analysis['passed_suites'] / analysis['total_suites']) * 100 if analysis['total_suites'] > 0 else 0
        report.append(f"📈 Success Rate: {success_rate:.1f}%")
        report.append("")
        
        # Suite Details
        report.append("📋 SUITE DETAILS")
        report.append("-" * 40)
        for suite_result in self.results["suite_results"]:
            status = "✅ PASSED" if suite_result["success"] else "❌ FAILED"
            report.append(f"{status} {suite_result['name']}")
            report.append(f"   Requirements: {', '.join(suite_result.get('requirements', []))}")
            report.append(f"   Execution Time: {suite_result.get('execution_time', 0):.2f}s")
            if not suite_result["success"]:
                report.append(f"   Error: {suite_result.get('error', 'Unknown error')[:100]}...")
            report.append("")
        
        # Requirements Coverage
        report.append("📋 REQUIREMENTS COVERAGE")
        report.append("-" * 40)
        for req, coverage in sorted(analysis["requirements_coverage"].items()):
            coverage_rate = (coverage["passed"] / coverage["tested"]) * 100 if coverage["tested"] > 0 else 0
            status = "✅" if coverage_rate == 100 else "⚠️" if coverage_rate >= 50 else "❌"
            report.append(f"{status} Requirement {req}: {coverage['passed']}/{coverage['tested']} ({coverage_rate:.1f}%)")
        report.append("")
        
        # Critical Failures
        if analysis["critical_failures"]:
            report.append("🚨 CRITICAL FAILURES")
            report.append("-" * 40)
            for failure in analysis["critical_failures"]:
                report.append(f"❌ {failure['suite']}")
                report.append(f"   Error: {failure['error']}")
                report.append(f"   Exit Code: {failure.get('exit_code', 'N/A')}")
                report.append("")
        
        # Performance Summary
        report.append("⏱️ PERFORMANCE SUMMARY")
        report.append("-" * 40)
        report.append(f"Total Execution Time: {analysis['performance_metrics']['total_time_minutes']:.2f} minutes")
        report.append(f"Average Suite Time: {analysis['performance_metrics']['average_execution_time']:.2f} seconds")
        report.append(f"Longest Running Suite: {analysis['performance_metrics']['longest_suite']}")
        report.append("")
        
        # Final Assessment
        report.append("🎯 FINAL ASSESSMENT")
        report.append("-" * 40)
        if success_rate == 100:
            report.append("🎉 ALL TESTS PASSED - AgentCore system is fully validated!")
            report.append("✅ Complete analysis workflow functioning correctly")
            report.append("✅ Query format handling working properly")
            report.append("✅ Error handling scenarios validated")
        elif success_rate >= 80:
            report.append("⚠️ MOSTLY SUCCESSFUL - Minor issues detected")
            report.append("Most core functionality is working correctly")
            report.append("Review failed tests for non-critical issues")
        else:
            report.append("❌ SIGNIFICANT ISSUES DETECTED")
            report.append("Multiple test suites failed - system needs attention")
            report.append("Review all failed tests before deployment")
        
        report.append("")
        report.append("📄 Detailed results available in individual test result files:")
        report.append("   - agentcore_integration_test_results.json")
        report.append("   - agentcore_query_format_test_results.json")
        report.append("   - agentcore_error_handling_test_results.json")
        
        return "\n".join(report)
    
    def run_all_tests(self) -> bool:
        """
        Run all test suites and generate comprehensive report.
        
        Returns:
            bool: True if all tests passed, False otherwise
        """
        print("🧪 COMPREHENSIVE AGENTCORE TEST SUITE")
        print("=" * 80)
        print("This suite validates the complete AgentCore financial advisor system")
        print("including workflow integration, query handling, and error scenarios.")
        print("")
        print("Test Coverage:")
        print("- Requirements 1.1, 1.2, 1.3: Core financial advisory functionality")
        print("- Requirements 3.2, 3.3, 3.4: Specialist agent coordination")
        print("- Requirements 7.1, 7.2, 7.3, 7.4: Query format handling")
        print("- Requirements 8.1, 8.2, 8.3, 8.5: Error handling and resilience")
        print("=" * 80)
        
        # Run each test suite
        for suite_config in self.test_suites:
            suite_result = self.run_test_suite(suite_config)
            self.results["suite_results"].append(suite_result)
            
            # Brief pause between suites
            time.sleep(2)
        
        # Analyze results
        analysis = self.analyze_test_results()
        self.results["analysis"] = analysis
        self.results["overall_success"] = analysis["passed_suites"] == analysis["total_suites"]
        
        # Generate and display report
        report = self.generate_comprehensive_report(analysis)
        print(f"\n{report}")
        
        # Save comprehensive results
        with open("comprehensive_agentcore_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        with open("comprehensive_agentcore_test_report.txt", "w") as f:
            f.write(report)
        
        print(f"\n📄 Comprehensive results saved to:")
        print(f"   - comprehensive_agentcore_test_results.json")
        print(f"   - comprehensive_agentcore_test_report.txt")
        
        return self.results["overall_success"]


def main():
    """Run the comprehensive AgentCore test suite."""
    tester = ComprehensiveAgentCoreTester()
    
    try:
        success = tester.run_all_tests()
        
        print(f"\n🏁 COMPREHENSIVE TESTING COMPLETE")
        if success:
            print(f"🎉 ALL TESTS PASSED - System ready for deployment!")
        else:
            print(f"❌ SOME TESTS FAILED - Review results before deployment")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing suite error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()