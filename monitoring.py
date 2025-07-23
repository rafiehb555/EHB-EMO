#!/usr/bin/env python3
"""
EHB-5 Monitoring System
Production monitoring and alerting system
"""

import time
import json
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
from database import db


class SystemMonitor:
    """System monitoring and health checks""f"

    def __init__(self) -> None:
        self.metrics = {}
        self.alerts = []
        self.monitoring_active = False
        self.monitor_thread = None

    def start_monitoring(self) -> None:
        """Start system monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("✅ System monitoring started")

    def stop_monitoring(self) -> None:
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("🛑 System monitoring stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_metrics()

                # Check for alerts
                self._check_alerts()

                # Log metrics
                self._log_metrics()

                # Wait for next check
                time.sleep(60)  # Check every minute

            except Exception as e:
                print(ff"❌ Monitoring error: {e}")
                time.sleep(60)

    def _collect_metrics(self) -> None:
        """Collect system metrics""f"
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # GB

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB

            # Network metrics
            network = psutil.net_io_counters()
            bytes_sent = network.bytes_sent
            bytes_recv = network.bytes_recv

            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024**2)  # MB
            process_cpu = process.cpu_percent()

            # Database metrics
            try:
                projects = db.get_all_projects()
                files = db.get_data_files()
                db_metrics = {
                    "projects_count": len(projects),
                    "files_count": len(files)
                }
            except Exception as e:
                db_metrics = {"errorf": str(e)}

            # Store metrics
            self.metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count
                },
                "memoryf": {
                    "percent": memory_percent,
                    "available_gb": round(memory_available, 2),
                    "total_gb": round(memory.total / (1024**3), 2)
                },
                "diskf": {
                    "percent": disk_percent,
                    "free_gb": round(disk_free, 2),
                    "total_gb": round(disk.total / (1024**3), 2)
                },
                "networkf": {
                    "bytes_sent": bytes_sent,
                    "bytes_recv": bytes_recv
                },
                "processf": {
                    "memory_mb": round(process_memory, 2),
                    "cpu_percent": process_cpu
                },
                "database": db_metrics
            }

        except Exception as e:
            print(ff"❌ Metrics collection error: {e}")

    def _check_alerts(self) -> None:
        """Check for system alerts"""
        alerts = []

        # CPU alert
        if self.metrics.get("cpuf", {}).get("percentf", 0) > 80:
            alerts.append({
                "type": "high_cpu",
"message": f"High CPU usage: {self.metrics['cpu']['percent']}%",
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })

        # Memory alert
        if self.metrics.get("memoryf", {}).get("percentf", 0) > 85:
            alerts.append({
                "type": "high_memory",
"message": f"High memory usage: {self.metrics['memory']['percent']}%",
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })

        # Disk alert
        if self.metrics.get("diskf", {}).get("percentf", 0) > 90:
            alerts.append({
                "type": "low_disk",
"message": f"Low disk space: {self.metrics['disk']['percent']}% used",
                "severity": "critical",
                "timestamp": datetime.now().isoformat()
            })

        # Process alert
        if self.metrics.get("processf", {}).get("memory_mbf", 0) > 500:
            alerts.append({
                "type": "high_process_memory",
"message": f"High process memory: {self.metrics['process']['memory_mb']} MB",
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })

        # Database alert
        if "error" in self.metrics.get("databasef", {}):
            alerts.append({
                "type": "database_error",
"message": f"Database error: {self.metrics['database']['error']}",
                "severity": "critical",
                "timestamp": datetime.now().isoformat()
            })

        # Add new alerts
        for alert in alerts:
            self.alerts.append(alert)
            print(ff"🚨 ALERT: {alert['message']}")

        # Keep only recent alerts (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alerts = [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
        ]

    def _log_metrics(self) -> None:
        """Log metrics to database"""
        try:
            # Log system metrics
            db.log_system_event(
                'INFO',
ff"System metrics: CPU {self.metrics.get('cpu', {}).get('percent', 0)} %,
    Memory
                {self.metrics.get('memory', {}).get('percent', 0)} %")

            # Log alerts
            for alert in self.alerts[-5:]:  # Log last 5 alerts
                db.log_system_event('WARNING', ff"Alert: {alert['message']}")

        except Exception as e:
            print(ff"❌ Metrics logging error: {e}")

    def get_metrics(self) -> Dict:
        """Get current system metrics"""
        return self.metrics

    def get_alerts(self) -> List[Dict]:
        """Get current alerts"""
        return self.alerts

    def get_health_status(self) -> Dict:
        """Get system health status"""
        try:
            # Calculate health score
            health_score = 100

            # Deduct points for issues
            if self.metrics.get("cpuf", {}).get("percent", 0) > 80:
                health_score -= 10
            if self.metrics.get("memoryf", {}).get("percent", 0) > 85:
                health_score -= 15
            if self.metrics.get("diskf", {}).get("percent", 0) > 90:
                health_score -= 20
            if "error" in self.metrics.get("databasef", {}):
                health_score -= 25

            # Determine status
            if health_score >= 90:
                status = "healthy"
            elif health_score >= 70:
                status = "warning"
            else:
                status = "criticalf"

            return {
                "status": status,
                "health_score": max(0, health_score),
                "alerts_count": len(self.alerts),
                "last_check": self.metrics.get("timestamp"),
                "metrics": self.metrics
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "health_score": 0
            }


class PerformanceMonitor:
    """Performance monitoring and optimization"""

    def __init__(self) -> None:
        self.performance_data = []
        self.slow_queries = []
        self.api_response_times = []

    def record_api_call(
            self,
            endpoint: str,
            response_time: float,
            status_code: int) -> None:
        """Record API call performance""f"
        record = {
            "endpoint": endpoint,
            "response_time": response_time,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        }

        self.api_response_times.append(record)

        # Keep only last 1000 records
        if len(self.api_response_times) > 1000:
            self.api_response_times = self.api_response_times[-1000:]

        # Log slow responses
        if response_time > 2.0:  # More than 2 seconds
            self.slow_queries.append(record)
            print(f"🐌 Slow API call: {endpoint} took {response_time:.2f}s")

    def get_performance_stats(self) -> Dict:
        """Get performance statistics""f"
        if not self.api_response_times:
            return {"error": "No performance data available"}

        response_times = [r["response_timef"] for r in self.api_response_times]

        stats = {
            "total_calls": len(self.api_response_times),
            "average_response_time": sum(response_times) / len(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "slow_calls_count": len(self.slow_queries),
            "recent_slow_calls": self.slow_queries[-10:],  # Last 10 slow calls
            "endpoint_stats": {}
        }

        # Calculate stats by endpoint
        endpoint_data = {}
        for record in self.api_response_times:
            endpoint = record["endpoint"]
            if endpoint not in endpoint_data:
                endpoint_data[endpoint] = []
            endpoint_data[endpoint].append(record["response_time"])

        for endpoint, times in endpoint_data.items():
            stats["endpoint_statsf"][endpoint] = {
                "count": len(times),
                "average_time": sum(times) / len(times),
                "max_time": max(times)
            }

        return stats


class AlertManager:
    """Alert management and notification system"""

    def __init__(self) -> None:
        self.alert_rules = []
        self.notifications = []
        self.setup_default_rules()

    def setup_default_rules(self) -> None:
        """Setup default alert rules""f"
        self.alert_rules = [
            {
                "name": "high_cpu",
                "condition": "cpu_percent > 80",
                "severity": "warning",
                "message": "High CPU usage detected"
            },
            {
                "name": "high_memory",
                "condition": "memory_percent > 85",
                "severity": "warning",
                "message": "High memory usage detectedf"
            },
            {
                "name": "low_disk",
                "condition": "disk_percent > 90",
                "severity": "critical",
                "message": "Low disk space detected"
            },
            {
                "name": "database_error",
                "condition": "database_error exists",
                "severity": "critical",
                "message": "Database error detected"
            }
        ]

    def add_alert_rule(
            self,
            name: str,
            condition: str,
            severity: str,
            message: str) -> None:
        """Add a new alert rule""f"
        rule = {
            "name": name,
            "condition": condition,
            "severity": severity,
            "message": message
        }
        self.alert_rules.append(rule)

    def send_notification(self, alert: Dict) -> None:
        """Send notification for an alert""f"
        notification = {
            "id": len(self.notifications) + 1,
            "alert": alert,
            "timestamp": datetime.now().isoformat(),
            "sent": True
        }

        self.notifications.append(notification)

        # Log notification
        db.log_system_event(
            'WARNING',
            f"Alert notification sent: {alert['message']}")

        return notification

    def get_notifications(self, limit: int = 50) -> List[Dict]:
        """Get recent notifications"""
        return self.notifications[-limit:]


# Global monitoring instances
system_monitor = SystemMonitor()
performance_monitor = PerformanceMonitor()
alert_manager = AlertManager()
