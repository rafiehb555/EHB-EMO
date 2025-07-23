# EHB-5 Intelligent System Auto-Runner
# This script automatically starts, monitors, and manages the entire intelligent system

param(
    [switch]$AutoStart,
    [switch]$MonitorOnly,
    [switch]$ForceRestart,
    [switch]$Silent,
    [int]$Port = 3001
)

# Set console colors
$Host.UI.RawUI.ForegroundColor = "Cyan"
Write-Host "🚀 EHB-5 Intelligent System Auto-Runner" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Global variables
$script:ServerProcess = $null
$script:IsRunning = $false
$script:StartTime = Get-Date
$script:RestartCount = 0
$script:MaxRestarts = 5
$script:HealthCheckInterval = 30
$script:LastHealthCheck = Get-Date

# Function to display status with colors
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )

    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] ✓ $Message" -ForegroundColor Green }
        "Error" { Write-Host "[$timestamp] ✗ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[$timestamp] ⚠ $Message" -ForegroundColor Yellow }
        "Info" { Write-Host "[$timestamp] ℹ $Message" -ForegroundColor Cyan }
        "System" { Write-Host "[$timestamp] 🔧 $Message" -ForegroundColor Blue }
    }
}

# Function to check if Node.js is installed
function Test-NodeJS {
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Status "Node.js found: $nodeVersion" "Success"
            return $true
        }
    }
    catch {
        Write-Status "Node.js not found" "Error"
        return $false
    }
    return $false
}

# Function to check if npm is installed
function Test-NPM {
    try {
        $npmVersion = npm --version 2>$null
        if ($npmVersion) {
            Write-Status "npm found: $npmVersion" "Success"
            return $true
        }
    }
    catch {
        Write-Status "npm not found" "Error"
        return $false
    }
    return $false
}

# Function to check if required files exist
function Test-RequiredFiles {
    $requiredFiles = @(
        "package.json",
        "intelligent-api-server.js",
        "intelligent-dashboard.html",
        "cli.js"
    )

    $missingFiles = @()
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }

    if ($missingFiles.Count -gt 0) {
        Write-Status "Missing required files: $($missingFiles -join ', ')" "Error"
        return $false
    }

    Write-Status "All required files found" "Success"
    return $true
}

# Function to install dependencies
function Install-Dependencies {
    Write-Status "Checking dependencies..." "Info"

    if (-not (Test-Path "node_modules")) {
        Write-Status "Installing dependencies..." "Info"
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Dependencies installed successfully" "Success"
        }
        else {
            Write-Status "Failed to install dependencies" "Error"
            return $false
        }
    }
    else {
        Write-Status "Dependencies already installed" "Success"
    }

    return $true
}

# Function to create necessary directories
function Create-Directories {
    $directories = @("logs", "config", "backups", "data", "public", "test")

    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Status "Created directory: $dir" "Success"
        }
    }
}

# Function to check if port is available
function Test-Port {
    param([int]$Port)

    try {
        $connection = Test-NetConnection -ComputerName "localhost" -Port $Port -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Status "Port $Port is in use" "Warning"
            return $false
        }
    }
    catch {
        # Port is available
    }

    Write-Status "Port $Port is available" "Success"
    return $true
}

# Function to kill processes on port
function Stop-PortProcesses {
    param([int]$Port)

    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq "Listen" }

        foreach ($process in $processes) {
            $processInfo = Get-Process -Id $process.OwningProcess -ErrorAction SilentlyContinue
            if ($processInfo) {
                Write-Status "Stopping process: $($processInfo.ProcessName) (PID: $($processInfo.Id))" "Warning"
                Stop-Process -Id $processInfo.Id -Force
            }
        }

        Start-Sleep -Seconds 2
        return $true
    }
    catch {
        Write-Status "Failed to stop processes on port $Port" "Error"
        return $false
    }
}

# Function to start the server
function Start-IntelligentServer {
    Write-Status "Starting Intelligent API Server..." "Info"

    # Set environment variables
    $env:PORT = $Port
    $env:NODE_ENV = "development"

    # Start the server process
    $script:ServerProcess = Start-Process -FilePath "node" -ArgumentList "intelligent-api-server.js" -PassThru -WindowStyle Hidden

    if ($script:ServerProcess) {
        $script:IsRunning = $true
        $script:StartTime = Get-Date
        Write-Status "Server process started (PID: $($script:ServerProcess.Id))" "Success"
        return $true
    }
    else {
        Write-Status "Failed to start server process" "Error"
        return $false
    }
}

# Function to check server health
function Test-ServerHealth {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$Port/health" -Method Get -TimeoutSec 5
        if ($response.status -eq "healthy") {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to get server metrics
function Get-ServerMetrics {
    try {
        $metrics = Invoke-RestMethod -Uri "http://localhost:$Port/api/v1/metrics" -Method Get -TimeoutSec 5
        return $metrics
    }
    catch {
        return $null
    }
}

# Function to get AI agents status
function Get-AgentsStatus {
    try {
        $agents = Invoke-RestMethod -Uri "http://localhost:$Port/api/v1/agents" -Method Get -TimeoutSec 5
        return $agents
    }
    catch {
        return @()
    }
}

# Function to display system status
function Show-SystemStatus {
    $uptime = (Get-Date) - $script:StartTime
    $uptimeString = "{0:D2}:{1:D2}:{2:D2}" -f $uptime.Hours, $uptime.Minutes, $uptime.Seconds

    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host "           SYSTEM STATUS" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host ""

    # Server status
    if ($script:IsRunning) {
        Write-Host "🟢 Server Status: RUNNING" -ForegroundColor Green
        Write-Host "⏱️  Uptime: $uptimeString" -ForegroundColor Cyan
        Write-Host "🔄 Restarts: $($script:RestartCount)" -ForegroundColor Yellow
        Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor Cyan
        Write-Host "🔌 WebSocket: ws://localhost:$Port" -ForegroundColor Cyan
    }
    else {
        Write-Host "🔴 Server Status: STOPPED" -ForegroundColor Red
    }

    # Health check
    if (Test-ServerHealth) {
        Write-Host "✅ Health Check: PASSED" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Health Check: FAILED" -ForegroundColor Red
    }

    # Metrics
    $metrics = Get-ServerMetrics
    if ($metrics) {
        Write-Host ""
        Write-Host "📊 SYSTEM METRICS" -ForegroundColor Blue
        Write-Host "CPU Usage: $($metrics.cpu)%" -ForegroundColor White
        Write-Host "Memory Usage: $($metrics.memory)%" -ForegroundColor White
        Write-Host "Network: $($metrics.network) MB/s" -ForegroundColor White
        Write-Host "Storage: $($metrics.storage)%" -ForegroundColor White
    }

    # AI Agents
    $agents = Get-AgentsStatus
    if ($agents.Count -gt 0) {
        Write-Host ""
        Write-Host "🤖 AI AGENTS" -ForegroundColor Blue
        foreach ($agent in $agents) {
            $statusColor = if ($agent.status -eq "active") { "Green" } else { "Red" }
            Write-Host "$($agent.name): $($agent.status)" -ForegroundColor $statusColor
        }
    }

    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Green
}

# Function to monitor the system
function Start-SystemMonitor {
    Write-Status "Starting system monitor..." "Info"

    while ($true) {
        try {
            # Check if server process is still running
            if ($script:ServerProcess -and -not $script:ServerProcess.HasExited) {
                # Check server health
                if (Test-ServerHealth) {
                    $script:LastHealthCheck = Get-Date
                }
                else {
                    Write-Status "Server health check failed" "Warning"

                    # Auto-restart if health check fails
                    if ($script:RestartCount -lt $script:MaxRestarts) {
                        Write-Status "Auto-restarting server..." "Warning"
                        Stop-IntelligentServer
                        Start-Sleep -Seconds 5
                        Start-IntelligentServer
                        $script:RestartCount++
                    }
                    else {
                        Write-Status "Maximum restart attempts reached" "Error"
                        break
                    }
                }
            }
            else {
                Write-Status "Server process has stopped" "Error"

                if ($script:RestartCount -lt $script:MaxRestarts) {
                    Write-Status "Restarting server..." "Warning"
                    Start-IntelligentServer
                    $script:RestartCount++
                }
                else {
                    Write-Status "Maximum restart attempts reached" "Error"
                    break
                }
            }

            # Display status every 30 seconds
            $timeSinceLastCheck = (Get-Date) - $script:LastHealthCheck
            if ($timeSinceLastCheck.TotalSeconds -ge $script:HealthCheckInterval) {
                Show-SystemStatus
                $script:LastHealthCheck = Get-Date
            }

            Start-Sleep -Seconds 10

        }
        catch {
            Write-Status "Monitor error: $($_.Exception.Message)" "Error"
            Start-Sleep -Seconds 5
        }
    }
}

# Function to stop the server
function Stop-IntelligentServer {
    if ($script:ServerProcess -and -not $script:ServerProcess.HasExited) {
        Write-Status "Stopping server process..." "Info"
        Stop-Process -Id $script:ServerProcess.Id -Force
        $script:IsRunning = $false
        Write-Status "Server stopped" "Success"
    }
}

# Function to open dashboard in browser
function Open-Dashboard {
    Write-Status "Opening dashboard in browser..." "Info"
    Start-Process "http://localhost:$Port"
    Write-Status "Dashboard opened" "Success"
}

# Function to handle cleanup
function Cleanup {
    Write-Status "Cleaning up..." "Info"
    Stop-IntelligentServer
    Stop-PortProcesses -Port $Port
    Write-Status "Cleanup complete" "Success"
}

# Main execution
try {
    # Check prerequisites
    Write-Status "Checking prerequisites..." "Info"

    if (-not (Test-NodeJS)) {
        Write-Status "Please install Node.js from https://nodejs.org/" "Error"
        exit 1
    }

    if (-not (Test-NPM)) {
        Write-Status "Please install npm" "Error"
        exit 1
    }

    if (-not (Test-RequiredFiles)) {
        Write-Status "Please run this script from the project root directory" "Error"
        exit 1
    }

    # Install dependencies
    if (-not (Install-Dependencies)) {
        Write-Status "Failed to install dependencies" "Error"
        exit 1
    }

    # Create directories
    Create-Directories

    # Check port availability
    if (-not (Test-Port -Port $Port)) {
        Write-Status "Attempting to free port $Port..." "Warning"
        Stop-PortProcesses -Port $Port
        Start-Sleep -Seconds 2

        if (-not (Test-Port -Port $Port)) {
            Write-Status "Could not free port $Port" "Error"
            exit 1
        }
    }

    # Start server if not in monitor only mode
    if (-not $MonitorOnly) {
        if ($ForceRestart) {
            Write-Status "Force restart requested..." "Warning"
            Stop-IntelligentServer
            Stop-PortProcesses -Port $Port
            Start-Sleep -Seconds 3
        }

        if (Start-IntelligentServer) {
            Write-Status "Waiting for server to start..." "Info"

            # Wait for server to start
            $attempts = 0
            $maxAttempts = 30

            while ($attempts -lt $maxAttempts) {
                if (Test-ServerHealth) {
                    Write-Status "Server is healthy and responding" "Success"
                    break
                }

                $attempts++
                Start-Sleep -Seconds 2
            }

            if ($attempts -ge $maxAttempts) {
                Write-Status "Server failed to start within expected time" "Error"
                exit 1
            }

            # Show initial status
            Show-SystemStatus

            # Open dashboard if auto-start is enabled
            if ($AutoStart) {
                Open-Dashboard
            }

            # Start monitoring
            Start-SystemMonitor
        }
        else {
            Write-Status "Failed to start server" "Error"
            exit 1
        }
    }
    else {
        # Monitor only mode
        Write-Status "Monitor only mode - checking existing server..." "Info"

        if (Test-ServerHealth) {
            Write-Status "Server is running and healthy" "Success"
            Show-SystemStatus
            Start-SystemMonitor
        }
        else {
            Write-Status "No healthy server found on port $Port" "Error"
            exit 1
        }
    }

}
catch {
    Write-Status "Unexpected error: $($_.Exception.Message)" "Error"
    exit 1
}
finally {
    # Cleanup on exit
    Cleanup
}

# Handle Ctrl+C gracefully
$null = Register-EngineEvent PowerShell.Exiting -Action {
    Write-Status "Shutting down..." "Info"
    Cleanup
}
