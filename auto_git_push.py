#!/usr/bin/env python3
"""
EHB-5 Auto Git Push Script
Automatically pushes data to GitHub when agents complete tasks
"""

import os
import json
import datetime
import subprocess
import time
import threading
from pathlib import Path

class AutoGitPusher:
    def __init__(self):
        self.repo_path = os.getcwd()
        self.git_config = {
            'user.name': 'EHB-5 Agent',
            'user.email': 'agent@ehb-5.com'
        }
        self.commit_messages = [
            "🤖 Agent task completed - Data updated",
            "⚡ Agent processed new data",
            "🔧 Agent configuration updated",
            "📊 Agent analytics data added",
            "🛠️ Agent maintenance completed",
            "🚀 Agent performance optimized",
            "📈 Agent metrics updated",
            "🔒 Agent security enhanced",
            "💾 Agent backup created",
            "🎯 Agent target achieved"
        ]
        self.setup_git()

    def setup_git(self):
        """Setup Git configuration"""
        try:
            for key, value in self.git_config.items():
                subprocess.run(['git', 'config', key, value],
                            cwd=self.repo_path, check=True, capture_output=True)
            print("✅ Git configuration set up successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git config warning: {e}")

    def get_changed_files(self):
        """Get list of changed files"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'],
                                  cwd=self.repo_path, capture_output=True, text=True)
            if result.returncode == 0:
                changed_files = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        status = line[:2]
                        filename = line[3:]
                        changed_files.append({
                            'status': status,
                            'filename': filename
                        })
                return changed_files
        except Exception as e:
            print(f"❌ Error getting changed files: {e}")
        return []

    def add_all_files(self):
        """Add all files to staging"""
        try:
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            print("✅ All files added to staging")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error adding files: {e}")
            return False

    def create_commit(self, message=None):
        """Create a commit with auto-generated message"""
        if not message:
            import random
            message = random.choice(self.commit_messages)

        try:
            subprocess.run(['git', 'commit', '-m', message],
                         cwd=self.repo_path, check=True)
            print(f"✅ Commit created: {message}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating commit: {e}")
            return False

    def push_to_github(self):
        """Push changes to GitHub"""
        try:
            subprocess.run(['git', 'push', 'origin', 'main'],
                         cwd=self.repo_path, check=True)
            print("✅ Changes pushed to GitHub successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pushing to GitHub: {e}")
            return False

    def auto_push(self, task_description=None):
        """Main auto-push function"""
        print(f"\n🚀 Starting auto-push process...")
        print(f"📁 Repository: {self.repo_path}")

        # Check for changes
        changed_files = self.get_changed_files()
        if not changed_files:
            print("ℹ️ No changes detected, skipping push")
            return False

        print(f"📝 Found {len(changed_files)} changed files:")
        for file_info in changed_files:
            print(f"   {file_info['status']} {file_info['filename']}")

        # Add files
        if not self.add_all_files():
            return False

        # Create commit
        commit_message = task_description if task_description else None
        if not self.create_commit(commit_message):
            return False

        # Push to GitHub
        if not self.push_to_github():
            return False

        print("🎉 Auto-push completed successfully!")
        return True

    def monitor_and_push(self, interval=30):
        """Monitor for changes and auto-push"""
        print(f"🔍 Starting auto-monitor (checking every {interval} seconds)...")

        while True:
            try:
                changed_files = self.get_changed_files()
                if changed_files:
                    print(f"🔄 Changes detected, auto-pushing...")
                    self.auto_push()
                else:
                    print(f"⏰ No changes detected at {datetime.datetime.now().strftime('%H:%M:%S')}")

                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n🛑 Auto-monitor stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in auto-monitor: {e}")
                time.sleep(interval)

def create_agent_task_logger():
    """Create a task logger for agents"""
    logger = {
        'tasks': [],
        'last_push': None,
        'auto_push_enabled': True
    }

    def log_task(task_name, task_type, description, data=None):
        """Log a completed task"""
        task = {
            'id': len(logger['tasks']) + 1,
            'name': task_name,
            'type': task_type,
            'description': description,
            'timestamp': datetime.datetime.now().isoformat(),
            'data': data or {}
        }

        logger['tasks'].append(task)

        # Save to file
        with open('agent_tasks.json', 'w') as f:
            json.dump(logger, f, indent=2)

        print(f"📝 Task logged: {task_name}")

        # Auto-push if enabled
        if logger['auto_push_enabled']:
            pusher = AutoGitPusher()
            pusher.auto_push(f"🤖 Agent task: {task_name} - {description}")

        return task

    return log_task

# Global task logger
agent_task_logger = create_agent_task_logger()

def agent_complete_task(task_name, task_type, description, data=None):
    """Function for agents to call when completing tasks"""
    return agent_task_logger(task_name, task_type, description, data)

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='EHB-5 Auto Git Push Script')
    parser.add_argument('--monitor', action='store_true',
                       help='Start monitoring mode')
    parser.add_argument('--interval', type=int, default=30,
                       help='Monitoring interval in seconds')
    parser.add_argument('--task', type=str,
                       help='Log a specific task')
    parser.add_argument('--description', type=str,
                       help='Task description')

    args = parser.parse_args()

    pusher = AutoGitPusher()

    if args.task:
        # Log specific task
        agent_complete_task(args.task, 'manual', args.description or 'Manual task')
    elif args.monitor:
        # Start monitoring mode
        pusher.monitor_and_push(args.interval)
    else:
        # Single push
        pusher.auto_push()

if __name__ == "__main__":
    main()
