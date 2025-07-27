#!/usr/bin/env python3
"""
EHB Complete System Test - Test everything to 100%
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path


class CompleteSystemTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": [],
            "tests_failed": [],
            "performance_metrics": {},
            "summary": {}
        }
    
    async def test_ai_agent(self):
        """Test AI agent functionality"""
        print("🧪 Testing AI Agent...")
        
        try:
            from world_best_agent_simple_final import WorldBestAIAgent

            # Create agent
            agent = WorldBestAIAgent()
            
            # Test basic functionality
            assert agent.name == "World's Best AI Agent"
            assert agent.version == "2.0.0"
            assert agent.is_active == True
            
            # Test text processing
            response = await agent.process_input({"type": "text", "text": "Test message"})
            assert response["status"] == "success"
            assert "response" in response
            
            # Test code processing
            response = await agent.process_input({"type": "code", "code": "print('test')", "language": "python"})
            assert response["status"] == "success"
            
            # Test data processing
            response = await agent.process_input({"type": "data", "data": "test data"})
            assert response["status"] == "success"
            
            # Test learning
            experience = {"input": "test", "output": "test", "success": True}
            result = await agent.learn(experience)
            assert result == True
            
            # Test planning
            plan = await agent.plan("test goal")
            assert isinstance(plan, list)
            assert len(plan) > 0
            
            # Test execution
            result = await agent.execute("test action")
            assert result["status"] == "completed"
            
            # Test status
            status = agent.get_status()
            assert "agent_id" in status
            assert "uptime" in status
            
            # Test metrics
            metrics = agent.get_metrics()
            assert "requests_processed" in metrics
            
            print("✅ AI Agent tests passed")
            self.results["tests_passed"].append("AI Agent functionality")
            
        except Exception as e:
            print(f"❌ AI Agent test failed: {e}")
            self.results["tests_failed"].append(f"AI Agent: {e}")
    
    def test_file_structure(self):
        """Test file structure completeness"""
        print("📁 Testing file structure...")
        
        required_files = [
            "requirements.txt",
            "docker-compose.yml",
            "Dockerfile",
            "world_best_agent_simple_final.py",
            "complete_100_percent_fixed.py"
        ]
        
        required_dirs = [
            "ai_agents",
            "ai_models",
            "ai_data",
            "ai_configs",
            "logs",
            "reports",
            "tests"
        ]
        
        all_passed = True
        
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ File exists: {file_path}")
                self.results["tests_passed"].append(f"File: {file_path}")
            else:
                print(f"❌ Missing file: {file_path}")
                self.results["tests_failed"].append(f"Missing file: {file_path}")
                all_passed = False
        
        for dir_path in required_dirs:
            if Path(dir_path).exists():
                print(f"✅ Directory exists: {dir_path}")
                self.results["tests_passed"].append(f"Directory: {dir_path}")
            else:
                print(f"❌ Missing directory: {dir_path}")
                self.results["tests_failed"].append(f"Missing directory: {dir_path}")
                all_passed = False
        
        if all_passed:
            print("✅ File structure tests passed")
        else:
            print("❌ Some file structure tests failed")
    
    def test_dependencies(self):
        """Test all dependencies"""
        print("📦 Testing dependencies...")
        
        dependencies = [
            "openai", "anthropic", "cohere", "transformers", "torch", "tensorflow",
            "scikit-learn", "numpy", "pandas", "matplotlib", "seaborn", "jupyter",
            "streamlit", "gradio", "fastapi", "uvicorn", "sqlalchemy", "redis",
            "celery", "pydantic", "python-dotenv", "python-jose", "passlib",
            "bcrypt", "httpx", "aiofiles", "python-multipart", "chromadb",
            "pinecone-client", "weaviate-client", "qdrant-client", "milvus",
            "faiss-cpu", "sentencepiece", "protobuf", "grpcio", "grpcio-tools",
            "sentence-transformers", "huggingface_hub", "aiohttp", "PyJWT",
            "cryptography", "prometheus_client", "elasticsearch", "loguru",
            "rich", "psutil", "tqdm", "click", "typer", "marshmallow",
            "cerberus", "jsonschema", "pyyaml", "toml", "configparser"
        ]
        
        passed = 0
        failed = 0
        
        for dep in dependencies:
            try:
                __import__(dep.replace("-", "_"))
                print(f"✅ {dep}: Available")
                self.results["tests_passed"].append(f"Dependency: {dep}")
                passed += 1
            except ImportError:
                print(f"❌ {dep}: Missing")
                self.results["tests_failed"].append(f"Missing dependency: {dep}")
                failed += 1
        
        print(f"📊 Dependencies: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("✅ All dependencies available")
        else:
            print(f"⚠️ {failed} dependencies missing")
    
    def test_performance(self):
        """Test system performance"""
        print("⚡ Testing performance...")
        
        import time

        # Test import performance
        start_time = time.time()
        try:
            from world_best_agent_simple_final import WorldBestAIAgent
            import_time = time.time() - start_time
            
            if import_time < 5.0:
                print(f"✅ Import performance: {import_time:.2f}s")
                self.results["tests_passed"].append("Import performance")
            else:
                print(f"⚠️ Slow import: {import_time:.2f}s")
                self.results["tests_failed"].append("Slow import performance")
            
            self.results["performance_metrics"]["import_time"] = import_time
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            self.results["tests_failed"].append(f"Import failed: {e}")
        
        # Test memory usage
        try:
            import psutil
            memory_usage = psutil.virtual_memory().percent
            print(f"✅ Memory usage: {memory_usage:.1f}%")
            self.results["performance_metrics"]["memory_usage"] = memory_usage
            
            if memory_usage < 80:
                self.results["tests_passed"].append("Memory usage")
            else:
                self.results["tests_failed"].append("High memory usage")
                
        except Exception as e:
            print(f"❌ Memory test failed: {e}")
            self.results["tests_failed"].append(f"Memory test failed: {e}")
    
    def test_security(self):
        """Test security features"""
        print("🔒 Testing security...")
        
        try:
            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            # Test encryption
            test_data = b"test data"
            encrypted = cipher.encrypt(test_data)
            decrypted = cipher.decrypt(encrypted)
            
            assert decrypted == test_data
            print("✅ Encryption/decryption working")
            self.results["tests_passed"].append("Encryption")
            
        except Exception as e:
            print(f"❌ Encryption test failed: {e}")
            self.results["tests_failed"].append(f"Encryption: {e}")
        
        try:
            import secrets

            import jwt

            # Test JWT
            secret = secrets.token_hex(32)
            payload = {"user_id": 123}
            token = jwt.encode(payload, secret, algorithm="HS256")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            
            assert decoded["user_id"] == 123
            print("✅ JWT working")
            self.results["tests_passed"].append("JWT")
            
        except Exception as e:
            print(f"❌ JWT test failed: {e}")
            self.results["tests_failed"].append(f"JWT: {e}")
    
    def test_database(self):
        """Test database functionality"""
        print("🗄️ Testing database...")
        
        try:
            import sqlite3

            # Test SQLite
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO test VALUES (1, 'test')")
            cursor.execute("SELECT * FROM test")
            result = cursor.fetchone()
            
            assert result == (1, "test")
            print("✅ SQLite working")
            self.results["tests_passed"].append("SQLite")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            self.results["tests_failed"].append(f"Database: {e}")
    
    def test_ai_models(self):
        """Test AI model imports"""
        print("🤖 Testing AI models...")
        
        ai_models = [
            "openai", "anthropic", "cohere", "transformers", "torch", "tensorflow",
            "sklearn", "numpy", "pandas", "matplotlib", "seaborn"
        ]
        
        passed = 0
        failed = 0
        
        for model in ai_models:
            try:
                __import__(model)
                print(f"✅ {model}: Available")
                self.results["tests_passed"].append(f"AI Model: {model}")
                passed += 1
            except ImportError:
                print(f"❌ {model}: Missing")
                self.results["tests_failed"].append(f"Missing AI model: {model}")
                failed += 1
        
        print(f"📊 AI Models: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("✅ All AI models available")
        else:
            print(f"⚠️ {failed} AI models missing")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 EHB Complete System Test")
        print("=" * 60)
        print("Running comprehensive system tests...")
        print("=" * 60)
        
        # Run all tests
        await self.test_ai_agent()
        self.test_file_structure()
        self.test_dependencies()
        self.test_performance()
        self.test_security()
        self.test_database()
        self.test_ai_models()
        
        # Generate summary
        self.generate_summary()
        
        return self.results
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results["tests_passed"]) + len(self.results["tests_failed"])
        passed_tests = len(self.results["tests_passed"])
        failed_tests = len(self.results["tests_failed"])
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
        else:
            success_rate = 0
        
        print(f"✅ Tests Passed: {passed_tests}")
        print(f"❌ Tests Failed: {failed_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("🎉 EXCELLENT! System is 95%+ functional!")
        elif success_rate >= 80:
            print("✅ GOOD! System is 80%+ functional!")
        else:
            print("⚠️ System needs more work")
        
        # Show performance metrics
        if self.results["performance_metrics"]:
            print("\n📈 PERFORMANCE METRICS")
            print("=" * 30)
            for key, value in self.results["performance_metrics"].items():
                print(f"{key}: {value}")
        
        # Save results
        report_file = f"reports/complete_system_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 60)
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "report_file": report_file
        }

async def main():
    """Main function"""
    try:
        tester = CompleteSystemTester()
        results = await tester.run_all_tests()
        
        if results["summary"]["success_rate"] >= 95:
            print("\n🎉 Complete system test successful!")
            return 0
        else:
            print(f"\n⚠️ System test at {results['summary']['success_rate']:.1f}% - needs improvement")
            return 1
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main())) 