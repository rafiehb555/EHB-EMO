#!/usr/bin/env python3
"""
Simple deployment test
"""

import json
import urllib.request


def test_api():
    url = "https://ehb-5-b108xdrxn-rafiehb555s-projects.vercel.app/"

    try:
        print(f"🔍 Testing: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode('utf-8')
        result = json.loads(data)

        print("✅ **SUCCESS!**")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🕒 Timestamp: {result.get('timestamp', 'unknown')}")
        print(f"📦 Version: {result.get('version', 'unknown')}")
        print(f"💬 Message: {result.get('message', 'unknown')}")

        return True

    except Exception as e:
        print(f"❌ **ERROR**: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 **EHB-5 DEPLOYMENT TEST**")
    print("=" * 40)

    success = test_api()

    if success:
        print("\n🎉 **DEPLOYMENT IS WORKING!**")
        print("✅ **500 ERROR FIXED!**")
    else:
        print("\n❌ **DEPLOYMENT STILL HAS ISSUES**")
