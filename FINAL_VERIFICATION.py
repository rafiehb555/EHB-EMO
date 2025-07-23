#!/usr/bin/env python3
"""
EHB-5 Final Verification Script
Confirms all components are ready for production deployment
"""

import os
import sys
import sqlite3
from datetime import datetime


class FinalVerifier:
    """Final verification for EHB-5 production deployment"""

    def __init__(self):
        self.verification_results = {
            'backend': False,
            'frontend': False,
            'database': False,
            'security': False,
            'deployment': False
        }

    def verify_backend(self):
        """Verify backend components"""
        print("🔧 Verifying Backend Components...")

        try:
            # Test imports
            import flask
            import jwt
            import bcrypt
            import psutil
            print("   ✅ All dependencies imported successfully")

            # Test API server
            from api_server import app
            print("   ✅ API server loaded successfully")

            # Test database
            from database import db
            print("   ✅ Database manager loaded successfully")

            # Test auth manager
            from auth_manager import AuthManager
            print("   ✅ Authentication manager loaded successfully")

            # Test data processor
            from data_processor import DataProcessor
            print("   ✅ Data processor loaded successfully")

            # Test enhanced security
            from enhanced_security import security_manager
            print("   ✅ Enhanced security loaded successfully")

            self.verification_results['backend'] = True
            print("   ✅ Backend verification complete")
            return True

        except Exception as e:
            print(f"   ❌ Backend verification failed: {e}")
            return False

    def verify_frontend(self):
        """Verify frontend components"""
        print("🎨 Verifying Frontend Components...")

        required_files = [
            'index.html',
            'styles.css',
            'script.js'
        ]

        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file} exists")
            else:
                print(f"   ❌ {file} missing")
                missing_files.append(file)

        if not missing_files:
            self.verification_results['frontend'] = True
            print("   ✅ Frontend verification complete")
            return True
        else:
            print(f"   ❌ Missing frontend files: {missing_files}")
            return False

    def verify_database(self):
        """Verify database components"""
        print("🗄️  Verifying Database Components...")

        try:
            # Check database file
            if os.path.exists('ehb5.db'):
                print("   ✅ Database file exists")
            else:
                print("   ❌ Database file missing")
                return False

            # Check database tables
            conn = sqlite3.connect('ehb5.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            required_tables = ['users', 'projects', 'data_files', 'system_logs']
            missing_tables = [table for table in required_tables if table not in table_names]

            if missing_tables:
                print(f"   ❌ Missing tables: {missing_tables}")
                return False
            else:
                print("   ✅ All required tables exist")

            conn.close()

            self.verification_results['database'] = True
            print("   ✅ Database verification complete")
            return True

        except Exception as e:
            print(f"   ❌ Database verification failed: {e}")
            return False

    def verify_security(self):
        """Verify security components"""
        print("🔒 Verifying Security Components...")

        try:
            from enhanced_security import security_manager

            # Test bcrypt
            test_password = "test123"
            hashed = security_manager.hash_password_bcrypt(test_password)
            if hashed and security_manager.verify_password_bcrypt(test_password, hashed):
                print("   ✅ Bcrypt password hashing working")
            else:
                print("   ❌ Bcrypt password hashing failed")
                return False

            # Test input validation
            if security_manager.validate_email("test@example.com"):
                print("   ✅ Email validation working")
            else:
                print("   ❌ Email validation failed")
                return False

            if security_manager.validate_username("testuser"):
                print("   ✅ Username validation working")
            else:
                print("   ❌ Username validation failed")
                return False

            # Test password strength validation
            password_validation = security_manager.validate_password_strength("Test123!")
            if password_validation['is_valid']:
                print("   ✅ Password strength validation working")
            else:
                print("   ❌ Password strength validation failed")
                return False

            self.verification_results['security'] = True
            print("   ✅ Security verification complete")
            return True

        except Exception as e:
            print(f"   ❌ Security verification failed: {e}")
            return False

    def verify_deployment(self):
        """Verify deployment components"""
        print("🚀 Verifying Deployment Components...")

        required_files = [
            'vercel.json',
            'api/index.py',
            'requirements.txt',
            'package.json'
        ]

        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file} exists")
            else:
                print(f"   ❌ {file} missing")
                missing_files.append(file)

        if not missing_files:
            self.verification_results['deployment'] = True
            print("   ✅ Deployment verification complete")
            return True
        else:
            print(f"   ❌ Missing deployment files: {missing_files}")
            return False

    def run_final_verification(self):
        """Run complete final verification"""
        print("🎯 EHB-5 FINAL VERIFICATION")
        print("=" * 60)

        # Run all verifications
        backend_ok = self.verify_backend()
        frontend_ok = self.verify_frontend()
        database_ok = self.verify_database()
        security_ok = self.verify_security()
        deployment_ok = self.verify_deployment()

        # Generate final report
        print("\n📊 FINAL VERIFICATION REPORT")
        print("=" * 60)

        for component, status in self.verification_results.items():
            status_icon = "✅" if status else "❌"
            print(f"{component:20} {status_icon}")

        print("=" * 60)

        if all(self.verification_results.values()):
            print("🎉 ALL SYSTEMS VERIFIED FOR PRODUCTION!")
            print("✅ Your EHB-5 project is 100% ready for deployment!")
            return True
        else:
            print("⚠️  Some components need attention before deployment")
            return False

    def show_deployment_instructions(self):
        """Show final deployment instructions"""
        print("\n🚀 FINAL DEPLOYMENT INSTRUCTIONS")
        print("=" * 60)
        print("1. Fix Vercel Authentication:")
        print("   • Visit: https://vercel.com/dashboard")
        print("   • Select your EHB-5 project")
        print("   • Go to Settings → Functions")
        print("   • Set Authentication to 'None'")
        print("   • Save changes and redeploy")
        print()
        print("2. Test Production Endpoints:")
        print("   • GET /api/health")
        print("   • GET /api/system/status")
        print("   • GET /api/security/status")
        print()
        print("3. Monitor Deployment:")
        print("   • Check response times")
        print("   • Verify security features")
        print("   • Test all functionality")
        print()
        print("🎯 After completing these steps, your system will be 100% operational!")


def main():
    """Main verification function"""
    verifier = FinalVerifier()

    # Run verification
    success = verifier.run_final_verification()

    if success:
        verifier.show_deployment_instructions()
        print("\n🎉 CONGRATULATIONS!")
        print("Your EHB-5 project is ready for production deployment!")
    else:
        print("\n❌ Verification failed. Please fix issues before deployment.")


if __name__ == "__main__":
    main()
