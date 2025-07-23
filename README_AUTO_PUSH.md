# 🤖 EHB-5 Auto Git Push System

## 🚀 Overview

This system automatically pushes data to GitHub whenever an EHB-5 agent completes a task. It includes:

- **Auto Git Push Script**: Automatically commits and pushes changes
- **Agent Task Manager**: Logs and manages agent tasks
- **Monitoring Mode**: Continuously monitors for changes
- **Batch Scripts**: Easy Windows execution

## 📁 Files

### Core Scripts
- `auto_git_push.py` - Main auto-push script
- `agent_task_manager.py` - Agent task management
- `github_auto_push.bat` - Windows batch script
- `start_auto_monitor.bat` - Auto-monitor starter

## 🛠️ Setup

### 1. Git Configuration
```bash
# Set up Git user (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. GitHub Repository
```bash
# Make sure you're in your project directory
cd /path/to/ehb-5-project

# Check if connected to GitHub
git remote -v
```

## 🚀 Usage

### Quick Start
```bash
# Single push
python auto_git_push.py

# Or use batch script
github_auto_push.bat
```

### Monitor Mode
```bash
# Start continuous monitoring
python auto_git_push.py --monitor --interval 30

# Or use batch script
start_auto_monitor.bat
```

### Agent Task Logging
```python
from agent_task_manager import AgentTasks

# Log different types of tasks
AgentTasks.data_processing_complete("user_data", 1500)
AgentTasks.configuration_updated("database", ["timeout", "connections"])
AgentTasks.security_scan_complete("vulnerability", 0)
AgentTasks.backup_created("system", 245)
AgentTasks.performance_optimization("database", 15)
AgentTasks.api_endpoint_tested("/api/status", "200 OK")
```

## 📊 Task Types

### Data Processing
- **Type**: `data_processing`
- **Description**: Data analysis, transformation, or processing tasks
- **Example**: Processed 1500 user records

### Configuration
- **Type**: `configuration`
- **Description**: System or application configuration changes
- **Example**: Updated database connection settings

### Security
- **Type**: `security`
- **Description**: Security scans, vulnerability checks
- **Example**: Completed vulnerability scan - 0 threats found

### Backup
- **Type**: `backup`
- **Description**: System backups, data exports
- **Example**: Created system backup (245MB)

### Optimization
- **Type**: `optimization`
- **Description**: Performance improvements, optimizations
- **Example**: Optimized database queries - 15% improvement

### API Testing
- **Type**: `api_testing`
- **Description**: API endpoint testing, validation
- **Example**: Tested /api/status - Status: 200 OK

## 🔧 Configuration

### Git Configuration
The script automatically sets up Git configuration:
```python
git_config = {
    'user.name': 'EHB-5 Agent',
    'user.email': 'agent@ehb-5.com'
}
```

### Commit Messages
Auto-generated commit messages include:
- 🤖 Agent task completed - Data updated
- ⚡ Agent processed new data
- 🔧 Agent configuration updated
- 📊 Agent analytics data added
- 🛠️ Agent maintenance completed
- 🚀 Agent performance optimized
- 📈 Agent metrics updated
- 🔒 Agent security enhanced
- 💾 Agent backup created
- 🎯 Agent target achieved

## 📈 Monitoring

### Task Statistics
```bash
python agent_task_manager.py stats
```

### Recent Tasks
```bash
python agent_task_manager.py recent
```

### Example Workflow
```bash
python agent_task_manager.py example
```

## 🔄 Auto-Monitor Mode

The auto-monitor continuously checks for changes and pushes them:

```bash
# Start monitoring (checks every 30 seconds)
python auto_git_push.py --monitor --interval 30
```

**Features:**
- ✅ Automatic change detection
- ✅ Smart commit messages
- ✅ Error handling
- ✅ Logging and notifications
- ✅ Configurable intervals

## 📝 Task Logging

Tasks are automatically logged to `agent_tasks.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "name": "Data Processing",
      "type": "data_processing",
      "description": "Processed 1500 user_data records",
      "timestamp": "2025-01-23T14:30:00",
      "data": {
        "data_type": "user_data",
        "records_processed": 1500,
        "processing_time": "2025-01-23T14:30:00"
      }
    }
  ],
  "last_push": "2025-01-23T14:30:05",
  "auto_push_enabled": true
}
```

## 🚨 Error Handling

The system includes comprehensive error handling:

- ✅ Git configuration errors
- ✅ Network connectivity issues
- ✅ Repository access problems
- ✅ File permission errors
- ✅ Invalid commit messages

## 🔐 Security

### Best Practices
1. **Use SSH Keys**: Set up SSH authentication for GitHub
2. **Token Access**: Use GitHub personal access tokens
3. **Repository Permissions**: Ensure proper repository access
4. **Secure Storage**: Store credentials securely

### SSH Setup
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "agent@ehb-5.com"

# Add to GitHub
# Copy public key to GitHub Settings > SSH Keys
```

## 📱 Integration

### With EHB-5 Agents
```python
# In your agent code
from agent_task_manager import AgentTasks

def process_data():
    # ... your processing code ...

    # Log the task completion
    AgentTasks.data_processing_complete("user_data", len(processed_records))
```

### With Web Dashboard
```javascript
// In your dashboard JavaScript
async function agentTaskComplete(taskType, description) {
    const response = await fetch('/api/agent-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ taskType, description })
    });

    if (response.ok) {
        console.log('Task logged and pushed to GitHub');
    }
}
```

## 🎯 Benefits

### For Development
- ✅ **Automatic Version Control**: All changes tracked
- ✅ **Collaboration**: Team can see agent activities
- ✅ **History**: Complete task history maintained
- ✅ **Backup**: Data automatically backed up to GitHub

### For Monitoring
- ✅ **Real-time Updates**: Immediate push notifications
- ✅ **Task Tracking**: Detailed task logging
- ✅ **Performance Metrics**: Task completion statistics
- ✅ **Error Detection**: Failed tasks identified

### For Management
- ✅ **Transparency**: All agent activities visible
- ✅ **Accountability**: Task completion tracking
- ✅ **Audit Trail**: Complete activity history
- ✅ **Reporting**: Automated task reports

## 🚀 Quick Commands

```bash
# Single push
python auto_git_push.py

# Monitor mode
python auto_git_push.py --monitor

# Log specific task
python auto_git_push.py --task "Data Processing" --description "Processed user data"

# View statistics
python agent_task_manager.py stats

# View recent tasks
python agent_task_manager.py recent

# Run example
python agent_task_manager.py example
```

## 📞 Support

If you encounter issues:

1. **Check Git Status**: `git status`
2. **Verify Remote**: `git remote -v`
3. **Check Permissions**: Ensure GitHub access
4. **Review Logs**: Check console output
5. **Test Manually**: Try manual git push

---

**🎉 Your EHB-5 agents will now automatically push all their work to GitHub!**
