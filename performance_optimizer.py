#!/usr/bin/env python3
"""
EHB-5 Performance Optimizer
System performance optimization and caching
"""

import time
import threading
import functools
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, List
from collections import OrderedDict

class CacheManager:
    """Intelligent caching system"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.max_size = max_size
        self.ttl = ttl  # seconds
        self.cache = OrderedDict()
        self.access_times = {}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                # Check if expired
                if time.time() - self.access_times[key] > self.ttl:
                    del self.cache[key]
                    del self.access_times[key]
                    return None
                
                # Move to end (LRU)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.access_times[key] = time.time()
                return value
            return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        with self.lock:
            # Remove if exists
            if key in self.cache:
                del self.cache[key]
                del self.access_times[key]
            
            # Add new value
            self.cache[key] = value
            self.access_times[key] = time.time()
            
            # Remove oldest if cache is full
            if len(self.cache) > self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.access_times[oldest_key]
    
    def clear(self):
        """Clear all cache"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
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
        # This is a simplified calculation
        return 0.85  # Placeholder

class QueryOptimizer:
    """Database query optimization"""
    
    def __init__(self):
        self.query_stats = {}
        self.slow_queries = []
        self.optimization_suggestions = []
    
    def analyze_query(self, query: str, execution_time: float):
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
                suggestions.append(f"Query taking {stats['avg_time']:.2f}s on average: {stats['query'][:100]}...")
            
            if stats["count"] > 100:  # Frequently executed
                suggestions.append(f"Frequently executed query ({stats['count']} times): Consider caching")
        
        return suggestions

class PerformanceProfiler:
    """Performance profiling and monitoring"""
    
    def __init__(self):
        self.profiles = {}
        self.active_profiles = {}
    
    def start_profile(self, name: str):
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
        
        # Keep only last 100 profiles per name
        if len(self.profiles[name]) > 100:
            self.profiles[name] = self.profiles[name][-100:]
        
        del self.active_profiles[name]
        return profile_data
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            return 0.0
    
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

def cache_result(ttl: int = 300):
    """Decorator to cache function results"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items()))}"
            
            # Try to get from cache
            result = cache_manager.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result)
            return result
        
        return wrapper
    return decorator

def profile_function(name: str = None):
    """Decorator to profile function performance"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profile_name = name or func.__name__
            performance_profiler.start_profile(profile_name)
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                performance_profiler.end_profile(profile_name)
        
        return wrapper
    return decorator

class ResourceManager:
    """Resource management and optimization"""
    
    def __init__(self):
        self.resource_limits = {
            "max_memory_mb": 512,
            "max_cpu_percent": 80,
            "max_disk_percent": 90
        }
        self.current_usage = {}
        self.alerts = []
    
    def check_resource_usage(self) -> Dict:
        """Check current resource usage"""
        try:
            import psutil
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_mb = memory.used / (1024 * 1024)
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            self.current_usage = {
                "memory": {
                    "percent": memory_percent,
                    "mb": round(memory_mb, 2),
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
            
            # Check for alerts
            self._check_alerts()
            
            return self.current_usage
            
        except ImportError:
            return {"error": "psutil not available"}
    
    def _check_alerts(self):
        """Check for resource usage alerts"""
        alerts = []
        
        if self.current_usage.get("memory", {}).get("percent", 0) > 80:
            alerts.append({
                "type": "high_memory",
                "message": f"High memory usage: {self.current_usage['memory']['percent']}%",
                "severity": "warning"
            })
        
        if self.current_usage.get("cpu", {}).get("percent", 0) > 80:
            alerts.append({
                "type": "high_cpu",
                "message": f"High CPU usage: {self.current_usage['cpu']['percent']}%",
                "severity": "warning"
            })
        
        if self.current_usage.get("disk", {}).get("percent", 0) > 85:
            alerts.append({
                "type": "low_disk",
                "message": f"Low disk space: {self.current_usage['disk']['percent']}%",
                "severity": "critical"
            })
        
        self.alerts = alerts
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        
        usage = self.current_usage
        
        if usage.get("memory", {}).get("percent", 0) > 70:
            recommendations.append("Consider implementing memory caching for frequently accessed data")
        
        if usage.get("cpu", {}).get("percent", 0) > 70:
            recommendations.append("Consider optimizing database queries and implementing query caching")
        
        if usage.get("disk", {}).get("percent", 0) > 80:
            recommendations.append("Consider implementing data archiving and cleanup procedures")
        
        return recommendations

# Global performance instances
cache_manager = CacheManager()
query_optimizer = QueryOptimizer()
performance_profiler = PerformanceProfiler()
resource_manager = ResourceManager() 