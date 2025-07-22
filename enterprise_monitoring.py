#!/usr/bin/env python3
"""
EHB-5 Enterprise Monitoring System
Advanced enterprise monitoring and analytics
"""

import time
import json
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
from database import db

class EnterpriseMonitor:
    """Enterprise-grade monitoring system"""
    
    def __init__(self):
        self.metrics_history = deque(maxlen=10000)
        self.alerts = deque(maxlen=1000)
        self.performance_data = deque(maxlen=5000)
        self.security_events = deque(maxlen=2000)
        self.monitoring_active = False
        self.monitor_thread = None
        self.alert_rules = self._setup_alert_rules()
        self.metrics_config = {
            "collection_interval": 30,  # seconds
            "retention_days": 30,
            "alert_thresholds": {
                "cpu_high": 80,
                "memory_high": 85,
                "disk_high": 90,
                "response_time_slow": 2.0,
                "error_rate_high": 5.0
            }
        }
    
    def _setup_alert_rules(self) -> Dict[str, Any]:
        """Setup enterprise alert rules"""
        return {
            "system_alerts": {
                "high_cpu": {
                    "condition": "cpu_percent > 80",
                    "severity": "warning",
                    "message": "High CPU usage detected",
                    "action": "notify_admin"
                },
                "high_memory": {
                    "condition": "memory_percent > 85",
                    "severity": "warning",
                    "message": "High memory usage detected",
                    "action": "notify_admin"
                },
                "low_disk": {
                    "condition": "disk_percent > 90",
                    "severity": "critical",
                    "message": "Low disk space detected",
                    "action": "notify_admin"
                },
                "high_error_rate": {
                    "condition": "error_rate > 5.0",
                    "severity": "critical",
                    "message": "High error rate detected",
                    "action": "notify_admin"
                }
            },
            "security_alerts": {
                "failed_login": {
                    "condition": "failed_logins > 5",
                    "severity": "warning",
                    "message": "Multiple failed login attempts",
                    "action": "block_ip"
                },
                "suspicious_activity": {
                    "condition": "suspicious_events > 3",
                    "severity": "critical",
                    "message": "Suspicious activity detected",
                    "action": "notify_security"
                }
            },
            "performance_alerts": {
                "slow_response": {
                    "condition": "response_time > 2.0",
                    "severity": "warning",
                    "message": "Slow response time detected",
                    "action": "optimize"
                },
                "high_latency": {
                    "condition": "latency > 1000",
                    "severity": "critical",
                    "message": "High latency detected",
                    "action": "investigate"
                }
            }
        }
    
    def start_monitoring(self):
        """Start enterprise monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("✅ Enterprise monitoring started")
    
    def stop_monitoring(self):
        """Stop enterprise monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("🛑 Enterprise monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect comprehensive metrics
                metrics = self._collect_enterprise_metrics()
                
                # Store metrics
                self.metrics_history.append(metrics)
                
                # Check alerts
                self._check_enterprise_alerts(metrics)
                
                # Log metrics
                self._log_metrics(metrics)
                
                # Wait for next collection
                time.sleep(self.metrics_config["collection_interval"])
                
            except Exception as e:
                print(f"❌ Enterprise monitoring error: {e}")
                time.sleep(self.metrics_config["collection_interval"])
    
    def _collect_enterprise_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive enterprise metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # GB
            memory_used = memory.used / (1024**3)  # GB
            
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            disk_used = disk.used / (1024**3)  # GB
            
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
                    "files_count": len(files),
                    "db_size_mb": self._get_db_size()
                }
            except Exception as e:
                db_metrics = {"error": str(e)}
            
            # Performance metrics
            performance_metrics = self._get_performance_metrics()
            
            # Security metrics
            security_metrics = self._get_security_metrics()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu": {
                        "percent": cpu_percent,
                        "count": cpu_count,
                        "frequency_mhz": cpu_freq.current if cpu_freq else None
                    },
                    "memory": {
                        "percent": memory_percent,
                        "available_gb": round(memory_available, 2),
                        "used_gb": round(memory_used, 2),
                        "total_gb": round(memory.total / (1024**3), 2)
                    },
                    "disk": {
                        "percent": disk_percent,
                        "free_gb": round(disk_free, 2),
                        "used_gb": round(disk_used, 2),
                        "total_gb": round(disk.total / (1024**3), 2)
                    },
                    "network": {
                        "bytes_sent": bytes_sent,
                        "bytes_recv": bytes_recv,
                        "packets_sent": network.packets_sent,
                        "packets_recv": network.packets_recv
                    },
                    "process": {
                        "memory_mb": round(process_memory, 2),
                        "cpu_percent": process_cpu,
                        "threads": process.num_threads(),
                        "open_files": len(process.open_files())
                    }
                },
                "database": db_metrics,
                "performance": performance_metrics,
                "security": security_metrics,
                "uptime": self._get_uptime()
            }
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _get_db_size(self) -> float:
        """Get database size in MB"""
        try:
            import os
            db_path = "ehb5.db"
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                return round(size_bytes / (1024 * 1024), 2)
            return 0.0
        except Exception:
            return 0.0
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            # This would integrate with your performance monitoring
            return {
                "response_time_avg": 0.5,
                "response_time_max": 2.1,
                "requests_per_second": 10.5,
                "error_rate": 0.1,
                "active_connections": 5
            }
        except Exception:
            return {"error": "Performance metrics unavailable"}
    
    def _get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics"""
        try:
            # This would integrate with your security monitoring
            return {
                "failed_logins": 2,
                "blocked_ips": 1,
                "suspicious_events": 0,
                "active_sessions": 3,
                "security_score": 85
            }
        except Exception:
            return {"error": "Security metrics unavailable"}
    
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        except Exception:
            return "Unknown"
    
    def _check_enterprise_alerts(self, metrics: Dict[str, Any]):
        """Check for enterprise alerts"""
        alerts = []
        
        # System alerts
        if metrics.get("system", {}).get("cpu", {}).get("percent", 0) > self.metrics_config["alert_thresholds"]["cpu_high"]:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"High CPU usage: {metrics['system']['cpu']['percent']}%",
                "timestamp": datetime.now().isoformat(),
                "category": "system"
            })
        
        if metrics.get("system", {}).get("memory", {}).get("percent", 0) > self.metrics_config["alert_thresholds"]["memory_high"]:
            alerts.append({
                "type": "high_memory",
                "severity": "warning",
                "message": f"High memory usage: {metrics['system']['memory']['percent']}%",
                "timestamp": datetime.now().isoformat(),
                "category": "system"
            })
        
        if metrics.get("system", {}).get("disk", {}).get("percent", 0) > self.metrics_config["alert_thresholds"]["disk_high"]:
            alerts.append({
                "type": "low_disk",
                "severity": "critical",
                "message": f"Low disk space: {metrics['system']['disk']['percent']}% used",
                "timestamp": datetime.now().isoformat(),
                "category": "system"
            })
        
        # Performance alerts
        if metrics.get("performance", {}).get("response_time_avg", 0) > self.metrics_config["alert_thresholds"]["response_time_slow"]:
            alerts.append({
                "type": "slow_response",
                "severity": "warning",
                "message": f"Slow response time: {metrics['performance']['response_time_avg']}s",
                "timestamp": datetime.now().isoformat(),
                "category": "performance"
            })
        
        # Security alerts
        if metrics.get("security", {}).get("failed_logins", 0) > 5:
            alerts.append({
                "type": "failed_logins",
                "severity": "warning",
                "message": f"Multiple failed logins: {metrics['security']['failed_logins']}",
                "timestamp": datetime.now().isoformat(),
                "category": "security"
            })
        
        # Add alerts to history
        for alert in alerts:
            self.alerts.append(alert)
            print(f"🚨 ENTERPRISE ALERT: {alert['message']}")
    
    def _log_metrics(self, metrics: Dict[str, Any]):
        """Log metrics to database"""
        try:
            # Log system metrics
            db.log_system_event('INFO', f"Enterprise metrics: CPU {metrics.get('system', {}).get('cpu', {}).get('percent', 0)}%, Memory {metrics.get('system', {}).get('memory', {}).get('percent', 0)}%")
            
            # Log alerts
            for alert in list(self.alerts)[-5:]:  # Log last 5 alerts
                db.log_system_event('WARNING', f"Enterprise Alert: {alert['message']}")
                
        except Exception as e:
            print(f"❌ Enterprise metrics logging error: {e}")
    
    def get_enterprise_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        try:
            # Get recent metrics
            recent_metrics = list(self.metrics_history)[-100:] if self.metrics_history else []
            
            # Calculate averages
            if recent_metrics:
                cpu_values = [m.get("system", {}).get("cpu", {}).get("percent", 0) for m in recent_metrics]
                memory_values = [m.get("system", {}).get("memory", {}).get("percent", 0) for m in recent_metrics]
                disk_values = [m.get("system", {}).get("disk", {}).get("percent", 0) for m in recent_metrics]
                
                avg_cpu = sum(cpu_values) / len(cpu_values)
                avg_memory = sum(memory_values) / len(memory_values)
                avg_disk = sum(disk_values) / len(disk_values)
            else:
                avg_cpu = avg_memory = avg_disk = 0
            
            # Get current metrics
            current_metrics = recent_metrics[-1] if recent_metrics else {}
            
            # Get alerts summary
            recent_alerts = list(self.alerts)[-50:] if self.alerts else []
            alert_summary = {
                "total_alerts": len(recent_alerts),
                "critical_alerts": len([a for a in recent_alerts if a.get("severity") == "critical"]),
                "warning_alerts": len([a for a in recent_alerts if a.get("severity") == "warning"]),
                "system_alerts": len([a for a in recent_alerts if a.get("category") == "system"]),
                "security_alerts": len([a for a in recent_alerts if a.get("category") == "security"]),
                "performance_alerts": len([a for a in recent_alerts if a.get("category") == "performance"])
            }
            
            return {
                "current_metrics": current_metrics,
                "averages": {
                    "cpu_percent": round(avg_cpu, 2),
                    "memory_percent": round(avg_memory, 2),
                    "disk_percent": round(avg_disk, 2)
                },
                "alert_summary": alert_summary,
                "recent_alerts": recent_alerts[-10:],  # Last 10 alerts
                "system_health": self._calculate_system_health(current_metrics),
                "monitoring_status": {
                    "active": self.monitoring_active,
                    "collection_interval": self.metrics_config["collection_interval"],
                    "metrics_count": len(self.metrics_history)
                }
            }
            
        except Exception as e:
            return {
                "error": f"Dashboard data error: {str(e)}",
                "monitoring_status": {
                    "active": self.monitoring_active,
                    "error": True
                }
            }
    
    def _calculate_system_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall system health score"""
        try:
            health_score = 100
            
            # Deduct for issues
            if metrics.get("system", {}).get("cpu", {}).get("percent", 0) > 80:
                health_score -= 10
            if metrics.get("system", {}).get("memory", {}).get("percent", 0) > 85:
                health_score -= 15
            if metrics.get("system", {}).get("disk", {}).get("percent", 0) > 90:
                health_score -= 20
            if "error" in metrics.get("database", {}):
                health_score -= 25
            
            # Determine status
            if health_score >= 90:
                status = "excellent"
            elif health_score >= 70:
                status = "good"
            elif health_score >= 50:
                status = "fair"
            else:
                status = "poor"
            
            return {
                "score": max(0, health_score),
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "score": 0,
                "status": "error",
                "error": str(e)
            }

# Global enterprise monitoring instance
enterprise_monitor = EnterpriseMonitor() 