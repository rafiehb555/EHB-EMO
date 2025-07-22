#!/usr/bin/env python3
"""
EHB-5 AI Agents Module
Implements intelligent agents for data processing, configuration management, and system automation
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from database import db
from data_processor import DataProcessor


class BaseAgent:
    """Base class for all AI agents"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "active"
        self.last_activity = datetime.now().isoformat()
        self.tasks = []

    def log_activity(self, action: str, status: str = "completed"):
        """Log agent activity"""
        activity = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "status": status
        }

        # Log to database
        db.log_system_event('INFO', f"{self.name}: {action}")

        return activity

    def update_status(self, status: str):
        """Update agent status"""
        self.status = status
        self.last_activity = datetime.now().isoformat()


class DataProcessorAgent(BaseAgent):
    """AI Agent for data processing and analysis"""

    def __init__(self):
        super().__init__(
            "Data Processing Agent",
            "Handles data processing and analysis"
        )
        self.data_processor = DataProcessor()
        self.tasks = ["data_analysis", "file_processing", "report_generation"]

    def analyze_data(self, data: Any) -> Dict:
        """Analyze data using the data processor"""
        try:
            result = self.data_processor.process_data(data, 'analyze')
            self.log_activity("Data analysis completed")
            return result
        except Exception as e:
            self.log_activity(f"Data analysis failed: {str(e)}", "error")
            return {"error": str(e)}

    def process_file(self, file_path: str) -> Dict:
        """Process a file and extract insights"""
        try:
            if not os.path.exists(file_path):
                return {"error": "File not found"}

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Analyze file content
            analysis = self.analyze_data(content)

            # Generate report
            report = {
                "file_path": file_path,
                "file_size": len(content),
                "analysis": analysis,
                "processed_at": datetime.now().isoformat()
            }

            self.log_activity(f"File processed: {file_path}")
            return report

        except Exception as e:
            self.log_activity(f"File processing failed: {str(e)}", "error")
            return {"error": str(e)}

    def generate_report(self, data_files: List[str]) -> Dict:
        """Generate comprehensive report from multiple files"""
        try:
            reports = []
            total_files = len(data_files)

            for i, file_path in enumerate(data_files, 1):
                report = self.process_file(file_path)
                reports.append(report)

                # Log progress
                self.log_activity(f"Processed {i}/{total_files} files")

            summary = {
                "total_files": total_files,
                "successful_processing": len([r for r in reports if "error" not in r]),
                "failed_processing": len([r for r in reports if "error" in r]),
                "reports": reports,
                "generated_at": datetime.now().isoformat()
            }

            self.log_activity("Report generation completed")
            return summary

        except Exception as e:
            self.log_activity(f"Report generation failed: {str(e)}", "error")
            return {"error": str(e)}


class ConfigManagerAgent(BaseAgent):
    """AI Agent for configuration management"""

    def __init__(self):
        super().__init__(
            "Configuration Manager",
            "Manages project configurations and settings"
        )
        self.tasks = [
            "config_validation",
            "settings_sync",
            "environment_setup"]

    def validate_config(self, config_data: Dict) -> Dict:
        """Validate configuration data"""
        try:
            errors = []
            warnings = []

            # Check required fields
            required_fields = ["project", "version", "settings"]
            for field in required_fields:
                if field not in config_data:
                    errors.append(f"Missing required field: {field}")

            # Validate settings
            if "settings" in config_data:
                settings = config_data["settings"]
                if "database" not in settings:
                    warnings.append("Database setting not specified")
                if "api" not in settings:
                    warnings.append("API setting not specified")

            validation_result = {
                "is_valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "validated_at": datetime.now().isoformat()
            }

            self.log_activity("Configuration validation completed")
            return validation_result

        except Exception as e:
            self.log_activity(
                f"Configuration validation failed: {str(e)}", "error")
            return {"error": str(e)}

    def sync_settings(self, config_file: str = "config.json") -> Dict:
        """Synchronize settings across the system"""
        try:
            if not os.path.exists(config_file):
                return {"error": "Configuration file not found"}

            with open(config_file, 'r') as f:
                config = json.load(f)

            # Validate configuration
            validation = self.validate_config(config)

            # Update system settings
            if validation.get("is_valid", False):
                # Update database settings
                db_settings = config.get("settings", {})
                if db_settings.get("database") == "enabled":
                    db.log_system_event(
                        'INFO', 'Database settings synchronized')

                # Update API settings
                if db_settings.get("api") == "active":
                    db.log_system_event('INFO', 'API settings synchronized')

            sync_result = {
                "config_file": config_file,
                "validation": validation,
                "synced_at": datetime.now().isoformat()
            }

            self.log_activity("Settings synchronization completed")
            return sync_result

        except Exception as e:
            self.log_activity(f"Settings sync failed: {str(e)}", "error")
            return {"error": str(e)}

    def setup_environment(self) -> Dict:
        """Set up the development environment"""
        try:
            setup_steps = []

            # Check Python environment
            import sys
            setup_steps.append({
                "step": "Python Environment",
                "status": "completed",
                "details": f"Python {sys.version}"
            })

            # Check required files
            required_files = ["config.json", "database.py", "api_server.py"]
            for file in required_files:
                if os.path.exists(file):
                    setup_steps.append({
                        "step": f"File Check: {file}",
                        "status": "completed",
                        "details": "File exists"
                    })
                else:
                    setup_steps.append({
                        "step": f"File Check: {file}",
                        "status": "failed",
                        "details": "File missing"
                    })

            # Check database
            try:
                projects = db.get_all_projects()
                setup_steps.append({
                    "step": "Database Connection",
                    "status": "completed",
                    "details": f"Connected, {len(projects)} projects found"
                })
            except Exception as e:
                setup_steps.append({
                    "step": "Database Connection",
                    "status": "failed",
                    "details": str(e)
                })

            setup_result = {
                "steps": setup_steps,
                "total_steps": len(setup_steps),
                "completed_steps": len([s for s in setup_steps if s["status"] == "completed"]),
                "setup_at": datetime.now().isoformat()
            }

            self.log_activity("Environment setup completed")
            return setup_result

        except Exception as e:
            self.log_activity(f"Environment setup failed: {str(e)}", "error")
            return {"error": str(e)}


class FileOrganizerAgent(BaseAgent):
    """AI Agent for file organization and management"""

    def __init__(self):
        super().__init__(
            "File Organizer Agent",
            "Organizes and manages project files"
        )
        self.tasks = ["file_scanning", "formatting", "backup_management"]

    def scan_files(self, directory: str = ".") -> Dict:
        """Scan and categorize files in the directory"""
        try:
            files = []
            categories = {
                "python": [],
                "javascript": [],
                "html": [],
                "css": [],
                "json": [],
                "markdown": [],
                "other": []
            }

            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    file_ext = os.path.splitext(filename)[1].lower()

                    file_info = {
                        "name": filename,
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "modified": datetime.fromtimestamp(
                            os.path.getmtime(file_path)).isoformat()}

                    files.append(file_info)

                    # Categorize by extension
                    if file_ext == '.py':
                        categories["python"].append(file_info)
                    elif file_ext in ['.js', '.ts']:
                        categories["javascript"].append(file_info)
                    elif file_ext == '.html':
                        categories["html"].append(file_info)
                    elif file_ext == '.css':
                        categories["css"].append(file_info)
                    elif file_ext == '.json':
                        categories["json"].append(file_info)
                    elif file_ext in ['.md', '.txt']:
                        categories["markdown"].append(file_info)
                    else:
                        categories["other"].append(file_info)

            scan_result = {
                "total_files": len(files),
                "categories": categories,
                "scanned_at": datetime.now().isoformat()
            }

            self.log_activity(f"File scan completed: {len(files)} files found")
            return scan_result

        except Exception as e:
            self.log_activity(f"File scan failed: {str(e)}", "error")
            return {"error": str(e)}

    def format_files(self, file_patterns: List[str] = None) -> Dict:
        """Format files according to standards"""
        try:
            if file_patterns is None:
                file_patterns = ["*.py", "*.js", "*.json"]

            formatted_files = []

            for pattern in file_patterns:
                import glob
                matching_files = glob.glob(pattern)

                for file_path in matching_files:
                    try:
                        # Basic formatting (in a real implementation, you'd use
                        # tools like black, prettier, etc.)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Simple formatting: remove trailing whitespace
                        formatted_content = '\n'.join(
                            line.rstrip() for line in content.splitlines())

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(formatted_content)

                        formatted_files.append({
                            "file": file_path,
                            "status": "formatted"
                        })

                    except Exception as e:
                        formatted_files.append({
                            "file": file_path,
                            "status": "error",
                            "error": str(e)
                        })

            format_result = {
                "formatted_files": formatted_files,
                "total_processed": len(formatted_files),
                "formatted_at": datetime.now().isoformat()
            }

            self.log_activity(
                f"File formatting completed: {len(formatted_files)} files processed")
            return format_result

        except Exception as e:
            self.log_activity(f"File formatting failed: {str(e)}", "error")
            return {"error": str(e)}

    def create_backup(self, backup_dir: str = "backups") -> Dict:
        """Create backup of important files"""
        try:
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            important_files = [
                "config.json", "database.py", "api_server.py",
                "auth_manager.py", "data_processor.py", "main.py"
            ]

            backup_files = []
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for file_path in important_files:
                if os.path.exists(file_path):
                    backup_path = os.path.join(
                        backup_dir, f"{file_path}_{timestamp}")

                    import shutil
                    shutil.copy2(file_path, backup_path)

                    backup_files.append({
                        "original": file_path,
                        "backup": backup_path,
                        "size": os.path.getsize(file_path)
                    })

            backup_result = {
                "backup_files": backup_files,
                "backup_dir": backup_dir,
                "total_backed_up": len(backup_files),
                "backup_created_at": datetime.now().isoformat()
            }

            self.log_activity(
                f"Backup created: {len(backup_files)} files backed up")
            return backup_result

        except Exception as e:
            self.log_activity(f"Backup creation failed: {str(e)}", "error")
            return {"error": str(e)}


class CodeAnalyzerAgent(BaseAgent):
    """AI Agent for code analysis and quality assessment"""

    def __init__(self):
        super().__init__(
            "Code Analysis Agent",
            "Analyzes code quality and provides suggestions"
        )
        self.tasks = ["linting", "code_review", "optimization_suggestions"]

    def analyze_code_quality(self, file_path: str) -> Dict:
        """Analyze code quality of a file"""
        try:
            if not os.path.exists(file_path):
                return {"error": "File not found"}

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.splitlines()
            analysis = {
                "file_path": file_path,
                "total_lines": len(lines),
                "non_empty_lines": len([line for line in lines if line.strip()]),
                "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
                "issues": [],
                "suggestions": []
            }

            # Basic code analysis
            for i, line in enumerate(lines, 1):
                line = line.strip()

                # Check for long lines
                if len(line) > 79:
                    analysis["issues"].append({
                        "line": i,
                        "type": "long_line",
                        "message": f"Line {i} is too long ({len(line)} characters)"
                    })

                # Check for trailing whitespace
                if line and line != line.rstrip():
                    analysis["suggestions"].append({
                        "line": i,
                        "type": "trailing_whitespace",
                        "message": f"Remove trailing whitespace on line {i}"
                    })

            # Calculate code quality score
            total_issues = len(analysis["issues"])
            total_suggestions = len(analysis["suggestions"])

            if total_issues == 0:
                analysis["quality_score"] = "excellent"
            elif total_issues <= 5:
                analysis["quality_score"] = "good"
            elif total_issues <= 10:
                analysis["quality_score"] = "fair"
            else:
                analysis["quality_score"] = "needs_improvement"

            analysis["analyzed_at"] = datetime.now().isoformat()

            self.log_activity(f"Code analysis completed for {file_path}")
            return analysis

        except Exception as e:
            self.log_activity(f"Code analysis failed: {str(e)}", "error")
            return {"error": str(e)}

    def review_project_code(self) -> Dict:
        """Review all code files in the project"""
        try:
            python_files = []

            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))

            reviews = []
            total_issues = 0
            total_suggestions = 0

            for file_path in python_files:
                review = self.analyze_code_quality(file_path)
                if "error" not in review:
                    reviews.append(review)
                    total_issues += len(review.get("issues", []))
                    total_suggestions += len(review.get("suggestions", []))

            project_review = {
                "files_reviewed": len(reviews),
                "total_issues": total_issues,
                "total_suggestions": total_suggestions,
                "reviews": reviews,
                "reviewed_at": datetime.now().isoformat()
            }

            self.log_activity(
                f"Project code review completed: {len(reviews)} files reviewed")
            return project_review

        except Exception as e:
            self.log_activity(f"Project code review failed: {str(e)}", "error")
            return {"error": str(e)}


class DeploymentManagerAgent(BaseAgent):
    """AI Agent for deployment and release management"""

    def __init__(self):
        super().__init__(
            "Deployment Manager",
            "Manages project deployment and releases"
        )
        self.tasks = ["build_management", "deployment", "version_control"]

    def check_deployment_readiness(self) -> Dict:
        """Check if the project is ready for deployment"""
        try:
            checks = []

            # Check required files
            required_files = [
                "main.py", "api_server.py", "database.py",
                "auth_manager.py", "data_processor.py", "requirements.txt"
            ]

            for file in required_files:
                if os.path.exists(file):
                    checks.append({
                        "check": f"File exists: {file}",
                        "status": "passed"
                    })
                else:
                    checks.append({
                        "check": f"File exists: {file}",
                        "status": "failed"
                    })

            # Check database
            try:
                projects = db.get_all_projects()
                checks.append({
                    "check": "Database connectivity",
                    "status": "passed",
                    "details": f"Connected, {len(projects)} projects found"
                })
            except Exception as e:
                checks.append({
                    "check": "Database connectivity",
                    "status": "failed",
                    "details": str(e)
                })

            # Check dependencies
            try:
                import flask
                checks.append({
                    "check": "Flask dependency",
                    "status": "passed"
                })
            except ImportError:
                checks.append({
                    "check": "Flask dependency",
                    "status": "failed"
                })

            passed_checks = len([c for c in checks if c["status"] == "passed"])
            total_checks = len(checks)

            readiness_result = {
                "checks": checks,
                "passed_checks": passed_checks,
                "total_checks": total_checks,
                "readiness_percentage": (
                    passed_checks /
                    total_checks) *
                100 if total_checks > 0 else 0,
                "ready_for_deployment": passed_checks == total_checks,
                "checked_at": datetime.now().isoformat()}

            self.log_activity("Deployment readiness check completed")
            return readiness_result

        except Exception as e:
            self.log_activity(
                f"Deployment readiness check failed: {str(e)}", "error")
            return {"error": str(e)}

# Agent Manager


class AgentManager:
    """Manages all AI agents"""

    def __init__(self):
        self.agents = {
            "dataProcessor": DataProcessorAgent(),
            "configManager": ConfigManagerAgent(),
            "fileOrganizer": FileOrganizerAgent(),
            "codeAnalyzer": CodeAnalyzerAgent(),
            "deploymentManager": DeploymentManagerAgent()
        }

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get a specific agent"""
        return self.agents.get(agent_name)

    def get_all_agents(self) -> Dict[str, BaseAgent]:
        """Get all agents"""
        return self.agents

    def run_agent_task(self, agent_name: str, task: str, **kwargs) -> Dict:
        """Run a specific task on an agent"""
        agent = self.get_agent(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}

        try:
            if hasattr(agent, task):
                method = getattr(agent, task)
                return method(**kwargs)
            else:
                return {"error": f"Task {task} not found in agent {agent_name}"}
        except Exception as e:
            return {"error": f"Task execution failed: {str(e)}"}

    def get_agents_status(self) -> Dict:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "name": agent.name,
                "status": agent.status,
                "last_activity": agent.last_activity,
                "tasks": agent.tasks
            }
        return status


# Global agent manager instance
agent_manager = AgentManager()
