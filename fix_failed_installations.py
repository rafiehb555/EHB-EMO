#!/usr/bin/env python3
"""
Fix Failed Installations with Different Approaches
"""

import json
import subprocess
import sys
from datetime import datetime


class FailedInstallationFixer:
    def __init__(self):
        self.fixed_installations = []
        self.still_failed = []
        
    def fix_transformers(self):
        """Fix transformers installation"""
        print("🔧 Fixing transformers...")
        
        approaches = [
            # Approach 1: Install with specific version
            ["pip", "install", "transformers==4.35.0"],
            # Approach 2: Install with --no-deps
            ["pip", "install", "transformers", "--no-deps"],
            # Approach 3: Install with --force-reinstall
            ["pip", "install", "transformers", "--force-reinstall"],
            # Approach 4: Install from git
            ["pip", "install", "git+https://github.com/huggingface/transformers.git"],
            # Approach 5: Install with conda
            ["conda", "install", "-c", "huggingface", "transformers"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("transformers")
                    print(f"  ✅ transformers fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("transformers")
        return False
    
    def fix_pinecone_client(self):
        """Fix pinecone-client installation"""
        print("🔧 Fixing pinecone-client...")
        
        approaches = [
            # Approach 1: Install with specific version
            ["pip", "install", "pinecone-client==2.2.4"],
            # Approach 2: Install with --no-deps
            ["pip", "install", "pinecone-client", "--no-deps"],
            # Approach 3: Install with --force-reinstall
            ["pip", "install", "pinecone-client", "--force-reinstall"],
            # Approach 4: Install from git
            ["pip", "install", "git+https://github.com/pinecone-io/pinecone-python.git"],
            # Approach 5: Alternative package name
            ["pip", "install", "pinecone-python"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("pinecone-client")
                    print(f"  ✅ pinecone-client fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("pinecone-client")
        return False
    
    def fix_milvus(self):
        """Fix milvus installation"""
        print("🔧 Fixing milvus...")
        
        approaches = [
            # Approach 1: Install pymilvus instead
            ["pip", "install", "pymilvus"],
            # Approach 2: Install with specific version
            ["pip", "install", "pymilvus==2.3.0"],
            # Approach 3: Install with --no-deps
            ["pip", "install", "pymilvus", "--no-deps"],
            # Approach 4: Install from git
            ["pip", "install", "git+https://github.com/milvus-io/pymilvus.git"],
            # Approach 5: Alternative package
            ["pip", "install", "milvus-python"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("pymilvus")
                    print(f"  ✅ milvus fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("milvus")
        return False
    
    def fix_grafana(self):
        """Fix grafana installation"""
        print("🔧 Fixing grafana...")
        
        approaches = [
            # Approach 1: Install grafana-api instead
            ["pip", "install", "grafana-api"],
            # Approach 2: Install with specific version
            ["pip", "install", "grafana-api==1.0.3"],
            # Approach 3: Install with --no-deps
            ["pip", "install", "grafana-api", "--no-deps"],
            # Approach 4: Alternative package
            ["pip", "install", "grafana-client"],
            # Approach 5: Install from git
            ["pip", "install", "git+https://github.com/grafana/grafana-api-python.git"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("grafana-api")
                    print(f"  ✅ grafana fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("grafana")
        return False
    
    def fix_logstash(self):
        """Fix logstash installation"""
        print("🔧 Fixing logstash...")
        
        approaches = [
            # Approach 1: Install logstash-formatter instead
            ["pip", "install", "logstash-formatter"],
            # Approach 2: Install with specific version
            ["pip", "install", "logstash-formatter==0.5.17"],
            # Approach 3: Alternative package
            ["pip", "install", "python-logstash"],
            # Approach 4: Install with --no-deps
            ["pip", "install", "python-logstash", "--no-deps"],
            # Approach 5: Install from git
            ["pip", "install", "git+https://github.com/vklochan/python-logstash.git"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("python-logstash")
                    print(f"  ✅ logstash fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("logstash")
        return False
    
    def fix_autogpt(self):
        """Fix autogpt installation"""
        print("🔧 Fixing autogpt...")
        
        approaches = [
            # Approach 1: Install with specific version
            ["pip", "install", "autogpt==0.4.0"],
            # Approach 2: Install with --no-deps
            ["pip", "install", "autogpt", "--no-deps"],
            # Approach 3: Install from git
            ["pip", "install", "git+https://github.com/Significant-Gravitas/Auto-GPT.git"],
            # Approach 4: Alternative package
            ["pip", "install", "auto-gpt"],
            # Approach 5: Install with --force-reinstall
            ["pip", "install", "auto-gpt", "--force-reinstall"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("auto-gpt")
                    print(f"  ✅ autogpt fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("autogpt")
        return False
    
    def fix_lightgbm(self):
        """Fix lightgbm installation"""
        print("🔧 Fixing lightgbm...")
        
        approaches = [
            # Approach 1: Install with specific version
            ["pip", "install", "lightgbm==4.1.0"],
            # Approach 2: Install with --no-deps
            ["pip", "install", "lightgbm", "--no-deps"],
            # Approach 3: Install with --force-reinstall
            ["pip", "install", "lightgbm", "--force-reinstall"],
            # Approach 4: Install from conda
            ["conda", "install", "-c", "conda-forge", "lightgbm"],
            # Approach 5: Install with specific compiler
            ["pip", "install", "lightgbm", "--no-binary", "lightgbm"]
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"  Trying approach {i}: {' '.join(approach)}")
                result = subprocess.run(approach, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.fixed_installations.append("lightgbm")
                    print(f"  ✅ lightgbm fixed with approach {i}")
                    return True
                else:
                    print(f"  ❌ Approach {i} failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Approach {i} error: {str(e)}")
        
        self.still_failed.append("lightgbm")
        return False
    
    def test_fixed_packages(self):
        """Test all fixed packages"""
        print("\n🧪 Testing Fixed Packages...")
        print("=" * 50)
        
        test_packages = {
            "transformers": "import transformers; print(f'Transformers: {transformers.__version__}')",
            "pinecone-client": "import pinecone; print('Pinecone: Available')",
            "pymilvus": "import pymilvus; print('Milvus: Available')",
            "grafana-api": "import grafana_api; print('Grafana: Available')",
            "python-logstash": "import logstash; print('Logstash: Available')",
            "auto-gpt": "import autogpt; print('AutoGPT: Available')",
            "lightgbm": "import lightgbm; print(f'LightGBM: {lightgbm.__version__}')"
        }
        
        working_packages = []
        failed_packages = []
        
        for package, test_code in test_packages.items():
            try:
                result = subprocess.run([sys.executable, "-c", test_code], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    working_packages.append(package)
                    print(f"✅ {package}: Working")
                else:
                    failed_packages.append(package)
                    print(f"❌ {package}: Failed")
            except Exception as e:
                failed_packages.append(package)
                print(f"❌ {package}: Error - {str(e)}")
        
        return working_packages, failed_packages
    
    def generate_fix_report(self, working_packages, failed_packages):
        """Generate fix report"""
        print("\n" + "=" * 80)
        print("🔧 FAILED INSTALLATIONS FIX REPORT")
        print("=" * 80)
        
        total_fixed = len(self.fixed_installations)
        total_still_failed = len(self.still_failed)
        total_working = len(working_packages)
        total_failed = len(failed_packages)
        
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Packages Fixed: {total_fixed}")
        print(f"❌ Still Failed: {total_still_failed}")
        print(f"✅ Working After Fix: {total_working}")
        print(f"❌ Failed After Fix: {total_failed}")
        
        if self.fixed_installations:
            print("\n✅ SUCCESSFULLY FIXED:")
            for package in self.fixed_installations:
                print(f"  ✅ {package}")
        
        if self.still_failed:
            print("\n❌ STILL FAILED:")
            for package in self.still_failed:
                print(f"  ❌ {package}")
        
        if working_packages:
            print("\n✅ WORKING PACKAGES:")
            for package in working_packages:
                print(f"  ✅ {package}")
        
        if failed_packages:
            print("\n❌ FAILED PACKAGES:")
            for package in failed_packages:
                print(f"  ❌ {package}")
        
        print("\n" + "=" * 80)
        print("🎯 FIX SUMMARY:")
        print(f"✅ Fixed: {total_fixed} packages")
        print(f"❌ Still Failed: {total_still_failed} packages")
        print(f"📈 Fix Success Rate: {round((total_fixed / (total_fixed + total_still_failed)) * 100, 1)}%")
        
        if total_fixed > 0:
            print("🎉 SUCCESS! Some packages were fixed!")
        else:
            print("⚠️  NEEDS MANUAL INTERVENTION! All packages still failed!")
        
        print("=" * 80)
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "fixed_installations": self.fixed_installations,
            "still_failed": self.still_failed,
            "working_packages": working_packages,
            "failed_packages": failed_packages,
            "summary": {
                "total_fixed": total_fixed,
                "total_still_failed": total_still_failed,
                "total_working": total_working,
                "total_failed": total_failed,
                "fix_success_rate": round((total_fixed / (total_fixed + total_still_failed)) * 100, 1) if (total_fixed + total_still_failed) > 0 else 0
            }
        }
        
        with open("fix_failed_installations_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: fix_failed_installations_report.json")
    
    def run_fix_all(self):
        """Run all fixes"""
        print("🔧 Starting Failed Installation Fixes...")
        print("=" * 60)
        
        # Fix all failed packages
        self.fix_transformers()
        self.fix_pinecone_client()
        self.fix_milvus()
        self.fix_grafana()
        self.fix_logstash()
        self.fix_autogpt()
        self.fix_lightgbm()
        
        # Test fixed packages
        working_packages, failed_packages = self.test_fixed_packages()
        
        # Generate report
        self.generate_fix_report(working_packages, failed_packages)
        
        print("\n🎉 Failed Installation Fix Complete!")
        print("🚀 Ready to run EHB AI Development System!")

if __name__ == "__main__":
    fixer = FailedInstallationFixer()
    fixer.run_fix_all() 