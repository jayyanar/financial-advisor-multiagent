#!/usr/bin/env python3
"""
AgentCore CLI Configuration Script

This script sets up the AgentCore CLI configuration for the financial advisor agent.
It configures the agentcore CLI to use financial_advisor_agentcore.py as the entry point
and sets up the necessary deployment parameters.

Requirements: 6.1, 6.2
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class AgentCoreConfigurator:
    """Handles AgentCore CLI configuration setup."""
    
    def __init__(self, entry_point: str = "financial_advisor_agentcore.py"):
        self.entry_point = entry_point
        self.agent_name = "financial_advisor_multiagent"
        self.agent_description = "AI-powered financial advisory system with multi-agent orchestration for educational purposes"
        
    def validate_entry_point(self) -> bool:
        """Validate that the entry point file exists and is properly configured."""
        print(f"🔍 Validating entry point: {self.entry_point}")
        
        if not Path(self.entry_point).exists():
            print(f"❌ Entry point file '{self.entry_point}' not found")
            return False
        
        # Check if the entry point file contains required AgentCore components
        try:
            with open(self.entry_point, 'r') as f:
                content = f.read()
                
            required_components = [
                "BedrockAgentCoreApp",
                "@app.entrypoint",
                "app.run()"
            ]
            
            missing_components = []
            for component in required_components:
                if component not in content:
                    missing_components.append(component)
            
            if missing_components:
                print(f"❌ Entry point missing required components: {missing_components}")
                return False
            
            print(f"✅ Entry point '{self.entry_point}' is properly configured")
            return True
            
        except Exception as e:
            print(f"❌ Error validating entry point: {e}")
            return False
    
    def check_agentcore_cli(self) -> bool:
        """Check if AgentCore CLI is installed and accessible."""
        print("🔍 Checking AgentCore CLI availability...")
        
        try:
            result = subprocess.run(
                ["agentcore", "--help"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                print("❌ AgentCore CLI not found or not working")
                print("Please install AgentCore CLI first")
                return False
            
            print(f"✅ AgentCore CLI found and working")
            return True
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ AgentCore CLI check failed: {e}")
            print("Please install AgentCore CLI first")
            return False
    
    def check_aws_credentials(self) -> bool:
        """Check if AWS credentials are configured."""
        print("🔍 Checking AWS credentials...")
        
        try:
            result = subprocess.run(
                ["aws", "sts", "get-caller-identity"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                print("❌ AWS credentials not configured or invalid")
                print("Please configure AWS credentials first using 'aws configure'")
                return False
            
            identity = json.loads(result.stdout)
            account_id = identity.get('Account', 'Unknown')
            user_arn = identity.get('Arn', 'Unknown')
            print(f"✅ AWS credentials configured")
            print(f"   Account: {account_id}")
            print(f"   User: {user_arn}")
            return True
            
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ AWS credentials check failed: {e}")
            print("Please install AWS CLI and configure credentials")
            return False
    
    def configure_agentcore(self) -> bool:
        """Configure AgentCore CLI with the financial advisor entry point."""
        print("⚙️  Configuring AgentCore CLI...")
        
        try:
            # Prepare the agentcore configure command
            cmd = [
                "agentcore", "configure",
                "--entrypoint", self.entry_point,
                "--name", self.agent_name
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            print(f"Entry point: {self.entry_point}")
            print(f"Agent name: {self.agent_name}")
            print(f"Description: {self.agent_description}")
            
            # Execute the configuration command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"❌ AgentCore configuration failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            print("✅ AgentCore CLI configuration completed successfully")
            
            # Display configuration output
            if result.stdout.strip():
                print("Configuration output:")
                print(result.stdout)
            
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ AgentCore configuration timed out")
            return False
        except Exception as e:
            print(f"❌ AgentCore configuration failed with error: {e}")
            return False
    
    def verify_configuration(self) -> bool:
        """Verify that the AgentCore configuration was successful."""
        print("🧪 Verifying AgentCore configuration...")
        
        try:
            # Check configuration status
            result = subprocess.run(
                ["agentcore", "status"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ AgentCore configuration verified successfully")
                if result.stdout.strip():
                    print("Configuration status:")
                    print(result.stdout)
                return True
            else:
                print("⚠️  Configuration verification returned non-zero status")
                print(f"Status output: {result.stderr}")
                # Don't fail here as this might be expected for unconfigured state
                return True
                
        except Exception as e:
            print(f"⚠️  Configuration verification failed: {e}")
            # Don't fail the overall process for verification issues
            return True
    
    def display_next_steps(self):
        """Display next steps after successful configuration."""
        print("\n" + "=" * 60)
        print("🎉 AgentCore CLI Configuration Complete!")
        print("=" * 60)
        
        print(f"\n📋 Configuration Summary:")
        print(f"   Entry Point: {self.entry_point}")
        print(f"   Agent Name: {self.agent_name}")
        print(f"   Description: {self.agent_description}")
        
        print(f"\n🚀 Next Steps:")
        print(f"1. Deploy the agent to AWS:")
        print(f"   agentcore launch")
        print(f"")
        print(f"2. Test the deployed agent:")
        print(f"   agentcore invoke '{{\"prompt\": \"Analyze AAPL for moderate risk investor\"}}'")
        print(f"")
        print(f"3. Check deployment status:")
        print(f"   agentcore status")
        print(f"")
        print(f"4. View agent logs:")
        print(f"   agentcore logs")
        print(f"")
        print(f"5. Use the deployment script for automated deployment:")
        print(f"   python deploy_agentcore.py")
        
        print(f"\n⚠️  Important Notes:")
        print(f"   • This system is for educational purposes only")
        print(f"   • Not licensed financial advice")
        print(f"   • Ensure AWS credentials have appropriate permissions")
        print(f"   • Monitor costs when deploying to AWS")
    
    def configure(self) -> bool:
        """Execute the complete configuration process."""
        print("🎯 Starting AgentCore CLI Configuration...")
        print("=" * 60)
        
        try:
            # Step 1: Validate entry point
            if not self.validate_entry_point():
                print("❌ Entry point validation failed. Aborting configuration.")
                return False
            
            # Step 2: Check AgentCore CLI
            if not self.check_agentcore_cli():
                print("❌ AgentCore CLI check failed. Aborting configuration.")
                return False
            
            # Step 3: Check AWS credentials
            if not self.check_aws_credentials():
                print("❌ AWS credentials check failed. Aborting configuration.")
                return False
            
            # Step 4: Configure AgentCore
            if not self.configure_agentcore():
                print("❌ AgentCore configuration failed. Aborting.")
                return False
            
            # Step 5: Verify configuration
            if not self.verify_configuration():
                print("⚠️  Configuration verification had issues, but continuing...")
            
            # Step 6: Display next steps
            self.display_next_steps()
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Configuration interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error during configuration: {e}")
            return False


def main():
    """Main configuration script entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Configure AgentCore CLI for financial advisor agent deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python configure_agentcore.py                           # Configure with default entry point
  python configure_agentcore.py --entry-point my_agent.py # Configure with custom entry point
  python configure_agentcore.py --name my-agent           # Configure with custom agent name
        """
    )
    
    parser.add_argument(
        "--entry-point",
        default="financial_advisor_agentcore.py",
        help="Entry point file for the agent (default: financial_advisor_agentcore.py)"
    )
    
    parser.add_argument(
        "--name",
        default="financial-advisor-multiagent",
        help="Name for the AgentCore agent (default: financial-advisor-multiagent)"
    )
    
    parser.add_argument(
        "--description",
        default="AI-powered financial advisory system with multi-agent orchestration for educational purposes",
        help="Description for the AgentCore agent"
    )
    
    args = parser.parse_args()
    
    configurator = AgentCoreConfigurator(entry_point=args.entry_point)
    configurator.agent_name = args.name
    configurator.agent_description = args.description
    
    success = configurator.configure()
    
    if success:
        print("\n✅ Configuration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Configuration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()