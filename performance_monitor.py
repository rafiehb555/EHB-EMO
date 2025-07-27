#!/usr/bin/env python3
"""
EHB Performance Monitor - Real-time performance monitoring and alerting
"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests


class EHBPerformanceMonitor:
    def __init__(self):
        self.monitoring = False
        self.alert_thresholds = {
            "cpu_usage": 80,  # 80%
            "memory_usage": 85,  # 85%
            "disk_usage": 90,  # 90%
            "response_time": 2.0,  # 2 seconds
            "error_rate": 5  # 5%
        }
        
        self.performance_history = []
        self.alerts = []
        self.monitoring_interval = 10  # seconds
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load monitoring configuration"""
        self.config = {
            "endpoints": [
                "http://localhost:3000",
                "http://localhost:8000/health"
            ],
            "monitoring_interval": 10,
            "alert_thresholds": self.alert_thresholds,
            "log_performance": True,
            "send_alerts": True
        }
    
    def start_monitoring(self):
        """Start performance monitoring"""
        print("📊 EHB Performance Monitor Started")
        print("=" * 50)
        print("Monitoring system performance in real-time...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        self.monitoring = True
        
        try:
            while self.monitoring:
                # Collect performance metrics
                metrics = self.collect_metrics()
                
                # Check for alerts
                self.check_alerts(metrics)
                
                # Log performance data
                if self.config["log_performance"]:
                    self.log_performance(metrics)
                
                # Display current status
                self.display_status(metrics)
                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Performance monitoring stopped")
        except Exception as e:
            print(f"❌ Performance monitoring error: {e}")
        finally:
            self.stop_monitoring()
    
    def collect_metrics(self):
        """Collect current performance metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_metrics(),
            "services": self.get_service_metrics(),
            "alerts": []
        }
        
        return metrics
    
    def get_system_metrics(self):
        """Get system performance metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # Network I/O
            network = psutil.net_io_counters()
            
            return {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_usage": disk_usage,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024),
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv
            }
        except Exception as e:
            print(f"❌ Error collecting system metrics: {e}")
            return {}
    
    def get_service_metrics(self):
        """Get service performance metrics"""
        service_metrics = {}
        
        for endpoint in self.config["endpoints"]:
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=5)
                response_time = time.time() - start_time
                
                service_metrics[endpoint] = {
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "content_length": len(response.content),
                    "available": True
                }
                
            except Exception as e:
                service_metrics[endpoint] = {
                    "status_code": None,
                    "response_time": None,
                    "content_length": 0,
                    "available": False,
                    "error": str(e)
                }
        
        return service_metrics
    
    def check_alerts(self, metrics):
        """Check for performance alerts"""
        alerts = []
        
        # System alerts
        system = metrics["system"]
        
        if system.get("cpu_usage", 0) > self.alert_thresholds["cpu_usage"]:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"CPU usage is {system['cpu_usage']:.1f}%",
                "value": system["cpu_usage"],
                "threshold": self.alert_thresholds["cpu_usage"]
            })
        
        if system.get("memory_usage", 0) > self.alert_thresholds["memory_usage"]:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "warning",
                "message": f"Memory usage is {system['memory_usage']:.1f}%",
                "value": system["memory_usage"],
                "threshold": self.alert_thresholds["memory_usage"]
            })
        
        if system.get("disk_usage", 0) > self.alert_thresholds["disk_usage"]:
            alerts.append({
                "type": "high_disk_usage",
                "severity": "critical",
                "message": f"Disk usage is {system['disk_usage']:.1f}%",
                "value": system["disk_usage"],
                "threshold": self.alert_thresholds["disk_usage"]
            })
        
        # Service alerts
        services = metrics["services"]
        
        for endpoint, service_metrics in services.items():
            if not service_metrics.get("available", False):
                alerts.append({
                    "type": "service_unavailable",
                    "severity": "critical",
                    "message": f"Service {endpoint} is unavailable",
                    "endpoint": endpoint
                })
            elif service_metrics.get("response_time", 0) > self.alert_thresholds["response_time"]:
                alerts.append({
                    "type": "slow_response",
                    "severity": "warning",
                    "message": f"Service {endpoint} is slow: {service_metrics['response_time']:.2f}s",
                    "endpoint": endpoint,
                    "response_time": service_metrics["response_time"]
                })
        
        # Store alerts
        if alerts:
            self.alerts.extend(alerts)
            metrics["alerts"] = alerts
            
            # Display alerts
            for alert in alerts:
                self.display_alert(alert)
    
    def display_alert(self, alert):
        """Display a performance alert"""
        severity_icon = {
            "warning": "⚠️",
            "critical": "🚨",
            "info": "ℹ️"
        }
        
        icon = severity_icon.get(alert["severity"], "❓")
        print(f"{icon} {alert['severity'].upper()}: {alert['message']}")
    
    def display_status(self, metrics):
        """Display current performance status"""
        system = metrics["system"]
        services = metrics["services"]
        
        print(f"\n📊 Performance Status - {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)
        
        # System metrics
        print(f"CPU Usage: {system.get('cpu_usage', 0):.1f}%")
        print(f"Memory Usage: {system.get('memory_usage', 0):.1f}%")
        print(f"Disk Usage: {system.get('disk_usage', 0):.1f}%")
        
        # Service metrics
        print("\nServices:")
        for endpoint, service_metrics in services.items():
            if service_metrics.get("available", False):
                status = "✅"
                response_time = service_metrics.get("response_time", 0)
                print(f"  {status} {endpoint}: {response_time:.3f}s")
            else:
                status = "❌"
                print(f"  {status} {endpoint}: Unavailable")
        
        # Alert summary
        if metrics["alerts"]:
            print(f"\n🚨 Active Alerts: {len(metrics['alerts'])}")
        
        print("-" * 40)
    
    def log_performance(self, metrics):
        """Log performance data"""
        self.performance_history.append(metrics)
        
        # Keep only last 1000 entries
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
        
        # Save to file periodically
        if len(self.performance_history) % 10 == 0:  # Every 10 entries
            self.save_performance_log()
    
    def save_performance_log(self):
        """Save performance log to file"""
        try:
            log_file = Path("logs/performance_log.json")
            log_file.parent.mkdir(exist_ok=True)
            
            with open(log_file, "w") as f:
                json.dump(self.performance_history, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving performance log: {e}")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        print("🛑 Performance monitoring stopped")
        
        # Save final log
        self.save_performance_log()
        
        # Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate performance summary report"""
        if not self.performance_history:
            return
        
        print("\n📈 Performance Summary Report")
        print("=" * 40)
        
        # Calculate averages
        total_entries = len(self.performance_history)
        
        cpu_usage_sum = sum(entry["system"].get("cpu_usage", 0) for entry in self.performance_history)
        memory_usage_sum = sum(entry["system"].get("memory_usage", 0) for entry in self.performance_history)
        
        avg_cpu = cpu_usage_sum / total_entries if total_entries > 0 else 0
        avg_memory = memory_usage_sum / total_entries if total_entries > 0 else 0
        
        print(f"Monitoring Duration: {total_entries * self.monitoring_interval} seconds")
        print(f"Average CPU Usage: {avg_cpu:.1f}%")
        print(f"Average Memory Usage: {avg_memory:.1f}%")
        print(f"Total Alerts: {len(self.alerts)}")
        
        # Alert breakdown
        alert_types = {}
        for alert in self.alerts:
            alert_type = alert["type"]
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        if alert_types:
            print("\nAlert Breakdown:")
            for alert_type, count in alert_types.items():
                print(f"  {alert_type}: {count}")
        
        print("=" * 40)

def main():
    """Main function"""
    try:
        monitor = EHBPerformanceMonitor()
        monitor.start_monitoring()
        return 0
    except Exception as e:
        print(f"❌ Performance monitor failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 