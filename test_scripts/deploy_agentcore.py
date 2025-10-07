#!/usr/bin/env python3
"""
AgentCore Deployment Script

This script automates the deployment of the financial advisor agent to Amazon Bedrock AgentCore.
It handles configuration, deployment, and basic validation with comprehensive error handling.

Requirements: 6.2, 6.3
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any


class AgentCoreDeployer:
    """Handles AgentCore deployment with error handling and validation."""
    
    def __init__(self, entry_point: str = "financial_advisor_agentcore.py"):
        self.entry_point = entry_point
        self.deployment_config = {}
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met for deployment."""
        print("🔍 Checking deployment prerequisites...")
        
        # Check if entry point file exists
        if not Path(self.entry_point).exists():
            print(f"❌ Entry point file '{self.entry_point}' not found")
            return False
        
        # Check if AgentCore CLI is installed
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
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ AgentCore CLI check failed: {e}")
            return False
        
        # Check if requirements.txt exists
        if not Path("requirements.txt").exists():
            print("❌ requirements.txt not found")
            return False
        
        # Check AWS credentials
        try:
            result = subprocess.run(
                ["aws", "sts", "get-caller-identity"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode != 0:
                print("❌ AWS credentials not configured or invalid")
                print("Please configure AWS credentials first")
                return False
            
            identity = json.loads(result.stdout)
            print(f"✅ AWS credentials configured for account: {identity.get('Account', 'Unknown')}")
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ AWS credentials check failed: {e}")
            return False
        
        print("✅ All prerequisites met")
        return True
    
    def configure_agentcore(self) -> bool:
        """Configure AgentCore with the financial advisor entry point."""
        print("⚙️  Configuring AgentCore...")
        
        try:
            # Run agentcore configure command
            cmd = [
                "agentcore", "configure",
                "--entrypoint", self.entry_point,
                "--name", "financial_advisor_multiagent"
            ]
            
            print(f"Running: {' '.join(cmd)}")
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
            
            print("✅ AgentCore configuration completed successfully")
            print(f"Configuration output: {result.stdout}")
            
            # Store configuration details
            self.deployment_config["configured"] = True
            self.deployment_config["entry_point"] = self.entry_point
            
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ AgentCore configuration timed out")
            return False
        except Exception as e:
            print(f"❌ AgentCore configuration failed with error: {e}")
            return False
    
    def launch_agentcore(self) -> bool:
        """Launch the agent to AgentCore Runtime."""
        print("🚀 Launching agent to AgentCore...")
        
        try:
            # Run agentcore launch command
            cmd = ["agentcore", "launch"]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout for deployment
            )
            
            if result.returncode != 0:
                print(f"❌ AgentCore launch failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            print("✅ Agent launched successfully to AgentCore")
            print(f"Launch output: {result.stdout}")
            
            # Store deployment details
            self.deployment_config["deployed"] = True
            self.deployment_config["launch_output"] = result.stdout
            
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ AgentCore launch timed out (this may take several minutes)")
            print("You can check deployment status with: agentcore status")
            return False
        except Exception as e:
            print(f"❌ AgentCore launch failed with error: {e}")
            return False
    
    def validate_deployment(self) -> bool:
        """Validate the deployed agent with a test invocation."""
        print("🧪 Validating deployed agent...")
        
        try:
            # Test with a simple financial query
            test_payload = {
                "prompt": "Provide a brief analysis of AAPL stock for a moderate risk investor with a medium-term horizon."
            }
            
            cmd = ["agentcore", "invoke", json.dumps(test_payload)]
            
            print("Running validation test...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout for test
            )
            
            if result.returncode != 0:
                print(f"❌ Deployment validation failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            # Parse and validate response
            try:
                response = json.loads(result.stdout)
                if "result" in response and response["result"]:
                    print("✅ Deployment validation successful")
                    print(f"Test response preview: {response['result'][:200]}...")
                    return True
                else:
                    print("❌ Deployment validation failed: Invalid response format")
                    return False
            except json.JSONDecodeError:
                print("❌ Deployment validation failed: Invalid JSON response")
                return False
            
        except subprocess.TimeoutExpired:
            print("❌ Deployment validation timed out")
            return False
        except Exception as e:
            print(f"❌ Deployment validation failed with error: {e}")
            return False
    
    def get_deployment_status(self) -> Optional[Dict[str, Any]]:
        """Get current deployment status from AgentCore."""
        try:
            result = subprocess.run(
                ["agentcore", "status"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {"status": "success", "output": result.stdout}
            else:
                return {"status": "error", "output": result.stderr}
                
        except Exception as e:
            return {"status": "error", "output": str(e)}
    
    def cleanup_on_failure(self):
        """Cleanup resources if deployment fails."""
        print("🧹 Cleaning up after deployment failure...")
        
        try:
            # Attempt to clean up any partial deployment
            subprocess.run(
                ["agentcore", "cleanup"],
                capture_output=True,
                text=True,
                timeout=60
            )
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup failed: {e}")
    
    def deploy(self) -> bool:
        """Execute the complete deployment process."""
        print("🎯 Starting AgentCore deployment process...")
        print("=" * 60)
        
        try:
            # Step 1: Check prerequisites
            if not self.check_prerequisites():
                print("❌ Prerequisites check failed. Aborting deployment.")
                return False
            
            # Step 2: Configure AgentCore
            if not self.configure_agentcore():
                print("❌ Configuration failed. Aborting deployment.")
                return False
            
            # Step 3: Launch to AgentCore
            if not self.launch_agentcore():
                print("❌ Launch failed. Attempting cleanup...")
                self.cleanup_on_failure()
                return False
            
            # Step 4: Validate deployment
            print("\n⏳ Waiting 30 seconds for deployment to stabilize...")
            time.sleep(30)
            
            if not self.validate_deployment():
                print("❌ Validation failed. Deployment may be incomplete.")
                status = self.get_deployment_status()
                if status:
                    print(f"Deployment status: {status}")
                return False
            
            # Success!
            print("\n" + "=" * 60)
            print("🎉 AgentCore deployment completed successfully!")
            print("=" * 60)
            
            # Show final status
            status = self.get_deployment_status()
            if status and status["status"] == "success":
                print(f"Final status: {status['output']}")
            
            print("\n📋 Next steps:")
            print("1. Test your deployed agent with: agentcore invoke '{\"prompt\": \"your query\"}'")
            print("2. Monitor deployment with: agentcore status")
            print("3. View logs with: agentcore logs")
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Deployment interrupted by user")
            self.cleanup_on_failure()
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error during deployment: {e}")
            self.cleanup_on_failure()
            return False


def main():
    """Main deployment script entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Deploy financial advisor agent to AgentCore",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy_agentcore.py                    # Deploy with default entry point
  python deploy_agentcore.py --entry-point my_agent.py  # Deploy with custom entry point
  python deploy_agentcore.py --validate-only   # Only validate existing deployment
        """
    )
    
    parser.add_argument(
        "--entry-point",
        default="financial_advisor_agentcore.py",
        help="Entry point file for the agent (default: financial_advisor_agentcore.py)"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing deployment, don't deploy"
    )
    
    args = parser.parse_args()
    
    deployer = AgentCoreDeployer(entry_point=args.entry_point)
    
    if args.validate_only:
        print("🧪 Running validation only...")
        success = deployer.validate_deployment()
    else:
        success = deployer.deploy()
    
    if success:
        print("\n✅ Operation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()