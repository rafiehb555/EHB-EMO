#!/usr/bin/env python3
"""
EMO Auto Cursor Script
Automated development environment setup and monitoring
"""

import sys
import subprocess
import json
import requests
from pathlib import Path


class EMODevSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
        }

    def log(self, message, color='green'):
        """Print colored log message"""
        print(f"{self.colors[color]}{message}{self.colors['reset']}")

    def error(self, message):
        """Print error message"""
        self.log(f"❌ {message}", 'red')

    def success(self, message):
        """Print success message"""
        self.log(f"✅ {message}", 'green')

    def info(self, message):
        """Print info message"""
        self.log(f"ℹ️  {message}", 'blue')

    def warning(self, message):
        """Print warning message"""
        self.log(f"⚠️  {message}", 'yellow')

    def check_node_version(self):
        """Check Node.js version"""
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True, text=True, check=True
            )
            version = result.stdout.strip()
            major_version = int(version.replace('v', '').split('.')[0])

            if major_version >= 18:
                self.success(f"Node.js {version} detected")
                return True
            else:
                self.error(f"Node.js {version} - Need 18+")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.error("Node.js not found")
            return False

    def check_npm_version(self):
        """Check npm version"""
        try:
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True, text=True, check=True
            )
            version = result.stdout.strip()
            self.success(f"npm {version} detected")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.error("npm not found")
            return False

    def install_dependencies(self, project_path, project_name):
        """Install dependencies for a project"""
        try:
            self.info(f"Installing dependencies for {project_name}...")
            subprocess.run(
                ['npm', 'install'],
                cwd=project_path, check=True, capture_output=True
            )
            self.success(f"{project_name} dependencies installed")
            return True
        except subprocess.CalledProcessError:
            self.error(f"Failed to install dependencies for {project_name}")
            return False

    def create_directories(self):
        """Create necessary directories"""
        dirs = [
            'backend/uploads',
            'backend/logs',
            'frontend/public',
            'admin-panel/public',
            'scripts/logs'
        ]

        for dir_path in dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.success(f"Created directory: {dir_path}")

    def setup_environment_files(self):
        """Setup environment files"""
        env_files = [
            ('backend/env.example', 'backend/.env'),
            ('frontend/env.example', 'frontend/.env.local'),
            ('admin-panel/env.example', 'admin-panel/.env.local')
        ]

        for src, dest in env_files:
            src_path = self.project_root / src
            dest_path = self.project_root / dest

            if src_path.exists() and not dest_path.exists():
                import shutil
                shutil.copy2(src_path, dest_path)
                self.success(f"Created {dest}")

    def check_services(self):
        """Check if services are running"""
        services = [
            {'url': 'http://localhost:3000', 'name': 'Frontend'},
            {'url': 'http://localhost:4003/health', 'name': 'Backend API'},
            {'url': 'http://localhost:6001', 'name': 'Admin Panel'}
        ]

        for service in services:
            try:
                response = requests.get(service['url'], timeout=5)
                if response.status_code == 200:
                    self.success(f"{service['name']} is running")
                else:
                    self.warning(
                        f"{service['name']} responded with status "
                        f"{response.status_code}"
                    )
            except requests.exceptions.RequestException:
                self.info(f"{service['name']} is not running")

    def run_health_check(self):
        """Run health check"""
        try:
            result = subprocess.run(
                ['node', 'scripts/health-check.js'],
                cwd=self.project_root, capture_output=True, text=True
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except Exception as e:
            self.error(f"Health check failed: {e}")

    def setup_development_tools(self):
        """Setup additional development tools"""
        tools = [
            {'name': 'ESLint', 'package': 'eslint'},
            {'name': 'Prettier', 'package': 'prettier'},
            {'name': 'Husky', 'package': 'husky'},
            {'name': 'Lint-staged', 'package': 'lint-staged'}
        ]

        for tool in tools:
            try:
                subprocess.run(
                    ['npm', 'install', '--save-dev', tool['package']],
                    cwd=self.project_root, check=True, capture_output=True
                )
                self.success(f"Installed {tool['name']}")
            except subprocess.CalledProcessError:
                self.warning(f"Failed to install {tool['name']}")

    def create_git_hooks(self):
        """Create git hooks for development"""
        git_hooks_dir = self.project_root / '.git' / 'hooks'
        if git_hooks_dir.exists():
            pre_commit_hook = git_hooks_dir / 'pre-commit'
            pre_commit_content = '''#!/bin/sh
# Pre-commit hook for EMO project
echo "Running pre-commit checks..."
npm run lint
npm run test
'''
            pre_commit_hook.write_text(pre_commit_content)
            pre_commit_hook.chmod(0o755)
            self.success("Created git pre-commit hook")

    def setup_monitoring(self):
        """Setup monitoring and logging"""
        monitoring_config = {
            'log_level': 'debug',
            'enable_health_checks': True,
            'enable_performance_monitoring': True,
            'enable_error_tracking': True
        }

        config_file = self.project_root / 'scripts' / 'monitoring-config.json'
        config_file.write_text(json.dumps(monitoring_config, indent=2))
        self.success("Created monitoring configuration")

    def run_setup(self):
        """Main setup function"""
        self.log("🚀 Starting EMO Auto Development Setup...\n")

        # Check prerequisites
        if not self.check_node_version():
            return False
        if not self.check_npm_version():
            return False

        self.info("MongoDB not found. Please install MongoDB or use MongoDB Atlas.")

        # Install dependencies
        projects = [
            {'path': 'backend', 'name': 'Backend'},
            {'path': 'frontend', 'name': 'Frontend'},
            {'path': 'admin-panel', 'name': 'Admin Panel'}
        ]

        for project in projects:
            project_path = self.project_root / project['path']
            if project_path.exists():
                self.install_dependencies(project_path, project['name'])
            else:
                self.error(f"{project['name']} directory not found")

        # Setup environment
        self.create_directories()
        self.setup_environment_files()
        self.setup_development_tools()
        self.create_git_hooks()
        self.setup_monitoring()

        # Check services
        self.check_services()

        # Run health check
        self.run_health_check()

        self.log("\n🎉 Auto setup complete!")
        self.log("\n📋 Next steps:")
        self.log("1. Configure your environment variables in .env files")
        self.log("2. Start MongoDB service")
        self.log("3. Run development servers:")
        self.log("   - Backend: cd backend && npm run dev")
        self.log("   - Frontend: cd frontend && npm run dev")
        self.log("   - Admin Panel: cd admin-panel && npm run dev")
        self.log("   - All: npm run dev")

        return True


def main():
    """Main function"""
    setup = EMODevSetup()
    try:
        success = setup.run_setup()
        if success:
            print("\n✅ Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
