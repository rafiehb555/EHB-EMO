import json
import urllib.request

#!/usr/bin/env python3
"""
Simple EHB-5 Deployment Test
Testing different approaches to access the API
"""



def test_with_headers():
    """Test with custom headers"""
    url = "https://ehb-5-ewn1itzcc-rafiehb555s-projects.vercel.app/"

    # Create request with headers
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    req.add_header('Accept', 'application/json')
    req.add_header('Cache-Control', 'no-cache')

    try:
        print(f"🔍 Testing with headers: {url}")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode('utf-8')
        result = json.loads(data)

        print("✅ **SUCCESS WITH HEADERS!**")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"💬 Message: {result.get('message', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ **ERROR WITH HEADERS**: {str(e)}")
        return False


def test_health_endpoint():
    """Test health endpoint specifically"""
    url = "https://ehb-5-ewn1itzcc-rafiehb555s-projects.vercel.app/api/health"

    try:
        print(f"🔍 Testing health endpoint: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode('utf-8')
        result = json.loads(data)

        print("✅ **HEALTH ENDPOINT SUCCESS!**")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🌍 Environment: {result.get('environment', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ **HEALTH ENDPOINT ERROR**: {str(e)}")
        return False


def test_public_endpoint():
    """Test public endpoint"""
    url = "https://ehb-5-ewn1itzcc-rafiehb555s-projects.vercel.app/api/public"

    try:
        print(f"🔍 Testing public endpoint: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode('utf-8')
        result = json.loads(data)

        print("✅ **PUBLIC ENDPOINT SUCCESS!**")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🔓 Access: {result.get('access', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ **PUBLIC ENDPOINT ERROR**: {str(e)}")
        return False


def test_system_status():
    """Test system status endpoint"""
    url = "https://ehb-5-ewn1itzcc-rafiehb555s-projects.vercel.app/api/system/status"

    try:
        print(f"🔍 Testing system status: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode('utf-8')
        result = json.loads(data)

        print("✅ **SYSTEM STATUS SUCCESS!**")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"⏱️ Uptime: {result.get('uptime', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ **SYSTEM STATUS ERROR**: {str(e)}")
        return False


def main():
    print("🚀 **EHB-5 COMPREHENSIVE TEST**")
    print("=" * 50)

    # Test all endpoints
    tests = [
        ("Root with Headers", test_with_headers),
        ("Health Endpoint", test_health_endpoint),
        ("Public Endpoint", test_public_endpoint),
        ("System Status", test_system_status)
    ]

    success_count = 0
    total_tests = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 **{test_name}**")
        print("-" * 30)
        if test_func():
            success_count += 1

    print(f"\n📊 **FINAL RESULTS**")
    print("=" * 30)
    print(f"✅ Successful: {success_count}/{total_tests}")
    print(f"❌ Failed: {total_tests - success_count}/{total_tests}")

    if success_count > 0:
        print("\n🎉 **DEPLOYMENT IS WORKING!**")
        print("At least one endpoint is accessible!")
    else:
        print("\n⚠️ **ALL TESTS FAILED**")
        print("There might be a Vercel authentication issue.")


if __name__ == "__main__":
    main()
