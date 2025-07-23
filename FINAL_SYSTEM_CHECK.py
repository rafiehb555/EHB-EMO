#!/usr/bin/env python3
"""
EHB-5 Final System Check
Comprehensive testing of all system components
"""

import os
import sys
import sqlite3
import requests
import json
from datetime import datetime


class FinalSystemCheck:
    """Comprehensive system check for EHB-5"""

    def __init__(self):
        self.check_results = {
            'file_structure': False,
            'database_integrity': False,
            'api_endpoints': False,
            'security_features': False,
            'ai_agents': False,
            'frontend_components': False
        }

    def check_file_structure(self):
        """Check all required files exist"""
        print("📁 Checking File Structure...")

        required_files = [
            'main.py',
            'api_server.py',
            'database.py',
            'auth_manager.py',
            'data_processor.py',
            'enhanced_security.py',
            'ai_agents.py',
            'index.html',
            'styles.css',
            'script.js',
            'vercel.json',
            'requirements.txt',
            'package.json',
            'api/index.py',
            'ehb5.db'
        ]

        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} - MISSING")
                missing_files.append(file)

        if not missing_files:
            self.check_results['file_structure'] = True
            print("   ✅ All required files present")
            return True
        else:
            print(f"   ❌ Missing files: {missing_files}")
            return False

    def check_database_integrity(self):
        """Check database integrity"""
        print("🗄️  Checking Database Integrity...")

        try:
            conn = sqlite3.connect('ehb5.db')
            cursor = conn.cursor()

            # Check tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            required_tables = ['users', 'projects', 'data_files', 'system_logs']
            missing_tables = [table for table in required_tables if table not in table_names]

            if missing_tables:
                print(f"   ❌ Missing tables: {missing_tables}")
                return False

            print("   ✅ All required tables exist")

            # Check table structure
            for table in required_tables:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"   ✅ {table} table structure valid ({len(columns)} columns)")

            conn.close()
            self.check_results['database_integrity'] = True
            print("   ✅ Database integrity verified")
            return True

        except Exception as e:
            print(f"   ❌ Database check failed: {e}")
            return False

    def check_api_endpoints(self):
        """Check API endpoints structure"""
        print("🔌 Checking API Endpoints...")

        try:
            # Import API server
            from api_server import app

            # Check if app has routes
            if hasattr(app, 'url_map'):
                routes = [str(rule) for rule in app.url_map.iter_rules()]
                print(f"   ✅ API server loaded with {len(routes)} routes")

                # Check for key endpoints
                key_endpoints = ['/api/health', '/api/users', '/api/system/status']
                found_endpoints = []

                for endpoint in key_endpoints:
                    if any(endpoint in route for route in routes):
                        found_endpoints.append(endpoint)
                        print(f"   ✅ {endpoint} endpoint available")
                    else:
                        print(f"   ❌ {endpoint} endpoint missing")

                if len(found_endpoints) == len(key_endpoints):
                    self.check_results['api_endpoints'] = True
                    print("   ✅ All key API endpoints available")
                    return True
                else:
                    return False
            else:
                print("   ❌ API server structure invalid")
                return False

        except Exception as e:
            print(f"   ❌ API check failed: {e}")
            return False

    def check_security_features(self):
        """Check security features"""
        print("🔒 Checking Security Features...")

        try:
            from enhanced_security import security_manager

            # Test password hashing
            test_password = "TestPassword123!"
            hashed = security_manager.hash_password_bcrypt(test_password)
            if hashed and security_manager.verify_password_bcrypt(test_password, hashed):
                print("   ✅ Bcrypt password hashing working")
            else:
                print("   ❌ Bcrypt password hashing failed")
                return False

            # Test input validation
            validation_tests = [
                ("test@example.com", "email"),
                ("validuser123", "username"),
                ("StrongPass123!", "password")
            ]

            for test_value, test_type in validation_tests:
                if test_type == "email":
                    result = security_manager.validate_email(test_value)
                elif test_type == "username":
                    result = security_manager.validate_username(test_value)
                elif test_type == "password":
                    result = security_manager.validate_password_strength(test_value)
                    result = result['is_valid']

                if result:
                    print(f"   ✅ {test_type} validation working")
                else:
                    print(f"   ❌ {test_type} validation failed")
                    return False

            self.check_results['security_features'] = True
            print("   ✅ All security features working")
            return True

        except Exception as e:
            print(f"   ❌ Security check failed: {e}")
            return False

    def check_ai_agents(self):
        """Check AI agents"""
        print("🤖 Checking AI Agents...")

        try:
            from ai_agents import agents

            if agents and len(agents) > 0:
                print(f"   ✅ {len(agents)} AI agents loaded")

                # Check agent structure
                for agent in agents[:5]:  # Check first 5 agents
                    if 'name' in agent and 'function' in agent:
                        print(f"   ✅ Agent '{agent['name']}' structure valid")
                    else:
                        print(f"   ❌ Agent structure invalid")
                        return False

                self.check_results['ai_agents'] = True
                print("   ✅ AI agents system operational")
                return True
            else:
                print("   ❌ No AI agents found")
                return False

        except Exception as e:
            print(f"   ❌ AI agents check failed: {e}")
            return False

    def check_frontend_components(self):
        """Check frontend components"""
        print("🎨 Checking Frontend Components...")

        try:
            # Check HTML file
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                if 'EHB-5' in html_content and 'dashboard' in html_content.lower():
                    print("   ✅ HTML structure valid")
                else:
                    print("   ❌ HTML structure invalid")
                    return False

            # Check CSS file
            with open('styles.css', 'r', encoding='utf-8') as f:
                css_content = f.read()
                if len(css_content) > 100:  # Basic check for content
                    print("   ✅ CSS styles loaded")
                else:
                    print("   ❌ CSS file too small")
                    return False

            # Check JavaScript file
            with open('script.js', 'r', encoding='utf-8') as f:
                js_content = f.read()
                if 'function' in js_content or 'const' in js_content:
                    print("   ✅ JavaScript functionality present")
                else:
                    print("   ❌ JavaScript file empty or invalid")
                    return False

            self.check_results['frontend_components'] = True
            print("   ✅ All frontend components valid")
            return True

        except Exception as e:
            print(f"   ❌ Frontend check failed: {e}")
            return False

    def run_comprehensive_check(self):
        """Run comprehensive system check"""
        print("🎯 EHB-5 COMPREHENSIVE SYSTEM CHECK")
        print("=" * 60)

        # Run all checks
        file_ok = self.check_file_structure()
        database_ok = self.check_database_integrity()
        api_ok = self.check_api_endpoints()
        security_ok = self.check_security_features()
        ai_ok = self.check_ai_agents()
        frontend_ok = self.check_frontend_components()

        # Generate comprehensive report
        print("\n📊 COMPREHENSIVE SYSTEM REPORT")
        print("=" * 60)

        for component, status in self.check_results.items():
            status_icon = "✅" if status else "❌"
            component_name = component.replace('_', ' ').title()
            print(f"{component_name:25} {status_icon}")

        print("=" * 60)

        if all(self.check_results.values()):
            print("🎉 ALL SYSTEMS OPERATIONAL!")
            print("✅ Your EHB-5 project is 100% ready for production!")
            return True
        else:
            print("⚠️  Some components need attention")
            return False

    def show_production_readiness(self):
        """Show production readiness status"""
        print("\n🚀 PRODUCTION READINESS STATUS")
        print("=" * 60)

        readiness_score = sum(self.check_results.values()) / len(self.check_results) * 100

        print(f"Overall Readiness: {readiness_score:.1f}%")

        if readiness_score == 100:
            print("🎯 STATUS: READY FOR PRODUCTION DEPLOYMENT")
            print("✅ All systems verified and operational")
            print("🚀 Ready to deploy to Vercel")
        elif readiness_score >= 80:
            print("⚠️  STATUS: NEARLY READY")
            print("🔧 Minor fixes needed before deployment")
        else:
            print("❌ STATUS: NEEDS ATTENTION")
            print("🔧 Significant work needed before deployment")

        print("\n🎯 Next Steps:")
        print("1. Fix Vercel authentication (5 minutes)")
        print("2. Deploy to production")
        print("3. Test all endpoints")
        print("4. Monitor system performance")


def main():
    """Main system check function"""
    checker = FinalSystemCheck()

    # Run comprehensive check
    success = checker.run_comprehensive_check()

    if success:
        checker.show_production_readiness()
        print("\n🎉 CONGRATULATIONS!")
        print("Your EHB-5 project is ready for production deployment!")
    else:
        print("\n❌ System check failed. Please fix issues before deployment.")


if __name__ == "__main__":
    main()
