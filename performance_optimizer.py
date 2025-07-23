#!/usr/bin/env python3
"""
EHB-5 Performance Optimizer
Advanced performance optimization and monitoring system
"""

import functools
import threading
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import psutil


class CacheManager:
    """Intelligent caching system"""

    def __init__(self, max_size: int = 1000, ttl: int = 300) -> None:
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if time.time() - item["timestamp"] < self.ttl:
                    self.hits += 1
                    return item["value"]
                else:
                    del self.cache[key]

            self.misses += 1
            return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest item
                oldest_key = min(self.cache.keys(),
                               key=lambda k: self.cache[k]["timestamp"])
                del self.cache[oldest_key]

            self.cache[key] = {
                "value": value,
                "timestamp": time.time()
            }

    def clear(self) -> None:
        """Clear all cache"""
        with self.lock:
            self.cache.clear()

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "ttl": self.ttl,
                "hit_rate": self._calculate_hit_rate()
            }

    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class QueryOptimizer:
    """Database query optimization"""

    def __init__(self) -> None:
        self.query_stats = {}
        self.slow_queries = []
        self.optimization_suggestions = []

    def analyze_query(self, query: str, execution_time: float) -> None:
        """Analyze query performance"""
        query_hash = hash(query)

        if query_hash not in self.query_stats:
            self.query_stats[query_hash] = {
                "query": query,
                "count": 0,
                "total_time": 0,
                "avg_time": 0,
                "min_time": float('inf'),
                "max_time": 0
            }

        stats = self.query_stats[query_hash]
        stats["count"] += 1
        stats["total_time"] += execution_time
        stats["avg_time"] = stats["total_time"] / stats["count"]
        stats["min_time"] = min(stats["min_time"], execution_time)
        stats["max_time"] = max(stats["max_time"], execution_time)

        # Track slow queries
        if execution_time > 1.0:  # More than 1 second
            self.slow_queries.append({
                "query": query,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            })

            # Keep only last 100 slow queries
            if len(self.slow_queries) > 100:
                self.slow_queries = self.slow_queries[-100:]

    def get_optimization_suggestions(self) -> List[str]:
        """Get query optimization suggestions"""
        suggestions = []

        for query_hash, stats in self.query_stats.items():
            if stats["avg_time"] > 0.5:  # Average time > 500ms
                suggestions.append(
                    f"Query taking {stats['avg_time']:.2f}s on average: "
                    f"{stats['query'][:100]}...")

            if stats["count"] > 100:  # Frequently executed
                suggestions.append(
                    f"Frequently executed query ({stats['count']} times): "
                    f"Consider caching")

        return suggestions


class PerformanceProfiler:
    """Performance profiling and monitoring"""

    def __init__(self) -> None:
        self.profiles = {}
        self.active_profiles = {}

    def start_profile(self, name: str) -> None:
        """Start profiling a function or operation"""
        self.active_profiles[name] = {
            "start_time": time.time(),
            "start_memory": self._get_memory_usage()
        }

    def end_profile(self, name: str) -> Dict:
        """End profiling and return results"""
        if name not in self.active_profiles:
            return {}

        start_data = self.active_profiles[name]
        end_time = time.time()
        end_memory = self._get_memory_usage()

        profile_data = {
            "execution_time": end_time - start_data["start_time"],
            "memory_delta": end_memory - start_data["start_memory"],
            "timestamp": datetime.now().isoformat()
        }

        if name not in self.profiles:
            self.profiles[name] = []

        self.profiles[name].append(profile_data)
        del self.active_profiles[name]

        return profile_data

    def get_profile_stats(self, name: str) -> Dict:
        """Get profiling statistics for a name"""
        if name not in self.profiles:
            return {}

        profiles = self.profiles[name]
        execution_times = [p["execution_time"] for p in profiles]
        memory_deltas = [p["memory_delta"] for p in profiles]

        return {
            "count": len(profiles),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "min_execution_time": min(execution_times),
            "max_execution_time": max(execution_times),
            "avg_memory_delta": sum(memory_deltas) / len(memory_deltas),
            "total_memory_delta": sum(memory_deltas)
        }

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0


def cache_result(ttl: int = 300):
    """Decorator to cache function results"""
    def decorator(func: Callable) -> Callable:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = (f"{func.__name__}:"
                        f"{hash(str(args) + str(sorted(kwargs.items())))}")

            # Try to get from cache
            if cache_key in cache:
                cached_result = cache[cache_key]
                if time.time() - cached_result["timestamp"] < ttl:
                    return cached_result["value"]

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = {
                "value": result,
                "timestamp": time.time()
            }

            return result

        return wrapper
    return decorator


class ResourceManager:
    """Resource management and optimization"""

    def __init__(self) -> None:
        self.resource_limits = {
            "max_memory_mb": 1024,
            "max_cpu_percent": 80,
            "max_disk_percent": 85
        }
        self.current_usage = {}
        self.alerts = []

    def check_resource_usage(self) -> Dict:
        """Check current resource usage"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_mb = memory.used / 1024 / 1024

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Disk usage
            disk = psutil.disk_usage('.')
            disk_percent = disk.percent

            self.current_usage = {
                "memory": {
                    "percent": memory_percent,
                    "used_mb": memory_mb,
                    "limit_mb": self.resource_limits["max_memory_mb"]
                },
                "cpu": {
                    "percent": cpu_percent,
                    "limit_percent": self.resource_limits["max_cpu_percent"]
                },
                "disk": {
                    "percent": disk_percent,
                    "limit_percent": self.resource_limits["max_disk_percent"]
                }
            }

            return self.current_usage

        except Exception as e:
            print(f"Error checking resource usage: {e}")
            return {}

    def get_alerts(self) -> List[Dict]:
        """Get resource alerts"""
        alerts = []

        if self.current_usage.get("memory", {}).get("percent", 0) > 80:
            alerts.append({
                "type": "high_memory",
                "message": "Memory usage is high",
                "value": self.current_usage["memory"]["percent"],
                "limit": 80
            })

        if self.current_usage.get("cpu", {}).get("percent", 0) > 80:
            alerts.append({
                "type": "high_cpu",
                "message": "CPU usage is high",
                "value": self.current_usage["cpu"]["percent"],
                "limit": 80
            })

        if self.current_usage.get("disk", {}).get("percent", 0) > 85:
            alerts.append({
                "type": "low_disk",
                "message": "Disk space is low",
                "value": self.current_usage["disk"]["percent"],
                "limit": 85
            })

        return alerts

    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        recommendations = []
        usage = self.current_usage

        if usage.get("memory", {}).get("percent", 0) > 70:
            recommendations.append(
"Consider implementing memory caching for frequently accessed data")

        if usage.get("cpu", {}).get("percent", 0) > 70:
            recommendations.append(
"Consider optimizing database queries and implementing query caching")

        if usage.get("disk", {}).get("percent", 0) > 80:
            recommendations.append(
                "Consider implementing data archiving and cleanup procedures")

        return recommendations


class PerformanceOptimizer:
    """Main performance optimization system"""

    def __init__(self) -> None:
        self.cache_manager = CacheManager()
        self.query_optimizer = QueryOptimizer()
        self.profiler = PerformanceProfiler()
        self.resource_manager = ResourceManager()

    def optimize_system(self) -> Dict:
        """Run complete system optimization"""
        print("⚡ Starting Performance Optimization...")

        # Check resource usage
        resource_usage = self.resource_manager.check_resource_usage()
        alerts = self.resource_manager.get_alerts()
recommendations = self.resource_manager.get_optimization_recommendations()

        # Get cache statistics
        cache_stats = self.cache_manager.get_stats()

        # Get query optimization suggestions
        query_suggestions = self.query_optimizer.get_optimization_suggestions()

        optimization_report = {
            "resource_usage": resource_usage,
            "alerts": alerts,
            "recommendations": recommendations,
            "cache_stats": cache_stats,
            "query_suggestions": query_suggestions,
            "timestamp": datetime.now().isoformat()
        }

        print("✅ Performance optimization completed!")
        return optimization_report

    def start_monitoring(self) -> None:
        """Start continuous performance monitoring"""
        print("👁️ Starting performance monitoring...")

        while True:
            try:
                self.optimize_system()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print("🛑 Performance monitoring stopped")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(10)


def main() -> None:
    """Main function"""
    optimizer = PerformanceOptimizer()

    if len(sys.argv) > 1 and sys.argv[1] == '--monitor':
        optimizer.start_monitoring()
    else:
        report = optimizer.optimize_system()
        print("📊 Performance Report:")
print(f"Memory Usage: {report['resource_usage']['memory']['percent']}%")
        print(f"CPU Usage: {report['resource_usage']['cpu']['percent']}%")
        print(f"Disk Usage: {report['resource_usage']['disk']['percent']}%")
        print(f"Cache Hit Rate: {report['cache_stats']['hit_rate']:.2%}")


if __name__ == "__main__":
    import sys
    main()
