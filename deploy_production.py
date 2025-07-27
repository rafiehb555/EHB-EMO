#!/usr/bin/env python3
"""
EHB Production Deployment Script
Deploy the World's Best AI Agent to production
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class ProductionDeployer:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "deployment_steps": [],
            "successful_steps": [],
            "failed_steps": [],
            "summary": {}
        }
    
    def deploy_docker(self):
        """Deploy using Docker"""
        print("🐳 Deploying with Docker...")
        
        try:
            # Build Docker image
            subprocess.run(["docker", "build", "-t", "world-best-ai-agent", "."], check=True)
            print("✅ Docker image built successfully")
            self.results["successful_steps"].append("Docker build")
            
            # Run Docker container
            subprocess.run([
                "docker", "run", "-d", 
                "--name", "ai-agent-container",
                "-p", "8000:8000",
                "-e", "OPENAI_API_KEY=dummy",
                "-e", "ANTHROPIC_API_KEY=dummy",
                "-e", "COHERE_API_KEY=dummy",
                "world-best-ai-agent"
            ], check=True)
            print("✅ Docker container started successfully")
            self.results["successful_steps"].append("Docker run")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker deployment failed: {e}")
            self.results["failed_steps"].append(f"Docker: {e}")
    
    def deploy_docker_compose(self):
        """Deploy using Docker Compose"""
        print("🐳 Deploying with Docker Compose...")
        
        try:
            # Start services
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("✅ Docker Compose services started")
            self.results["successful_steps"].append("Docker Compose")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker Compose failed: {e}")
            self.results["failed_steps"].append(f"Docker Compose: {e}")
    
    def deploy_kubernetes(self):
        """Deploy to Kubernetes"""
        print("☸️ Deploying to Kubernetes...")
        
        try:
            # Apply Kubernetes manifests
            subprocess.run(["kubectl", "apply", "-f", "kubernetes/"], check=True)
            print("✅ Kubernetes deployment applied")
            self.results["successful_steps"].append("Kubernetes deployment")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Kubernetes deployment failed: {e}")
            self.results["failed_steps"].append(f"Kubernetes: {e}")
    
    def setup_monitoring(self):
        """Setup monitoring"""
        print("📊 Setting up monitoring...")
        
        try:
            # Start Prometheus
            subprocess.run(["docker", "run", "-d", "--name", "prometheus", "-p", "9090:9090", "prom/prometheus"], check=True)
            print("✅ Prometheus started")
            self.results["successful_steps"].append("Prometheus")
            
            # Start Grafana
            subprocess.run(["docker", "run", "-d", "--name", "grafana", "-p", "3000:3000", "grafana/grafana"], check=True)
            print("✅ Grafana started")
            self.results["successful_steps"].append("Grafana")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Monitoring setup failed: {e}")
            self.results["failed_steps"].append(f"Monitoring: {e}")
    
    def run_health_checks(self):
        """Run health checks"""
        print("🏥 Running health checks...")
        
        import time

        import requests
        
        endpoints = [
            "http://localhost:8000/health",
            "http://localhost:9090/-/healthy",
            "http://localhost:3000/api/health"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {endpoint}: Healthy")
                    self.results["successful_steps"].append(f"Health check: {endpoint}")
                else:
                    print(f"⚠️ {endpoint}: Status {response.status_code}")
                    self.results["failed_steps"].append(f"Health check: {endpoint}")
            except Exception as e:
                print(f"❌ {endpoint}: Failed - {e}")
                self.results["failed_steps"].append(f"Health check: {endpoint}")
    
    def run_performance_tests(self):
        """Run performance tests"""
        print("⚡ Running performance tests...")
        
        try:
            import time

            import requests

            # Test response time
            start_time = time.time()
            response = requests.get("http://localhost:8000/health", timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:
                print(f"✅ Response time: {response_time:.2f}s (Good)")
                self.results["successful_steps"].append("Performance test")
            else:
                print(f"⚠️ Response time: {response_time:.2f}s (Slow)")
                self.results["failed_steps"].append("Performance test")
            
        except Exception as e:
            print(f"❌ Performance test failed: {e}")
            self.results["failed_steps"].append(f"Performance test: {e}")
    
    def generate_deployment_report(self):
        """Generate deployment report"""
        print("\n" + "=" * 60)
        print("📊 DEPLOYMENT REPORT")
        print("=" * 60)
        
        total_steps = len(self.results["successful_steps"]) + len(self.results["failed_steps"])
        successful_steps = len(self.results["successful_steps"])
        failed_steps = len(self.results["failed_steps"])
        
        if total_steps > 0:
            success_rate = (successful_steps / total_steps) * 100
        else:
            success_rate = 0
        
        print(f"✅ Successful Steps: {successful_steps}")
        print(f"❌ Failed Steps: {failed_steps}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Production deployment successful!")
        elif success_rate >= 70:
            print("✅ GOOD! Production deployment mostly successful!")
        else:
            print("⚠️ Production deployment needs attention")
        
        # Show successful steps
        if self.results["successful_steps"]:
            print("\n✅ SUCCESSFUL STEPS:")
            for step in self.results["successful_steps"]:
                print(f"  ✅ {step}")
        
        # Show failed steps
        if self.results["failed_steps"]:
            print("\n❌ FAILED STEPS:")
            for step in self.results["failed_steps"]:
                print(f"  ❌ {step}")
        
        # Save report
        report_file = f"reports/production_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 60)
        
        self.results["summary"] = {
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "failed_steps": failed_steps,
            "success_rate": success_rate,
            "report_file": report_file
        }
    
    def deploy_to_production(self):
        """Main deployment process"""
        print("🚀 EHB Production Deployment")
        print("=" * 60)
        print("Deploying World's Best AI Agent to production...")
        print("=" * 60)
        
        try:
            # Step 1: Docker deployment
            self.deploy_docker()
            
            # Step 2: Docker Compose deployment
            self.deploy_docker_compose()
            
            # Step 3: Kubernetes deployment (if available)
            try:
                self.deploy_kubernetes()
            except:
                print("⚠️ Kubernetes not available, skipping...")
            
            # Step 4: Setup monitoring
            self.setup_monitoring()
            
            # Step 5: Health checks
            self.run_health_checks()
            
            # Step 6: Performance tests
            self.run_performance_tests()
            
            # Step 7: Generate report
            self.generate_deployment_report()
            
            print("✅ Production deployment process completed")
            
        except Exception as e:
            print(f"❌ Production deployment failed: {e}")
            self.results["summary"]["status"] = "failed"
            self.results["summary"]["error"] = str(e)
        
        return self.results

def main():
    """Main function"""
    try:
        deployer = ProductionDeployer()
        results = deployer.deploy_to_production()
        
        if results["summary"]["success_rate"] >= 70:
            print("\n🎉 Production deployment successful!")
            return 0
        else:
            print(f"\n⚠️ Production deployment at {results['summary']['success_rate']:.1f}% - needs attention")
            return 1
            
    except Exception as e:
        print(f"❌ Production deployment failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 