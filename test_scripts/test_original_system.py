#!/usr/bin/env python3
"""
Test Original Financial Advisor System

This script tests the original financial advisor system to ensure it works
before testing the AgentCore wrapper.
"""

from financial_advisor_multiagent import FinancialAdvisorOrchestrator


def test_original_system():
    """Test the original financial advisor system."""
    print("🧪 Testing Original Financial Advisor System")
    print("=" * 50)
    
    try:
        # Initialize the orchestrator
        print("🚀 Initializing FinancialAdvisorOrchestrator...")
        advisor = FinancialAdvisorOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test with a simple query
        print("\n📤 Testing simple query...")
        test_query = "Analyze AAPL stock for moderate risk investor"
        
        print(f"Query: {test_query}")
        response = advisor.analyze(test_query)
        
        print(f"✅ Response received ({len(response)} characters)")
        print(f"Response sample: {response[:300]}...")
        
        # Check for key indicators
        response_lower = response.lower()
        indicators = {
            "market": "market" in response_lower,
            "strategy": "strategy" in response_lower,
            "execution": "execution" in response_lower,
            "risk": "risk" in response_lower,
            "educational": "educational" in response_lower
        }
        
        print(f"\n📊 Content Analysis:")
        for indicator, present in indicators.items():
            print(f"   {indicator.capitalize()}: {'✅' if present else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing original system: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_original_system()
    if success:
        print("\n🎉 Original system test PASSED")
    else:
        print("\n❌ Original system test FAILED")