#!/usr/bin/env python3
"""
EHB-5 API Endpoints Test Script
Test all API endpoints and AI agents functionality
"""

import requests
import time


class APIEndpointTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.dashboard_url = "http://localhost:8000"

    def test_health_endpoint(self):
        """Test health endpoint"""
        print("🏥 Testing Health Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_system_status(self):
        """Test system status endpoint"""
        print("\n📊 Testing System Status...")
        try:
            response = requests.get(f"{self.base_url}/api/system/status")
            print(f"   Status: {response.status_code}")
            data = response.json()
            print(f"   System Status: {data.get('status', 'unknown')}")
            print(f"   Agents Active: {data.get('agents_active', 0)}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_agents_endpoint(self):
        """Test agents endpoint"""
        print("\n🤖 Testing Agents Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/agents")
            print(f"   Status: {response.status_code}")
            data = response.json()
            print(f"   Total Agents: {len(data.get('agents', []))}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_data_processing(self):
        """Test data processing endpoint"""
        print("\n📊 Testing Data Processing...")
        try:
            test_data = {"data": "Test data for processing"}
            response = requests.post(
                f"{self.base_url}/api/process-data",
                json=test_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Processed: {data.get('status', 'unknown')}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_config_validation(self):
        """Test config validation endpoint"""
        print("\n⚙️ Testing Config Validation...")
        try:
            test_config = {
                "project": "EHB-5",
                "version": "2.0.0",
                "settings": {
                    "database": "enabled",
                    "api": "active"
                }
            }
            response = requests.post(
                f"{self.base_url}/api/validate-config",
                json=test_config
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Valid: {data.get('is_valid', False)}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_security_scan(self):
        """Test security scan endpoint"""
        print("\n🛡️ Testing Security Scan...")
        try:
            response = requests.get(f"{self.base_url}/api/security/scan")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                threats = data.get('threats_detected', 0)
                print(f"   Threats: {threats}")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def test_performance_metrics(self):
        """Test performance metrics endpoint"""
        print("\n⚡ Testing Performance Metrics...")
        try:
            response = requests.get(f"{self.base_url}/api/performance")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   CPU: {data.get('cpu_percent', 0)}%")
                print(f"   Memory: {data.get('memory_percent', 0)}%")
            return response.status_code == 200
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 EHB-5 API Endpoints Test")
        print("="*50)

        tests = [
            self.test_health_endpoint,
            self.test_system_status,
            self.test_agents_endpoint,
            self.test_data_processing,
            self.test_config_validation,
            self.test_security_scan,
            self.test_performance_metrics
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Small delay between tests

        print(f"\n📊 Test Results: {passed}/{total} passed")

        if passed == total:
            print("✅ All API endpoints working correctly!")
        else:
            print("⚠️ Some endpoints may need attention")

    def interactive_menu(self):
        """Interactive test menu"""
        while True:
            print("\n" + "="*50)
            print("🎮 API ENDPOINTS TEST MENU")
            print("="*50)
            print("1. Test All Endpoints")
            print("2. Test Health Endpoint")
            print("3. Test System Status")
            print("4. Test Agents Endpoint")
            print("5. Test Data Processing")
            print("6. Test Config Validation")
            print("7. Test Security Scan")
            print("8. Test Performance Metrics")
            print("9. Exit")

            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == '1':
                self.run_all_tests()
            elif choice == '2':
                self.test_health_endpoint()
            elif choice == '3':
                self.test_system_status()
            elif choice == '4':
                self.test_agents_endpoint()
            elif choice == '5':
                self.test_data_processing()
            elif choice == '6':
                self.test_config_validation()
            elif choice == '7':
                self.test_security_scan()
            elif choice == '8':
                self.test_performance_metrics()
            elif choice == '9':
                print("👋 Exiting API Test System...")
                break
            else:
                print("❌ Invalid choice. Please try again.")


def main():
    """Main function"""
    tester = APIEndpointTester()
    tester.interactive_menu()


if __name__ == "__main__":
    main()
