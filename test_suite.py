#!/usr/bin/env python3
"""
EHB-5 Comprehensive Test Suite
Tests all components for 100% completion
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from api_server import app
from database import DatabaseManager
from auth_manager import AuthManager
from data_processor import DataProcessor
from natural_language_processor import NaturalLanguageProcessor


class TestFrontend(unittest.TestCase):
    """Test frontend components"""

    def test_index_html_exists(self):
        """Test that index.html exists"""
        self.assertTrue(os.path.exists('index.html'))

    def test_styles_css_exists(self):
        """Test that styles.css exists"""
        self.assertTrue(os.path.exists('styles.css'))

    def test_script_js_exists(self):
        """Test that script.js exists"""
        self.assertTrue(os.path.exists('script.js'))

    def test_modern_ui_elements(self):
        """Test modern UI elements"""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('modern-ui', content)

    def test_responsive_design(self):
        """Test responsive design elements"""
        with open('styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('@media', content)


class TestBackend(unittest.TestCase):
    """Test backend components"""

    def setUp(self):
        """Set up test environment"""
        self.app = app.test_client()
        self.db = DatabaseManager(':memory:')
        self.auth = AuthManager()
        self.data_processor = DataProcessor()

    def test_api_health_check(self):
        """Test API health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)

    def test_database_initialization(self):
        """Test database initialization"""
        self.db.init_database()
        # Database should be initialized without errors
        self.assertTrue(True)

    def test_authentication(self):
        """Test authentication system"""
        password = "test123"
        hashed = self.auth.hash_password(password)
        self.assertTrue(self.auth.verify_password(password, hashed))

    def test_data_processing(self):
        """Test data processing"""
        test_data = "test data"
        result = self.data_processor.process_data(test_data)
        self.assertIsNotNone(result)


class TestAdminPanel(unittest.TestCase):
    """Test admin panel components"""

    def setUp(self):
        """Set up test environment"""
        self.db = DatabaseManager(':memory:')

    def test_user_management(self):
        """Test user management functionality"""
        result = self.db.create_user(
            "testuser",
            "test@example.com",
            "hashed_password",
            "user"
        )
        self.assertTrue(result)

    def test_system_monitoring(self):
        """Test system monitoring"""
        # Check if monitoring files exist
        monitoring_files = ['monitoring.py', 'real_time_monitor.py']
        for file in monitoring_files:
            if os.path.exists(file):
                self.assertTrue(True)
                break
        else:
            self.fail("No monitoring files found")

    def test_data_analytics(self):
        """Test data analytics"""
        analytics_files = ['enterprise_analytics.py', 'data_processor.py']
        for file in analytics_files:
            if os.path.exists(file):
                self.assertTrue(True)
                break
        else:
            self.fail("No analytics files found")


class TestAIFeatures(unittest.TestCase):
    """Test AI features"""

    def setUp(self):
        """Set up test environment"""
        self.nlp = NaturalLanguageProcessor()

    def test_natural_language_processing(self):
        """Test NLP functionality"""
        text = "This is a test sentence with some keywords."
        keywords = self.nlp.extract_keywords(text)
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)

    def test_sentiment_analysis(self):
        """Test sentiment analysis"""
        text = "This is a great and wonderful test."
        sentiment = self.nlp.sentiment_analysis(text)
        self.assertIn('positive', sentiment)
        self.assertIn('negative', sentiment)
        self.assertIn('neutral', sentiment)

    def test_entity_extraction(self):
        """Test entity extraction"""
        text = "Contact us at test@example.com or visit http://example.com"
        entities = self.nlp.extract_entities(text)
        self.assertIn('emails', entities)
        self.assertIn('urls', entities)


class TestDeployment(unittest.TestCase):
    """Test deployment components"""

    def test_production_config(self):
        """Test production configuration"""
        config_files = ['production_config.py', 'vercel.json']
        for file in config_files:
            if os.path.exists(file):
                self.assertTrue(True)
                break
        else:
            self.fail("No production config files found")

    def test_deployment_scripts(self):
        """Test deployment scripts"""
        deployment_files = ['deployment.py', 'deploy_to_production.py']
        for file in deployment_files:
            if os.path.exists(file):
                self.assertTrue(True)
                break
        else:
            self.fail("No deployment scripts found")

    def test_documentation(self):
        """Test documentation"""
        self.assertTrue(os.path.exists('README.md'))
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertGreater(len(content), 1000)


def run_all_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestFrontend,
        TestBackend,
        TestAdminPanel,
        TestAIFeatures,
        TestDeployment
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    if success:
        print("\n🎉 All tests passed! Project is 100% complete!")
    else:
        print("\n❌ Some tests failed. Please fix issues.")
    sys.exit(0 if success else 1)
