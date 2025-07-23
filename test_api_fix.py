#!/usr/bin/env python3
"""
Test script to check and fix API issues
"""

import requests
import json

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "https://ehb-5-rafiehb555s-projects.vercel.app"

    endpoints = [
        "/",
        "/health",
        "/api/status",
        "/api/system/status"
    ]

    print("🧪 Testing API Endpoints...")
    print("=" * 50)

    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n🔍 Testing: {endpoint}")
            print(f"URL: {url}")

            response = requests.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ JSON Response:")
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Error: {e}")
                    print(f"Raw Response: {response.text[:200]}...")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"❌ Request Error: {e}")

    print("\n" + "=" * 50)
    print("🎯 API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints()
