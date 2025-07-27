#!/usr/bin/env python3
"""
EHB-5 Automatic Deployment Fix
Tests and verifies deployment status
"""

import json
import time
from datetime import datetime

import requests


def test_deployment(url):
    """Test deployment endpoints"""
    results = {}

    # Test health endpoint
    try:
        response = requests.get(f"{url}/api/health", timeout=10)
        results['health'] = {
            'status': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'success': response.status_code == 200
        }
    except Exception as e:
        results['health'] = {
            'status': 'error',
            'error': str(e),
            'success': False
        }

    # Test system status
    try:
        response = requests.get(f"{url}/api/system/status", timeout=10)
        results['system'] = {
            'status': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'success': response.status_code == 200
        }
    except Exception as e:
        results['system'] = {
            'status': 'error',
            'error': str(e),
            'success': False
        }

    # Test projects endpoint
    try:
        response = requests.get(f"{url}/api/projects", timeout=10)
        results['projects'] = {
            'status': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'success': response.status_code == 200
        }
    except Exception as e:
        results['projects'] = {
            'status': 'error',
            'error': str(e),
            'success': False
        }

    return results


def print_results(results, url):
    """Print test results"""
    print(f"\n🔍 **DEPLOYMENT TEST RESULTS**")
    print(f"🌐 **URL**: {url}")
    print(f"⏰ **Test Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    all_success = True

    for endpoint, result in results.items():
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} **{endpoint.upper()}**: {result['status']}")

        if result['success'] and result['data']:
            print(f"   📊 Data: {json.dumps(result['data'], indent=2)}")
        elif not result['success']:
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
            all_success = False

    print()
    if all_success:
        print("🎉 **ALL TESTS PASSED! DEPLOYMENT IS WORKING!**")
        return True
    else:
        print("⚠️ **SOME TESTS FAILED! DEPLOYMENT NEEDS FIXING!**")
        return False


def main():
    """Main function"""
    print("🚀 **EHB-5 AUTOMATIC DEPLOYMENT FIX**")
    print("=" * 50)

    # Test the latest deployment
    url = "https://ehb-5-gxn0yksvg-rafiehb555s-projects.vercel.app"

    print(f"🔍 Testing deployment: {url}")
    print("⏳ Please wait...")

    # Test deployment
    results = test_deployment(url)
    success = print_results(results, url)

    if success:
        print("\n✅ **DEPLOYMENT FIXED SUCCESSFULLY!**")
        print("🎯 **Your EHB-5 system is now working on Vercel!**")
        print(f"🌐 **Live URL**: {url}")
        print("🚀 **Status**: OPERATIONAL")
    else:
        print("\n❌ **DEPLOYMENT STILL HAS ISSUES**")
        print("🔧 **Need to investigate further**")

    return success


if __name__ == "__main__":
    main()
