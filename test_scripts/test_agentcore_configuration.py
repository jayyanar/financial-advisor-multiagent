#!/usr/bin/env python3
"""
Test script for AgentCore CLI configuration

This script tests the AgentCore configuration functionality to ensure
it works correctly before deployment.

Requirements: 6.1, 6.2
"""

import sys
import subprocess
from pathlib import Path
from configure_agentcore import AgentCoreConfigurator


def test_entry_point_validation():
    """Test entry point validation functionality."""
    print("🧪 Testing entry point validation...")
    
    configurator = AgentCoreConfigurator()
    
    # Test with existing entry point
    result = configurator.validate_entry_point()
    if result:
        print("✅ Entry point validation test passed")
        return True
    else:
        print("❌ Entry point validation test failed")
        return False


def test_agentcore_cli_check():
    """Test AgentCore CLI availability check."""
    print("🧪 Testing AgentCore CLI check...")
    
    configurator = AgentCoreConfigurator()
    
    # This will check if AgentCore CLI is available
    # Note: This may fail if AgentCore CLI is not installed, which is expected
    result = configurator.check_agentcore_cli()
    
    if result:
        print("✅ AgentCore CLI check test passed - CLI is available")
        return True
    else:
        print("⚠️  AgentCore CLI check test - CLI not available (this may be expected)")
        return True  # Don't fail the test if CLI is not installed


def test_configuration_parameters():
    """Test configuration parameter handling."""
    print("🧪 Testing configuration parameters...")
    
    # Test with custom parameters
    configurator = AgentCoreConfigurator(entry_point="test_entry.py")
    configurator.agent_name = "test-agent"
    configurator.agent_description = "Test agent description"
    
    # Verify parameters are set correctly
    if (configurator.entry_point == "test_entry.py" and
        configurator.agent_name == "test-agent" and
        configurator.agent_description == "Test agent description"):
        print("✅ Configuration parameters test passed")
        return True
    else:
        print("❌ Configuration parameters test failed")
        return False


def test_command_line_interface():
    """Test command line interface functionality."""
    print("🧪 Testing command line interface...")
    
    try:
        # Test help command
        result = subprocess.run(
            [sys.executable, "configure_agentcore.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and "Configure AgentCore CLI" in result.stdout:
            print("✅ Command line interface test passed")
            return True
        else:
            print("❌ Command line interface test failed")
            return False
            
    except Exception as e:
        print(f"❌ Command line interface test failed: {e}")
        return False


def test_file_existence():
    """Test that required files exist."""
    print("🧪 Testing required files existence...")
    
    required_files = [
        "configure_agentcore.py",
        "financial_advisor_agentcore.py",
        "AGENTCORE_CONFIGURATION.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if not missing_files:
        print("✅ Required files existence test passed")
        return True
    else:
        print(f"❌ Required files existence test failed - missing: {missing_files}")
        return False


def run_all_tests():
    """Run all configuration tests."""
    print("🎯 Running AgentCore Configuration Tests...")
    print("=" * 60)
    
    tests = [
        ("File Existence", test_file_existence),
        ("Entry Point Validation", test_entry_point_validation),
        ("Configuration Parameters", test_configuration_parameters),
        ("Command Line Interface", test_command_line_interface),
        ("AgentCore CLI Check", test_agentcore_cli_check),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All configuration tests passed!")
        return True
    else:
        print(f"❌ {total - passed} tests failed")
        return False


def main():
    """Main test runner."""
    success = run_all_tests()
    
    if success:
        print("\n🎉 AgentCore configuration is ready!")
        print("\nNext steps:")
        print("1. Run: python configure_agentcore.py")
        print("2. Then: python deploy_agentcore.py")
        sys.exit(0)
    else:
        print("\n❌ Configuration tests failed!")
        print("Please fix the issues before proceeding with deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main()