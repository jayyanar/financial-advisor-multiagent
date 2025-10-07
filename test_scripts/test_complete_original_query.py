#!/usr/bin/env python3
"""
Test Original System with Complete Query

This script tests the original financial advisor system with a complete query
that includes all required parameters.
"""

from financial_advisor_multiagent import FinancialAdvisorOrchestrator


def test_complete_query():
    """Test the original system with a complete query."""
    print("🧪 Testing Original System with Complete Query")
    print("=" * 60)
    
    try:
        # Initialize the orchestrator
        print("🚀 Initializing FinancialAdvisorOrchestrator...")
        advisor = FinancialAdvisorOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test with a complete query
        print("\n📤 Testing complete query...")
        test_query = (
            "Analyze Apple Inc. (AAPL) stock for a moderate risk investor "
            "with a long-term investment horizon. Please provide comprehensive "
            "market intelligence, develop trading strategies, create execution "
            "plans, and assess risks."
        )
        
        print(f"Query: {test_query}")
        print("⏳ Processing (this may take a minute)...")
        
        response = advisor.analyze(test_query)
        
        print(f"✅ Response received ({len(response)} characters)")
        
        # Check for key workflow indicators
        response_lower = response.lower()
        workflow_indicators = {
            "market_intelligence": any(term in response_lower for term in ["market", "research", "analysis", "intelligence"]),
            "strategy_development": any(term in response_lower for term in ["strategy", "strategies", "approach"]),
            "execution_planning": any(term in response_lower for term in ["execution", "implementation", "plan"]),
            "risk_assessment": any(term in response_lower for term in ["risk", "assessment", "mitigation"]),
            "educational_disclaimer": any(term in response_lower for term in ["educational", "not financial advice", "disclaimer"])
        }
        
        print(f"\n📊 Workflow Component Analysis:")
        for component, present in workflow_indicators.items():
            print(f"   {component.replace('_', ' ').title()}: {'✅' if present else '❌'}")
        
        # Show sample of response
        print(f"\n📄 Response Sample (first 800 characters):")
        print(f"{response[:800]}...")
        
        # Check if all components are present
        all_present = all(workflow_indicators.values())
        print(f"\n🎯 Complete Workflow: {'✅' if all_present else '❌'}")
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error testing complete query: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_complete_query()
    if success:
        print("\n🎉 Complete query test PASSED - All workflow components present")
    else:
        print("\n⚠️  Complete query test completed but some workflow components may be missing")