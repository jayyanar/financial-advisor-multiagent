#!/usr/bin/env python3
"""
Complete AgentCore Test Suite

This script provides a comprehensive test suite that combines server startup testing
with HTTP request validation. It can run the complete test workflow or individual
test components as needed.

Requirements addressed:
- 5.1: Test system starts on localhost:8080
- 5.2: Test POST /invocations endpoint with sample financial queries
- 5.3: Test GET /ping endpoint for health checks
- 5.4: Validate response formats match AgentCore expectations

Usage:
    python test_agentcore_complete.py                    # Full test suite
    python test_agentcore_complete.py --quick            # Quick tests only
    python test_agentcore_complete.py --server-only      # Server startup only
    python test_agentcore_complete.py --http-only        # HTTP tests only (assumes server running)
"""

import sys
import time
import argparse
from test_local_agentcore_server import AgentCoreServerTester
from test_agentcore_http_requests import AgentCoreHTTPTester


class CompleteAgentCoreTestSuite:
    """Complete test suite combining server startup and HTTP request testing."""
    
    def __init__(self, server_url: str = "http://localhost:8080", timeout: int = 30):
        self.server_url = server_url
        self.timeout = timeout
        self.server_tester = AgentCoreServerTester()
        self.http_tester = AgentCoreHTTPTester(server_url)
        
        # Configure timeouts
        self.server_tester.startup_timeout = timeout
        self.http_tester.timeout = timeout
    
    def run_complete_test_suite(self, quick_mode: bool = False) -> bool:
        """
        Run the complete test suite including server startup and HTTP testing.
        
        Args:
            quick_mode: If True, run quick tests only
            
        Returns:
            bool: True if all tests pass, False otherwise
        """
        print("=" * 80)
        print("🧪 Complete AgentCore Test Suite")
        print("=" * 80)
        print(f"Server URL: {self.server_url}")
        print(f"Timeout: {self.timeout}s")
        print(f"Mode: {'Quick' if quick_mode else 'Comprehensive'}")
        
        overall_success = True
        
        try:
            # Phase 1: Server Startup Test
            print("\n" + "=" * 60)
            print("📡 Phase 1: Server Startup Testing")
            print("=" * 60)
            
            if not self.server_tester.start_server():
                print("❌ Server startup failed - cannot proceed with HTTP tests")
                return False
            
            # Basic connectivity check
            if not self.server_tester.test_basic_connectivity():
                print("❌ Basic connectivity failed")
                overall_success = False
            
            # Health endpoint check
            if not self.server_tester.test_health_endpoint():
                print("❌ Health endpoint test failed")
                overall_success = False
            
            # Phase 2: HTTP Request Testing
            print("\n" + "=" * 60)
            print("🌐 Phase 2: HTTP Request Testing")
            print("=" * 60)
            
            if quick_mode:
                http_success = self.http_tester.run_quick_tests()
            else:
                http_success = self.http_tester.run_comprehensive_tests()
            
            if not http_success:
                print("❌ HTTP request tests failed")
                overall_success = False
            
            # Phase 3: Results Summary
            print("\n" + "=" * 60)
            print("📊 Complete Test Suite Results")
            print("=" * 60)
            
            if overall_success:
                print("🎉 All tests passed! AgentCore system is fully functional.")
                print(f"   ✅ Server startup: SUCCESS")
                print(f"   ✅ Basic connectivity: SUCCESS")
                print(f"   ✅ Health endpoint: SUCCESS")
                print(f"   ✅ HTTP request tests: SUCCESS")
                print(f"\n🚀 System is ready for deployment!")
            else:
                print("⚠️  Some tests failed. Please review the results above.")
                print("   Check server logs and configuration before deployment.")
            
            # Print HTTP test summary
            self.http_tester.print_test_summary()
            
            return overall_success
            
        except KeyboardInterrupt:
            print("\n\n🛑 Test suite interrupted by user")
            overall_success = False
            
        finally:
            # Always stop the server
            print("\n" + "=" * 60)
            print("🛑 Cleanup: Stopping Server")
            print("=" * 60)
            self.server_tester.stop_server()
        
        return overall_success
    
    def run_server_tests_only(self) -> bool:
        """
        Run server startup tests only.
        
        Returns:
            bool: True if server tests pass, False otherwise
        """
        print("=" * 80)
        print("📡 AgentCore Server Startup Tests Only")
        print("=" * 80)
        
        return self.server_tester.run_startup_test()
    
    def run_http_tests_only(self, quick_mode: bool = False) -> bool:
        """
        Run HTTP request tests only (assumes server is already running).
        
        Args:
            quick_mode: If True, run quick tests only
            
        Returns:
            bool: True if HTTP tests pass, False otherwise
        """
        print("=" * 80)
        print("🌐 AgentCore HTTP Request Tests Only")
        print("=" * 80)
        print("⚠️  Assuming server is already running at", self.server_url)
        
        if quick_mode:
            success = self.http_tester.run_quick_tests()
        else:
            success = self.http_tester.run_comprehensive_tests()
        
        self.http_tester.print_test_summary()
        return success


def main():
    """Main entry point for complete test suite."""
    parser = argparse.ArgumentParser(
        description="Complete AgentCore test suite with server startup and HTTP testing"
    )
    parser.add_argument(
        "--server",
        default="http://localhost:8080",
        help="AgentCore server URL (default: http://localhost:8080)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Test timeout in seconds (default: 30)"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick tests only"
    )
    parser.add_argument(
        "--server-only",
        action="store_true",
        help="Run server startup tests only"
    )
    parser.add_argument(
        "--http-only",
        action="store_true",
        help="Run HTTP request tests only (assumes server is running)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.server_only and args.http_only:
        print("❌ Error: Cannot specify both --server-only and --http-only")
        sys.exit(1)
    
    # Create test suite
    test_suite = CompleteAgentCoreTestSuite(args.server, args.timeout)
    
    try:
        if args.server_only:
            success = test_suite.run_server_tests_only()
        elif args.http_only:
            success = test_suite.run_http_tests_only(args.quick)
        else:
            success = test_suite.run_complete_test_suite(args.quick)
        
        # Exit with appropriate code
        if success:
            print("\n✅ All requested tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Check the output above for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error in test suite: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()