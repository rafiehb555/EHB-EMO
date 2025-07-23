#!/usr/bin/env python3
"""
EHB-5 Simple Automatic Deployment
Simplified automatic deployment system
"""

import subprocess
import time


def check_git_changes():
    """Check if there are new commits to deploy"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        return len(result.stdout.strip()) > 0
    except Exception:
        return False


def deploy_to_vercel():
    """Deploy to Vercel"""
    print("🚀 Deploying to Vercel...")

    try:
        result = subprocess.run(
            ["vercel", "--prod", "--yes"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ Deployment successful!")
            return True
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


def test_deployment():
    """Test the deployment"""
    print("🧪 Testing deployment...")

    try:
        # Test health check
        url = "https://ehb-5-exyq48ygf-rafiehb555s-projects.vercel.app/api/health"
        result = subprocess.run(
            ["curl", "-f", url],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ Health check passed!")
            return True
        else:
            print("❌ Health check failed")
            return False

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def run_auto_deployment():
    """Run automatic deployment"""
    print("🤖 Starting automatic deployment...")

    # Step 1: Check for changes
    if not check_git_changes():
        print("⏭️ No changes detected, skipping deployment")
        return False

    # Step 2: Deploy to Vercel
    if not deploy_to_vercel():
        print("❌ Deployment failed")
        return False

    # Step 3: Test deployment
    if not test_deployment():
        print("❌ Deployment test failed")
        return False

    print("✅ Automatic deployment completed successfully!")
    return True


def start_continuous_deployment():
    """Start continuous deployment monitoring"""
    print("🔄 Starting continuous deployment monitoring...")
    print("📡 Monitoring for changes every 30 seconds...")

    while True:
        try:
            if run_auto_deployment():
                print("✅ Deployment cycle completed")
            else:
                print("⏭️ No deployment needed or failed")

            print("⏳ Waiting 30 seconds before next check...")
            time.sleep(30)

        except KeyboardInterrupt:
            print("🛑 Continuous deployment stopped by user")
            break
        except Exception as e:
            print(f"❌ Continuous deployment error: {e}")
            time.sleep(30)


if __name__ == "__main__":
    # Run single deployment
    success = run_auto_deployment()
    print(f"Deployment Result: {'Success' if success else 'Failed'}")

    # Uncomment to start continuous deployment
    # start_continuous_deployment()
