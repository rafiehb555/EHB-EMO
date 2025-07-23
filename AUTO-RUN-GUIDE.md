# 🚀 EHB-5 Intelligent System Auto-Run Guide

## 📋 Overview

The EHB-5 Intelligent System can be automatically started, monitored, and managed using the provided automation scripts. This guide explains how to use the auto-run features effectively.

## 🎯 Quick Start

### Option 1: Simple Auto-Run (Recommended)

```bash

## Double-click this file or run from command line

auto-run.bat

```

### Option 2: PowerShell Direct

```powershell

## Run with auto-start and monitoring

.\auto-run-system.ps1 -AutoStart

## Run with force restart

.\auto-run-system.ps1 -AutoStart -ForceRestart

## Monitor only (if server is already running)

.\auto-run-system.ps1 -MonitorOnly

```

### Option 3: Custom Port

```powershell

## Run on different port

.\auto-run-system.ps1 -AutoStart -Port 3002

```

## 🔧 Auto-Run Features

### ✅ Automatic Features

- **Prerequisites Check**: Node.js, npm, required files
- **Dependency Installation**: Automatic npm install
- **Directory Creation**: Creates necessary folders
- **Port Management**: Frees occupied ports automatically
- **Server Startup**: Starts the intelligent API server
- **Health Monitoring**: Continuous health checks
- **Auto-Recovery**: Restarts server if it fails
- **Dashboard Launch**: Opens browser automatically
- **Real-time Status**: Live system status display
- **Graceful Shutdown**: Clean exit on Ctrl+C

### 📊 Monitoring Features

- **System Metrics**: CPU, Memory, Network, Storage
- **AI Agents Status**: All 5 agents monitoring
- **Health Checks**: Continuous server health verification
- **Auto-Restart**: Up to 5 automatic restarts
- **Error Logging**: Comprehensive error tracking
- **Performance Tracking**: Real-time performance metrics

## 🎛️ Command Line Options

### PowerShell Script Options

```powershell

.\auto-run-system.ps1 [options]

Options:
  - AutoStart        Automatically open dashboard in browser
  - MonitorOnly      Only monitor existing server (don't start)
  - ForceRestart     Force restart existing server
  - Silent           Run with minimal output
  - Port <number>    Use custom port (default: 3001)

```

### Examples

```powershell

## Basic auto-run with dashboard

.\auto-run-system.ps1 -AutoStart

## Force restart everything

.\auto-run-system.ps1 -AutoStart -ForceRestart

## Monitor existing server only

.\auto-run-system.ps1 -MonitorOnly

## Run on port 3002

.\auto-run-system.ps1 -AutoStart -Port 3002

## Silent mode

.\auto-run-system.ps1 -AutoStart -Silent

```

## 🔄 Auto-Recovery System

### How It Works

1. **Health Check**: Every 10 seconds
2. **Failure Detection**: If health check fails
3. **Auto-Restart**: Automatically restarts server
4. **Retry Limit**: Maximum 5 restart attempts
5. **Status Reporting**: Real-time status updates

### Recovery Scenarios

- **Server Crash**: Automatic restart
- **Port Conflict**: Automatic port freeing
- **Dependency Issues**: Automatic npm install
- **Process Death**: Automatic process restart
- **Health Failure**: Automatic server restart

## 📈 Real-time Monitoring

### System Status Display

```

===============================================
           SYSTEM STATUS
===============================================

🟢 Server Status: RUNNING
⏱️  Uptime: 01:23:45
🔄 Restarts: 0
🌐 URL: http://localhost:3001
🔌 WebSocket: ws://localhost:3001

✅ Health Check: PASSED

📊 SYSTEM METRICS
CPU Usage: 45%
Memory Usage: 65%
Network: 12.5 MB/s
Storage: 75%

🤖 AI AGENTS
Main Agent: active
Data Processing Agent: active
Analytics Agent: active
Security Agent: active
Recovery Agent: active
===============================================

```

### Monitoring Intervals

- **Health Check**: Every 10 seconds
- **Status Display**: Every 30 seconds
- **Metrics Update**: Every 5 seconds
- **Agent Status**: Every 10 seconds

## 🛠️ Troubleshooting

### Common Issues

#### 1. PowerShell Execution Policy

```powershell

## Fix execution policy

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

#### 2. Port Already in Use

```powershell

## The script automatically handles this, but you can manually

netstat -ano | findstr :3001
taskkill /PID <PID> /F

```

#### 3. Node.js Not Found

```bash

## Install Node.js from https://nodejs.org/


## Then run the script again

```

#### 4. Dependencies Not Installed

```bash

## The script automatically runs npm install


## If it fails, manually run

npm install

```

#### 5. Server Won't Start

```powershell

## Check logs

Get-Content logs\server.log

## Force restart

.\auto-run-system.ps1 -ForceRestart

```

### Debug Mode

```powershell

## Run with verbose output

.\auto-run-system.ps1 -AutoStart -Verbose

```

## 🔧 Advanced Configuration

### Custom Configuration

Create `config/auto-run.json`:

```json

{
  "port": 3001,
  "maxRestarts": 5,
  "healthCheckInterval": 10,
  "statusDisplayInterval": 30,
  "autoOpenDashboard": true,
  "forceRestart": false,
  "monitorOnly": false
}

```

### Environment Variables

```bash

## Set custom environment variables

set PORT=3001
set NODE_ENV=development
set AUTO_START=true

```

## 📱 Integration with Other Tools

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., at startup)
4. Action: Start a program
5. Program: `powershell.exe`
6. Arguments: `-ExecutionPolicy Bypass -File "auto-run-system.ps1" -AutoStart`

### Windows Startup

1. Press `Win + R`
2. Type `shell:startup`
3. Create shortcut to `auto-run.bat`

### System Service (Advanced)

```powershell

## Create Windows service (requires admin)

sc create "EHB5IntelligentSystem" binPath="powershell.exe -ExecutionPolicy Bypass -File auto-run-system.ps1 -AutoStart"
sc start "EHB5IntelligentSystem"

```

## 🔒 Security Considerations

### Safe Execution

- Script runs with current user privileges
- No admin rights required for basic operation
- All operations are logged
- Graceful error handling

### Network Security

- Server runs on localhost only by default
- WebSocket connections are local
- No external network access by default
- Firewall-friendly configuration

## 📊 Performance Monitoring

### Resource Usage

- **CPU**: Typically 5-15% during normal operation
- **Memory**: Approximately 50-100MB
- **Network**: Minimal (local connections only)
- **Disk**: Log files and temporary data

### Optimization Tips

- Close unnecessary browser tabs
- Monitor system resources
- Restart periodically for long-running sessions
- Use SSD for better performance

## 🚀 Production Deployment

### For Production Use

```powershell

## Production mode

$env:NODE_ENV = "production"
.\auto-run-system.ps1 -AutoStart -Port 3001

```

### Load Balancing

- Run multiple instances on different ports
- Use reverse proxy (nginx, Apache)
- Monitor all instances

### High Availability

- Use Windows clustering
- Implement failover mechanisms
- Monitor system health

## 📞 Support

### Getting Help

1. **Check Logs**: `logs\server.log`
2. **Health Check**: `http://localhost:3001/health`
3. **CLI Status**: `node cli.js status`
4. **System Monitor**: `node cli.js monitor`

### Common Commands

```bash

## Check system status

node cli.js status

## View logs

node cli.js logs

## Monitor in real-time

node cli.js monitor

## Health check

node cli.js health

## Restart server

node cli.js stop
node cli.js start

```

## 🎯 Best Practices

### Daily Usage

1. **Start**: Run `auto-run.bat` or `auto-run-system.ps1 -AutoStart`
2. **Monitor**: Watch the status display
3. **Use**: Access dashboard at `http://localhost:3001`
4. **Stop**: Press `Ctrl+C` to stop gracefully

### Maintenance

1. **Weekly**: Check logs for errors
2. **Monthly**: Update dependencies
3. **Quarterly**: Review configuration
4. **Annually**: Full system audit

### Backup

1. **Configuration**: Backup `config/` folder
2. **Data**: Backup `data/` folder
3. **Logs**: Archive `logs/` folder
4. **Scripts**: Keep all automation scripts

- --

## 🎉 Quick Reference

### One-Click Start

```bash

## Double-click this file

auto-run.bat

```

### Command Line Start

```powershell

## Basic auto-run

.\auto-run-system.ps1 -AutoStart

## Force restart (2)

.\auto-run-system.ps1 -AutoStart -ForceRestart

## Monitor only

.\auto-run-system.ps1 -MonitorOnly

```

### Stop System

```bash

## Press Ctrl+C in the terminal


## Or close the terminal window

```

### Access Dashboard

```

http://localhost:3001

```

- --

* *🚀 Your EHB-5 Intelligent System is now ready for automatic operation!**

* The system will start, monitor, and manage itself automatically with full auto-recovery capabilities.*
