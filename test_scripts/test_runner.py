#!/usr/bin/env python3
"""
AgentCore Test Runner

Simple script to run individual AgentCore tests or the complete test suite.

Usage:
    python test_runner.py --all                    # Run all tests
    python test_runner.py --integration            # Run integration workflow test
    python test_runner.py --query-formats          # Run query format tests
    python test_runner.py --error-handling         # Run error handling tests
    python test_runner.py --help                   # Show help

Author: Financial Advisory System Testing
License: Educational Use Only
"""

import argparse
import subprocess
import sys
from typing import List


def run_test_script(script_name: str, description: str) -> bool:
    """
    Run a specific test script.
    
    Args:
        script_name: Name of the test script to run
        description: Description of the test
        
    Returns:
        bool: True if test passed, False otherwise
    """
    print(f"\n🧪 Running {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_name], check=False)
        
        if result.returncode == 0:
            print(f"✅ {description} PASSED")
            return True
        else:
            print(f"❌ {description} FAILED (exit code: {result.returncode})")
            return False
            
    except FileNotFoundError:
        print(f"❌ Test script not found: {script_name}")
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="AgentCore Test Runner - Run individual tests or complete test suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py --all                    # Run all tests
  python test_runner.py --integration            # Run integration workflow test
  python test_runner.py --query-formats          # Run query format tests
  python test_runner.py --error-handling         # Run error handling tests

Test Descriptions:
  Integration Test:     Complete analysis workflow validation
                       (Requirements: 1.1, 1.2, 1.3, 3.2, 3.3, 3.4)
                       
  Query Format Test:    Various input query format handling
                       (Requirements: 7.1, 7.2, 7.3, 7.4)
                       
  Error Handling Test:  Error scenarios and graceful degradation
                       (Requirements: 8.1, 8.2, 8.3, 8.5)
        """
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all test suites (comprehensive testing)"
    )
    
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run integration workflow test"
    )
    
    parser.add_argument(
        "--query-formats",
        action="store_true",
        help="Run query format tests"
    )
    
    parser.add_argument(
        "--error-handling",
        action="store_true",
        help="Run error handling tests"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tests"
    )
    
    args = parser.parse_args()
    
    # Available tests
    tests = {
        "integration": {
            "script": "test_agentcore_integration_workflow.py",
            "description": "Integration Workflow Test",
            "requirements": "1.1, 1.2, 1.3, 3.2, 3.3, 3.4"
        },
        "query-formats": {
            "script": "test_agentcore_query_formats.py",
            "description": "Query Format Test",
            "requirements": "7.1, 7.2, 7.3, 7.4"
        },
        "error-handling": {
            "script": "test_agentcore_error_handling.py",
            "description": "Error Handling Test",
            "requirements": "8.1, 8.2, 8.3, 8.5"
        }
    }
    
    # List available tests
    if args.list:
        print("📋 Available AgentCore Tests:")
        print("=" * 50)
        for test_key, test_info in tests.items():
            print(f"🧪 {test_info['description']}")
            print(f"   Script: {test_info['script']}")
            print(f"   Requirements: {test_info['requirements']}")
            print(f"   Command: python test_runner.py --{test_key}")
            print()
        return
    
    # Run comprehensive test suite
    if args.all:
        print("🚀 Running Comprehensive AgentCore Test Suite")
        success = run_test_script(
            "run_comprehensive_agentcore_tests.py",
            "Comprehensive Test Suite"
        )
        sys.exit(0 if success else 1)
    
    # Run individual tests
    tests_to_run = []
    
    if args.integration:
        tests_to_run.append("integration")
    
    if args.query_formats:
        tests_to_run.append("query-formats")
    
    if args.error_handling:
        tests_to_run.append("error-handling")
    
    # If no specific tests selected, show help
    if not tests_to_run:
        parser.print_help()
        print("\n💡 Tip: Use --all to run all tests, or specify individual tests")
        print("   Use --list to see available tests")
        return
    
    # Run selected tests
    results = []
    
    for test_key in tests_to_run:
        test_info = tests[test_key]
        success = run_test_script(test_info["script"], test_info["description"])
        results.append((test_info["description"], success))
    
    # Summary
    print(f"\n🏁 Test Summary")
    print("=" * 40)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {description}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All selected tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()