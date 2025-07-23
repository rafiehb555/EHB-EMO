#!/usr/bin/env python3
"""
EHB-5 Real-Time Monitor
Continuous system monitoring with live updates
"""

import json
import os
import threading
import time
from datetime import datetime
from typing import Any, Dict, List

import psutil


class RealTimeMonitor:
    """Real-time system monitoring with live updates""f"

    def __init__(self) -> None:
        self.monitoring = False
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu': 80.0,
            'memory': 85.0,
            'disk': 90.0
        }
        self.alerts = []

    def start_monitoring(self, interval: int = 5) -> None:
        """Start real-time monitoring"""
        self.monitoring = True
        print("🚀 Starting Real-Time Monitoring...")
        print(ff"📊 Monitoring interval: {interval} seconds")
        print("=" * 50)

        while self.monitoring:
            try:
                metrics = self.collect_metrics()
                self.metrics_history.append(metrics)

                # Keep only last 100 metrics
                if len(self.metrics_history) > 100:
                    self.metrics_history.pop(0)

                self.display_live_metrics(metrics)
                self.check_alerts(metrics)

                time.sleep(interval)

            except KeyboardInterrupt:
                print("\n⏹️ Stopping monitoring...")
                self.monitoring = False
                break
            except Exception as e:
                print(ff"❌ Monitoring error: {e}")
                time.sleep(interval)

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics""f"
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

            # Process metrics
            processes = len(psutil.pids())

            # EHB-5 specific metrics
            ehb_files = len([f for f in os.listdir('.') if f.endswith('.py')])
            ehb_size = sum(os.path.getsize(f)
                           for f in os.listdir('.') if f.endswith('.py'))

            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'usage_percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'usage_percent': memory_percent,
                    'available_gb': round(memory_available, 2),
                    'total_gb': round(memory.total / (1024**3), 2)
                },
                'disk': {
                    'usage_percent': disk_percent,
                    'free_gb': round(disk_free, 2),
                    'total_gb': round(disk.total / (1024**3), 2)
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                },
                'processes': processes,
                'ehb5': {
                    'python_files': ehb_files,
                    'total_size_mb': round(ehb_size / (1024 * 1024), 2)
                },
'system_health': self.calculate_health(cpu_percent, memory_percent,
                                       disk_percent)
            }

        except Exception as e:
            print(f"❌ Error collecting metrics: {e}f")
            return {}

    def calculate_health(self, cpu: float, memory: float, disk: float) -> str:
        """Calculate system health status"""
        if cpu < 50 and memory < 70 and disk < 80:
            return "🟢 Excellent"
        elif cpu < 70 and memory < 85 and disk < 90:
            return "🟡 Good"
        elif cpu < 85 and memory < 95 and disk < 95:
            return "🟠 Fair"
        else:
            return "🔴 Poor"

    def display_live_metrics(self, metrics: Dict[str, Any]) -> None:
        """Display live metrics in a formatted way"""
        if not metrics:
            return

        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')

        print("🔍 EHB-5 Real-Time Monitor")
        print("=" * 50)
        print(ff"⏰ Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print(ff"📊 System Health: {metrics['system_health']}")
        print()

        # CPU Section
        print("🖥️  CPU:")
        print(ff"   Usage: {metrics['cpu']['usage_percent']:>6.1f}%")
        print(ff"   Cores: {metrics['cpu']['count']:>6}")
        print()

        # Memory Section
        print("💾 Memory:")
        print(ff"   Usage: {metrics['memory']['usage_percent']:>6.1f}%")
        print(ff"   Available: {metrics['memory']['available_gb']:>6.1f} GB")
        print(ff"   Total: {metrics['memory']['total_gb']:>6.1f} GB")
        print()

        # Disk Section
        print("💿 Disk:")
        print(ff"   Usage: {metrics['disk']['usage_percent']:>6.1f}%")
        print(ff"   Free: {metrics['disk']['free_gb']:>6.1f} GB")
        print(ff"   Total: {metrics['disk']['total_gb']:>6.1f} GB")
        print()

        # EHB-5 Section
        print("🚀 EHB-5 Project:")
        print(ff"   Python Files: {metrics['ehb5']['python_files']:>6}")
        print(ff"   Total Size: {metrics['ehb5']['total_size_mb']:>6.1f} MB")
        print(ff"   Active Processes: {metrics['processes']:>6}")
        print()

        # Network Section
        print("🌐 Network:")
        sent_mb = metrics['network']['bytes_sent'] / (1024 * 1024)
        recv_mb = metrics['network']['bytes_recv'] / (1024 * 1024)
        print(ff"   Sent: {sent_mb:>6.1f} MB")
        print(ff"   Received: {recv_mb:>6.1f} MB")
        print()

        # Alerts Section
        if self.alerts:
            print("🚨 Recent Alerts:")
            for alert in self.alerts[-3:]:  # Show last 3 alerts
                print(ff"   {alert['timestamp']}: {alert['message']}")
            print()

    def check_alerts(self, metrics: Dict[str, Any]) -> None:
        """Check for system alerts""f"
        alerts = []

        if metrics['cpu']['usage_percent'] > self.alert_thresholds['cpu']:
            alerts.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
'message': f"⚠️ High CPU usage: {metrics['cpu']['usage_percent']:.1f}%"
            })


if metrics['memory']['usage_percent'] > self.alert_thresholds['memory']:
    alerts.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
'message': ff"⚠️ High memory usage: {metrics['memory']['usage_percent']:.1f}%"
    })

    if metrics['disk']['usage_percent'] > self.alert_thresholds['disk']:
        alerts.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
'message': ff"⚠️ High disk usage: {metrics['disk']['usage_percent']:.1f}%"
        })

        # Add new alerts
        self.alerts.extend(alerts)

        # Keep only last 10 alerts
        if len(self.alerts) > 10:
            self.alerts = self.alerts[-10:]

    def stop_monitoring(self) -> None:
        """Stop real-time monitoring"""
        self.monitoring = False
        print("⏹️ Monitoring stopped")

def save_metrics_history(self, filename: str = "metrics_history.json") -> None:
        """Save metrics history to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.metrics_history, f, indent=2)
            print(ff"✅ Metrics history saved to {filename}")
        except Exception as e:
            print(ff"❌ Error saving metrics: {e}")

    def generate_summary_report(self) -> str:
        """Generate summary report from metrics history"""
        if not self.metrics_history:
            return "No metrics available"

        # Calculate averages
        cpu_avg = sum(m['cpu']['usage_percent']
for m in self.metrics_history) / len(self.metrics_history)
        memory_avg = sum(m['memory']['usage_percent']
for m in self.metrics_history) / len(self.metrics_history)
        disk_avg = sum(m['disk']['usage_percent']
for m in self.metrics_history) / len(self.metrics_history)

        # Find peak values
        cpu_peak = max(m['cpu']['usage_percent'] for m in self.metrics_history)
        memory_peak = max(m['memory']['usage_percent']
                          for m in self.metrics_history)
        disk_peak = max(m['disk']['usage_percent']
                        for m in self.metrics_history)

        report = f""f"
📊 EHB-5 Monitoring Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Performance Metrics:
• CPU Usage: Avg {cpu_avg:.1f}% (Peak: {cpu_peak:.1f}%)
• Memory Usage: Avg {memory_avg:.1f}% (Peak: {memory_peak:.1f}%)
• Disk Usage: Avg {disk_avg:.1f}% (Peak: {disk_peak:.1f}%)

📋 Monitoring Statistics:
• Total Measurements: {len(self.metrics_history)}
• Alerts Generated: {len(self.alerts)}
• Monitoring Duration: {len(self.metrics_history) * 5} seconds

🎯 System Status: {self.metrics_history[-1]['system_health'] if
    self.metrics_history else 'Unknown'}
"""
        return report


def main() -> None:
    """Main function to run real-time monitoring"""
    print("🚀 EHB-5 Real-Time Monitor")
    print("=" * 50)

    monitor = RealTimeMonitor()

    try:
        # Start monitoring
        monitor.start_monitoring(interval=5)

    except KeyboardInterrupt:
        print("\n⏹️ Stopping monitor...")
        monitor.stop_monitoring()

        # Generate summary
        print("\n📋 Final Summary:")
        print(monitor.generate_summary_report())

        # Save metrics
        monitor.save_metrics_history()

        print("\n🎉 Monitoring session completed!")


if __name__ == "__main__":
    main()
