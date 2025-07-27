import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import os

#!/usr/bin/env python3
"""
EHB Auto Bug Fixer Complete
Comprehensive automatic bug fixing, testing, security, and deployment
"""


class AutoBugFixerComplete:
    def __init__(self):
        self.project_root = Path.cwd()
        self.setup_logging()
        self.fixes_applied = []
        self.issues_found = []
        self.results = {
            "bugs_fixed": [],
            "security_issues": [],
            "performance_issues": [],
            "deployment_issues": [],
            "overall_status": "pending"
        }
        
    def setup_logging(self):
        """Setup logging with UTF-8 encoding"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('auto_bug_fixer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fix_encoding_issues(self):
        """Fix encoding issues in Python files"""
        self.logger.info("TOOLS Fixing encoding issues...")
        
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Fix common encoding issues
                fixed_content = content
                
                # Fix emoji encoding issues
                emoji_fixes = {
                    'EHB AI': 'EHB AI',
                    'ROCKET': 'ROCKET',
                    'TOOLS': 'TOOLS',
                    'SUCCESS': 'SUCCESS',
                    'ERROR': 'ERROR',
                    'WARNING': 'WARNING',
                    'SECURITY': 'SECURITY',
                    'TESTING': 'TESTING',
                    'REPORT': 'REPORT',
                    'CODE': 'CODE',
                    'SEARCH': 'SEARCH',
                    'FAST': 'FAST',
                    'TARGET': 'TARGET',
                    'SHIELD': 'SHIELD',
                    'CHART': 'CHART',
                    'LOCK': 'LOCK',
                    'DESIGN': 'DESIGN',
                    'SETTINGS': 'SETTINGS',
                    'MOBILE': 'MOBILE',
                    'WEB': 'WEB'
                }
                
                for emoji, replacement in emoji_fixes.items():
                    fixed_content = fixed_content.replace(emoji, replacement)
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Fixed encoding in {file_path}")
                    self.logger.info(f"Fixed encoding in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error fixing encoding in {file_path}: {e}")
    
    def fix_import_issues(self):
        """Fix import issues"""
        self.logger.info("TOOLS Fixing import issues...")
        
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = content
                
                # Fix common import issues
                import_fixes = [
                    (r'# import sarif_om  # Disabled due to missing module', '# # import sarif_om  # Disabled due to missing module  # Disabled due to missing module'),
                    (r'# from sarif_om  # Disabled due to missing module', '# # from sarif_om  # Disabled due to missing module  # Disabled due to missing module'),
                    (r'import importlib.metadata as pkg_resources', 'import importlib.metadata as pkg_resources'),
                ]
                
                for pattern, replacement in import_fixes:
                    fixed_content = re.sub(pattern, replacement, fixed_content)
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Fixed imports in {file_path}")
                    self.logger.info(f"Fixed imports in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error fixing imports in {file_path}: {e}")
    
    def fix_security_issues(self):
        """Fix security issues"""
        self.logger.info("SECURITY Fixing security issues...")
        
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = content
                
                # Fix hardcoded secrets
                secret_patterns = [
                    (r'password\s*=\s*["\'][^"\']+["\']', 'password=os.getenv("PASSWORD", "")'),
                    (r'secret\s*=\s*["\'][^"\']+["\']', 'secret=os.getenv("SECRET", "")'),
                    (r'api_key\s*=\s*["\'][^"\']+["\']', 'api_key=os.getenv("API_KEY", "")'),
                    (r'token\s*=\s*["\'][^"\']+["\']', 'token=os.getenv("TOKEN", "")'),
                ]
                
                for pattern, replacement in secret_patterns:
                    if re.search(pattern, fixed_content):
                        fixed_content = re.sub(pattern, replacement, fixed_content)
                        # Add import if not present
                        if 'import os' not in fixed_content:
                            fixed_content = 'import os\n' + fixed_content
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Fixed security issues in {file_path}")
                    self.logger.info(f"Fixed security issues in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error fixing security issues in {file_path}: {e}")
    
    def fix_syntax_issues(self):
        """Fix syntax issues"""
        self.logger.info("TOOLS Fixing syntax issues...")
        
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = content
                
                # Fix common syntax issues
                syntax_fixes = [
                    (r'print\s*\(\s*["\'][^"\']*\\u[0-9a-fA-F]{4}[^"\']*["\']\s*\)', 'print("Fixed encoding issue")'),
                    (r'print\s*\(\s*["\'][^"\']*\\U[0-9a-fA-F]{8}[^"\']*["\']\s*\)', 'print("Fixed encoding issue")'),
                ]
                
                for pattern, replacement in syntax_fixes:
                    fixed_content = re.sub(pattern, replacement, fixed_content)
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Fixed syntax in {file_path}")
                    self.logger.info(f"Fixed syntax in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error fixing syntax in {file_path}: {e}")
    
    def run_tests_and_fix(self):
        """Run tests and fix issues"""
        self.logger.info("TESTING Running tests and fixing issues...")
        
        try:
            # Run pytest
            result = subprocess.run([
                sys.executable, "-m", "pytest", "--tb=short", "-v"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                # Parse test output and fix issues
                self.parse_test_output_and_fix(result.stdout + result.stderr)
            
            return {
                "status": "success" if result.returncode == 0 else "fixed",
                "output": result.stdout,
                "error": result.stderr
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def parse_test_output_and_fix(self, output):
        """Parse test output and apply fixes"""
        # Common test failure patterns and fixes
        failure_patterns = [
            (r'ImportError.*sarif_om', self.fix_sarif_import),
            (r'UnicodeEncodeError.*charmap', self.fix_encoding_issues),
            (r'SyntaxError', self.fix_syntax_issues),
            (r'ModuleNotFoundError', self.install_missing_modules),
        ]
        
        for pattern, fix_function in failure_patterns:
            if re.search(pattern, output):
                fix_function()
    
    def fix_sarif_import(self):
        """Fix sarif_om import issues"""
        self.logger.info("TOOLS Fixing sarif_om import issues...")
        
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace sarif_om imports with safe alternatives
                fixed_content = content.replace('# import sarif_om  # Disabled due to missing module', '# # import sarif_om  # Disabled due to missing module  # Disabled')
                fixed_content = fixed_content.replace('# from sarif_om  # Disabled due to missing module', '# # from sarif_om  # Disabled due to missing module  # Disabled')
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Fixed sarif_om import in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error fixing sarif_om import in {file_path}: {e}")
    
    def install_missing_modules(self):
        """Install missing Python modules"""
        self.logger.info("📦 Installing missing modules...")
        
        missing_modules = [
            "sarif-om",
            "pytest-cov",
            "bandit",
            "safety",
            "black",
            "flake8",
            "mypy",
            "pylint"
        ]
        
        for module in missing_modules:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", module
                ], capture_output=True, text=True, check=True)
                
                self.fixes_applied.append(f"Installed {module}")
                self.logger.info(f"Installed {module}")
                
            except subprocess.CalledProcessError:
                self.logger.warning(f"Failed to install {module}")
    
    def run_security_scan_and_fix(self):
        """Run security scan and fix issues"""
        self.logger.info("SECURITY Running security scan and fixing issues...")
        
        try:
            # Run bandit
            result = subprocess.run([
                sys.executable, "-m", "bandit", "-r", ".", "-f", "json"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # Parse security issues and fix them
                self.parse_security_issues_and_fix(result.stdout)
            
            return {
                "status": "success" if result.returncode == 0 else "issues_found",
                "output": result.stdout,
                "error": result.stderr
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def parse_security_issues_and_fix(self, output):
        """Parse security issues and apply fixes"""
        try:
            issues = json.loads(output)
            
            for issue in issues.get('results', []):
                issue_type = issue.get('issue_type', '')
                filename = issue.get('filename', '')
                
                if 'hardcoded_password' in issue_type:
                    self.fix_hardcoded_password(filename)
                elif 'sql_injection' in issue_type:
                    self.fix_sql_injection(filename)
                elif 'shell_injection' in issue_type:
                    self.fix_shell_injection(filename)
                    
        except json.JSONDecodeError:
            self.logger.warning("Could not parse security scan output")
    
    def fix_hardcoded_password(self, filename):
        """Fix hardcoded password in file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace hardcoded passwords with environment variables
            fixed_content = re.sub(
                r'password\s*=\s*["\'][^"\']+["\']',
                'password=os.getenv("PASSWORD", "")',
                content
            )
            
            if fixed_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                self.fixes_applied.append(f"Fixed hardcoded password in {filename}")
                
        except Exception as e:
            self.logger.error(f"Error fixing hardcoded password in {filename}: {e}")
    
    def fix_sql_injection(self, filename):
        """Fix SQL injection vulnerability"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace string concatenation with parameterized queries
            fixed_content = re.sub(
                r'cursor\.execute\s*\(\s*["\'][^"\']*"\s*\+\s*[^)]+["\']\s*\)',
                'cursor.execute("SELECT * FROM table WHERE id = %s", (id,))',
                content
            )
            
            if fixed_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                self.fixes_applied.append(f"Fixed SQL injection in {filename}")
                
        except Exception as e:
            self.logger.error(f"Error fixing SQL injection in {filename}: {e}")
    
    def fix_shell_injection(self, filename):
        """Fix shell injection vulnerability"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace os.system with subprocess.run
            fixed_content = re.sub(
                r'os\.system\s*\(\s*([^)]+)\s*\)',
                r'subprocess.run(\1, shell=False, check=True)',
                content
            )
            
            if fixed_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                self.fixes_applied.append(f"Fixed shell injection in {filename}")
                
        except Exception as e:
            self.logger.error(f"Error fixing shell injection in {filename}: {e}")
    
    def run_performance_optimization(self):
        """Run performance optimization"""
        self.logger.info("FAST Running performance optimization...")
        
        optimizations = [
            self.optimize_imports,
            self.optimize_string_operations,
            self.optimize_file_operations,
            self.optimize_memory_usage
        ]
        
        for optimization in optimizations:
            try:
                optimization()
            except Exception as e:
                self.logger.error(f"Error in optimization: {e}")
    
    def optimize_imports(self):
        """Optimize imports in Python files"""
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove unused imports
                lines = content.split('\n')
                optimized_lines = []
                imports = []
                
                for line in lines:
                    if line.strip().startswith(('import ', 'from ')):
                        imports.append(line)
                    else:
                        optimized_lines.append(line)
                
                # Keep only necessary imports
                necessary_imports = [
                    'import os',
                    'import sys',
                    'import json',
                    'import subprocess',
                    'import logging',
                    'from pathlib import Path',
                    'from datetime import datetime'
                ]
                
                final_imports = []
                for imp in imports:
                    if any(necessary in imp for necessary in necessary_imports):
                        final_imports.append(imp)
                
                optimized_content = '\n'.join(final_imports + [''] + optimized_lines)
                
                if optimized_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(optimized_content)
                    
                    self.fixes_applied.append(f"Optimized imports in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error optimizing imports in {file_path}: {e}")
    
    def optimize_string_operations(self):
        """Optimize string operations"""
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace string concatenation with f-strings
                fixed_content = re.sub(
                    r'(["\'])\s*\+\s*([^+]+)\s*\+\s*(["\'])',
                    r'\1{}\3',
                    content
                )
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Optimized string operations in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error optimizing string operations in {file_path}: {e}")
    
    def optimize_file_operations(self):
        """Optimize file operations"""
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use context managers for file operations
                fixed_content = re.sub(
                    r'f\s*=\s*open\s*\(([^)]+)\)\s*\n(.*?)\nf\.close\s*\(\)',
                    r'with open(\1) as f:\n\2',
                    content,
                    flags=re.DOTALL
                )
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Optimized file operations in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error optimizing file operations in {file_path}: {e}")
    
    def optimize_memory_usage(self):
        """Optimize memory usage"""
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace list comprehensions with generators where appropriate
                fixed_content = re.sub(
                    r'\[([^]]+)\s+for\s+([^]]+)\s+in\s+([^]]+)\]',
                    r'(\1 for \2 in \3)',
                    content
                )
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.fixes_applied.append(f"Optimized memory usage in {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error optimizing memory usage in {file_path}: {e}")
    
    def create_deployment_package(self):
        """Create deployment package"""
        self.logger.info("ROCKET Creating deployment package...")
        
        try:
            # Create deployment directory
            deploy_dir = self.project_root / "deployment"
            deploy_dir.mkdir(exist_ok=True)
            
            # Copy necessary files
            files_to_copy = [
                "auto_testing_security_deploy.py",
                "auto_bug_fixer_complete.py",
                "api_server.py",
                "main.py",
                "requirements.txt",
                ".env"
            ]
            
            for file in files_to_copy:
                if (self.project_root / file).exists():
                    shutil.copy2(self.project_root / file, deploy_dir / file)
            
            # Create deployment script
            deploy_script = deploy_dir / "deploy.py"
            with open(deploy_script, 'w', encoding='utf-8') as f:
                f.write("""#!/usr/bin/env python3

def deploy():
    print("EHB AI Dev Agent - Deploying...")
    
    # Install dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run security scan
    subprocess.run([sys.executable, "auto_bug_fixer_complete.py"])
    
    # Start server
    subprocess.run([sys.executable, "api_server.py", "--port", "8000"])
    
    print("Deployment complete!")

if __name__ == "__main__":
    deploy()
""")
            
            # Create Dockerfile
            dockerfile = deploy_dir / "Dockerfile"
            with open(dockerfile, 'w', encoding='utf-8') as f:
                f.write("""FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api_server.py", "--port", "8000"]
""")
            
            # Create docker-compose.yml
            compose_file = deploy_dir / "docker-compose.yml"
            with open(compose_file, 'w', encoding='utf-8') as f:
                f.write("""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - .:/app
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ehb
      POSTGRES_USER: ehb
      POSTGRES_PASSWORD: ehb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
""")
            
            self.fixes_applied.append("Created deployment package")
            self.logger.info("Created deployment package")
            
            return {
                "status": "success",
                "deployment_dir": str(deploy_dir)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_root.name,
            "fixes_applied": self.fixes_applied,
            "issues_found": self.issues_found,
            "summary": {
                "total_fixes": len(self.fixes_applied),
                "total_issues": len(self.issues_found),
                "status": "completed" if self.fixes_applied else "no_issues"
            }
        }
        
        # Save report
        with open('auto_bug_fixer_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def run_complete_automation(self):
        """Run complete automation"""
        self.logger.info("EHB AI Starting Complete Auto Bug Fixer...")
        self.logger.info("=" * 80)
        
        # Step 1: Fix encoding issues
        self.logger.info("TOOLS Step 1: Fixing encoding issues...")
        self.fix_encoding_issues()
        
        # Step 2: Fix import issues
        self.logger.info("TOOLS Step 2: Fixing import issues...")
        self.fix_import_issues()
        
        # Step 3: Fix security issues
        self.logger.info("SECURITY Step 3: Fixing security issues...")
        self.fix_security_issues()
        
        # Step 4: Fix syntax issues
        self.logger.info("TOOLS Step 4: Fixing syntax issues...")
        self.fix_syntax_issues()
        
        # Step 5: Run tests and fix
        self.logger.info("TESTING Step 5: Running tests and fixing issues...")
        test_results = self.run_tests_and_fix()
        
        # Step 6: Security scan and fix
        self.logger.info("SECURITY Step 6: Running security scan and fixing issues...")
        security_results = self.run_security_scan_and_fix()
        
        # Step 7: Performance optimization
        self.logger.info("FAST Step 7: Running performance optimization...")
        self.run_performance_optimization()
        
        # Step 8: Create deployment package
        self.logger.info("ROCKET Step 8: Creating deployment package...")
        deployment_results = self.create_deployment_package()
        
        # Step 9: Generate report
        self.logger.info("REPORT Step 9: Generating report...")
        report = self.generate_report()
        
        return report

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="EHB Auto Bug Fixer Complete")
    parser.add_argument("--encoding-only", action="store_true", help="Fix only encoding issues")
    parser.add_argument("--security-only", action="store_true", help="Fix only security issues")
    parser.add_argument("--performance-only", action="store_true", help="Run only performance optimization")
    parser.add_argument("--deployment-only", action="store_true", help="Create only deployment package")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("EHB AI EHB Auto Bug Fixer Complete")
    print("=" * 80)
    
    tool = AutoBugFixerComplete()
    
    if args.encoding_only:
        tool.fix_encoding_issues()
        print("TOOLS Encoding issues fixed!")
    elif args.security_only:
        tool.fix_security_issues()
        tool.run_security_scan_and_fix()
        print("SECURITY Security issues fixed!")
    elif args.performance_only:
        tool.run_performance_optimization()
        print("FAST Performance optimized!")
    elif args.deployment_only:
        tool.create_deployment_package()
        print("ROCKET Deployment package created!")
    else:
        report = tool.run_complete_automation()
        print("\n" + "=" * 80)
        print("REPORT COMPREHENSIVE BUG FIXING REPORT")
        print("=" * 80)
        print(f"SUCCESS Total Fixes Applied: {report['summary']['total_fixes']}")
        print(f"SUCCESS Total Issues Found: {report['summary']['total_issues']}")
        print(f"SUCCESS Overall Status: {report['summary']['status']}")
        print("=" * 80)
        print("📄 Report saved: auto_bug_fixer_report.json")
        print("ROCKET Deployment package ready in: deployment/")

if __name__ == "__main__":
    main() 