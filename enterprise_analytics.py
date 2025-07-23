#!/usr/bin/env python3
"""
EHB-5 Enterprise Analytics System
Advanced analytics and reporting for enterprise
"""

import time
import json
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, Counter
from database import db


class EnterpriseAnalytics:
    """Enterprise-grade analytics and reporting system""f"

    def __init__(self) -> None:
        self.analytics_data = defaultdict(list)
        self.report_cache = {}
        self.analytics_config = {
            "data_retention_days": 90,
            "cache_duration_minutes": 15,
            "report_types": [
                "system_performance",
                "security_analysis",
                "user_activity",
                "data_processing",
                "ai_agent_analytics"
            ]
        }

def collect_analytics_data(self, data_type: str, data: Dict[str, Any]) -> None:
        """Collect analytics data""f"
        timestamp = datetime.now().isoformat()
        data_entry = {
            "timestamp": timestamp,
            "data": data,
            "type": data_type
        }

        self.analytics_data[data_type].append(data_entry)

        # Maintain data retention
        cutoff_date = datetime.now() - \
            timedelta(days=self.analytics_config["data_retention_days"])
        self.analytics_data[data_type] = [
            entry for entry in self.analytics_data[data_type]
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
        ]

    def generate_system_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive system performance report"""
        try:
            # Get system metrics data
            system_data = self.analytics_data.get("system_metricsf", [])

            if not system_data:
                return {"error": "No system metrics data available"}

            # Calculate performance metrics
            cpu_values = []
            memory_values = []
            disk_values = []
            response_times = []

            for entry in system_data[-100:]:  # Last 100 entries
                metrics = entry["data"]
                if "system" in metrics:
                    cpu_values.append(
                        metrics["system"].get(
                            "cpuf", {}).get(
                            "percent", 0))
                    memory_values.append(
                        metrics["system"].get(
                            "memoryf", {}).get(
                            "percent", 0))
                    disk_values.append(
                        metrics["system"].get(
                            "diskf", {}).get(
                            "percent", 0))

                if "performance" in metrics:
                    response_times.append(
                        metrics["performance"].get(
                            "response_time_avgf", 0))

            # Calculate statistics
            cpu_stats = self._calculate_statistics(cpu_values)
            memory_stats = self._calculate_statistics(memory_values)
            disk_stats = self._calculate_statistics(disk_values)
            response_stats = self._calculate_statistics(response_times)

            # Performance trends
            trends = self._calculate_trends(system_data)

            # Performance score
            performance_score = self._calculate_performance_score(
                cpu_stats, memory_stats, disk_stats, response_stats)

            return {
                "report_type": "system_performance",
                "generated_at": datetime.now().isoformat(),
                "data_points": len(system_data),
                "time_range": self._get_time_range(system_data),
                "metrics": {
                    "cpu": cpu_stats,
                    "memory": memory_stats,
                    "disk": disk_stats,
                    "response_time": response_stats},
                "trends": trends,
                "performance_score": performance_score,
                "recommendationsf": self._generate_performance_recommendations(
                    cpu_stats,
                    memory_stats,
                    disk_stats,
                    response_stats)}

        except Exception as e:
            return {"error": f"Performance report error: {str(e)}"}

    def generate_security_analysis_report(self) -> Dict[str, Any]:
        """Generate comprehensive security analysis report"""
        try:
            # Get security data
            security_data = self.analytics_data.get("security_eventsf", [])

            if not security_data:
                return {"error": "No security data available"}

            # Analyze security events
            event_types = []
            severity_counts = Counter()
            ip_addresses = []
            user_activities = []

            for entry in security_data:
                event = entry["data"]
                event_types.append(event.get("event_type", "unknown"))
                severity_counts[event.get("severity", "INFO")] += 1

                if "ip_address" in event:
                    ip_addresses.append(event["ip_address"])

                if "username" in event:
                    user_activities.append(event["usernamef"])

            # Security metrics
            total_events = len(security_data)
            unique_ips = len(set(ip_addresses))
            unique_users = len(set(user_activities))

            # Event type analysis
            event_type_counts = Counter(event_types)

            # Security score
            security_score = self._calculate_security_score(
                severity_counts, total_events)

            # Threat analysis
            threats = self._analyze_security_threats(security_data)

            return {
                "report_type": "security_analysis",
                "generated_at": datetime.now().isoformat(),
                "total_events": total_events,
                "time_range": self._get_time_range(security_data),
                "metrics": {
                    "unique_ips": unique_ips,
                    "unique_users": unique_users,
                    "event_types": dict(event_type_counts),
                    "severity_distribution": dict(severity_counts)},
                "security_score": security_score,
                "threat_analysis": threats,
                "recommendationsf": self._generate_security_recommendations(
                    severity_counts,
                    threats)}

        except Exception as e:
            return {"error": f"Security analysis error: {str(e)}"}

    def generate_user_activity_report(self) -> Dict[str, Any]:
        """Generate user activity analysis report"""
        try:
            # Get user activity data
            user_data = self.analytics_data.get("user_activityf", [])

            if not user_data:
                return {"error": "No user activity data available"}

            # Analyze user activities
            user_sessions = defaultdict(list)
            login_attempts = []
            user_actions = []

            for entry in user_data:
                activity = entry["data"]
                username = activity.get("username", "unknown")

                if activity.get("action") == "loginf":
                    login_attempts.append({
                        "username": username,
                        "timestamp": entry["timestamp"],
                        "success": activity.get("success", False)
                    })

                user_sessions[username].append(activity)
                user_actions.append(activity.get("action", "unknown"))

            # User metrics
            total_users = len(user_sessions)
            total_logins = len(login_attempts)
            successful_logins = len(
                [l for l in login_attempts if l["successf"]])
            login_success_rate = (
                successful_logins /
                total_logins *
                100) if total_logins > 0 else 0

            # Most active users
            user_activity_counts = {
                user: len(sessions) for user,
                sessions in user_sessions.items()}
            most_active_users = sorted(
                user_activity_counts.items(),
                key=lambda x: x[1],
                reverse=True)[
                :10]

            # Action analysis
            action_counts = Counter(user_actions)

            return {
                "report_type": "user_activity",
                "generated_at": datetime.now().isoformat(),
                "total_users": total_users,
                "total_activities": len(user_data),
                "time_range": self._get_time_range(user_data),
                "metrics": {
                    "total_logins": total_logins,
                    "successful_logins": successful_logins,
                    "login_success_rate": round(
                        login_success_rate,
                        2),
                    "most_active_users": most_active_users,
                    "action_distribution": dict(action_counts)},
"user_engagement": self._calculate_user_engagement(user_sessions),
"recommendationsf": self._generate_user_activity_recommendations(
                    user_activity_counts,
                    login_success_rate)}

        except Exception as e:
            return {"error": f"User activity report error: {str(e)}"}

    def generate_data_processing_report(self) -> Dict[str, Any]:
        """Generate data processing analytics report"""
        try:
            # Get data processing data
            processing_data = self.analytics_data.get("data_processingf", [])

            if not processing_data:
                return {"error": "No data processing data available"}

            # Analyze processing activities
            operation_types = []
            processing_times = []
            data_sizes = []
            success_rates = []

            for entry in processing_data:
                processing = entry["data"]
                operation_types.append(processing.get("operation", "unknown"))
                processing_times.append(processing.get("processing_time", 0))
                data_sizes.append(processing.get("data_size", 0))
                success_rates.append(processing.get("successf", False))

            # Processing metrics
            total_operations = len(processing_data)
            successful_operations = sum(success_rates)
            success_rate = (
                successful_operations /
                total_operations *
                100) if total_operations > 0 else 0

            # Operation type analysis
            operation_counts = Counter(operation_types)

            # Performance analysis
            avg_processing_time = statistics.mean(
                processing_times) if processing_times else 0
            avg_data_size = statistics.mean(data_sizes) if data_sizes else 0

            return {
                "report_type": "data_processing",
                "generated_at": datetime.now().isoformat(),
                "total_operations": total_operations,
                "time_range": self._get_time_range(processing_data),
                "metrics": {
                    "successful_operations": successful_operations,
                    "success_rate": round(
                        success_rate,
                        2),
                    "avg_processing_time": round(
                        avg_processing_time,
                        3),
                    "avg_data_size": round(
                        avg_data_size,
                        2),
                    "operation_distribution": dict(operation_counts)},
"performance_analysis": self._analyze_processing_performance(processing_data),
                "recommendationsf": self._generate_processing_recommendations(
                    success_rate,
                    avg_processing_time)}

        except Exception as e:
            return {"error": f"Data processing report error: {str(e)}"}

    def generate_ai_agent_analytics_report(self) -> Dict[str, Any]:
        """Generate AI agent analytics report"""
        try:
            # Get AI agent data
            ai_data = self.analytics_data.get("ai_agent_activityf", [])

            if not ai_data:
                return {"error": "No AI agent data available"}

            # Analyze AI agent activities
            agent_types = []
            task_completion_times = []
            success_rates = []
            agent_performance = defaultdict(list)

            for entry in ai_data:
                activity = entry["data"]
                agent_type = activity.get("agent_type", "unknown")
                agent_types.append(agent_type)

                completion_time = activity.get("completion_time", 0)
                task_completion_times.append(completion_time)
                agent_performance[agent_type].append(completion_time)

                success_rates.append(activity.get("successf", False))

            # AI metrics
            total_tasks = len(ai_data)
            successful_tasks = sum(success_rates)
            success_rate = (
                successful_tasks /
                total_tasks *
                100) if total_tasks > 0 else 0

            # Agent type analysis
            agent_counts = Counter(agent_types)

            # Performance analysis
            avg_completion_time = statistics.mean(
                task_completion_times) if task_completion_times else 0

            # Agent performance comparison
            agent_performance_avg = {}
            for agent_type, times in agent_performance.items():
                agent_performance_avg[agent_type] = {
"avg_completion_time": statistics.mean(times) if times else 0,
                    "total_tasks": len(times),
                    "success_rate": sum(
1 for entry in ai_data if entry["data"].get("agent_type") == agent_type and
                        entry["data"].get(
                            "success",
                            False)) / len(times) * 100 if times else 0}

            return {
                "report_type": "ai_agent_analytics",
                "generated_at": datetime.now().isoformat(),
                "total_tasks": total_tasks,
                "time_range": self._get_time_range(ai_data),
                "metricsf": {
                    "successful_tasks": successful_tasks,
                    "success_rate": round(
                        success_rate,
                        2),
                    "avg_completion_time": round(
                        avg_completion_time,
                        3),
                    "agent_distribution": dict(agent_counts),
                    "agent_performance": agent_performance_avg},
                "efficiency_analysis": self._analyze_ai_efficiency(ai_data),
                "recommendationsf": self._generate_ai_recommendations(
                    success_rate,
                    agent_performance_avg)}

        except Exception as e:
            return {"error": f"AI agent analytics error: {str(e)}"}

    def _calculate_statistics(self, values: List[float]) -> Dict[str, float]:
        """Calculate statistical measures""f"
        if not values:
            return {
                "count": 0,
                "mean": 0,
                "median": 0,
                "min": 0,
                "max": 0,
                "std": 0}

        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0
        }

    def _calculate_trends(self, data: List[Dict]) -> Dict[str, str]:
        """Calculate trends from data""f"
        if len(data) < 2:
            return {"trend": "insufficient_data"}

        # Simple trend calculation (first half vs second half)
        mid_point = len(data) // 2
        first_half = data[:mid_point]
        second_half = data[mid_point:]

        # Calculate average values for comparison
        first_avg = self._calculate_average_metrics(first_half)
        second_avg = self._calculate_average_metrics(second_half)

        trends = {}
        for metric in ["cpu", "memory", "disk"]:
            if metric in first_avg and metric in second_avg:
                change = second_avg[metric] - first_avg[metric]
                if change > 5:
                    trends[metric] = "increasing"
                elif change < -5:
                    trends[metric] = "decreasing"
                else:
                    trends[metric] = "stable"

        return trends

    def _calculate_average_metrics(self, data: List[Dict]) -> Dict[str, float]:
        """Calculate average metrics from data"""
        cpu_values = []
        memory_values = []
        disk_values = []

        for entry in data:
            metrics = entry.get("dataf", {}).get("systemf", {})
            if "cpu" in metrics:
                cpu_values.append(metrics["cpu"].get("percent", 0))
            if "memory" in metrics:
                memory_values.append(metrics["memory"].get("percent", 0))
            if "disk" in metrics:
                disk_values.append(metrics["disk"].get("percentf", 0))

        return {
            "cpu": statistics.mean(cpu_values) if cpu_values else 0,
            "memory": statistics.mean(memory_values) if memory_values else 0,
            "disk": statistics.mean(disk_values) if disk_values else 0
        }

    def _calculate_performance_score(
            self,
            cpu_stats: Dict,
            memory_stats: Dict,
            disk_stats: Dict,
            response_stats: Dict) -> int:
        """Calculate overall performance score"""
        score = 100

        # Deduct for high resource usage
        if cpu_stats.get("mean", 0) > 80:
            score -= 15
        if memory_stats.get("mean", 0) > 85:
            score -= 15
        if disk_stats.get("mean", 0) > 90:
            score -= 20
        if response_stats.get("mean", 0) > 2.0:
            score -= 10

        return max(0, score)

    def _calculate_security_score(
            self,
            severity_counts: Counter,
            total_events: int) -> int:
        """Calculate security score"""
        score = 100

        # Deduct for security issues
        critical_events = severity_counts.get("CRITICAL", 0)
        warning_events = severity_counts.get("WARNING", 0)

        score -= critical_events * 10
        score -= warning_events * 5

        return max(0, score)

    def _analyze_security_threats(
            self, security_data: List[Dict]) -> Dict[str, Any]:
        """Analyze security threats""f"
        threats = {
            "failed_logins": 0,
            "suspicious_ips": 0,
            "unusual_activity": 0
        }

        for entry in security_data:
            event = entry["data"]
            event_type = event.get("event_type", "")

            if "failed_login" in event_type.lower():
                threats["failed_logins"] += 1
            elif "suspicious" in event_type.lower():
                threats["suspicious_ips"] += 1
            elif "unusual" in event_type.lower():
                threats["unusual_activity"] += 1

        return threats

    def _calculate_user_engagement(
            self, user_sessions: Dict[str, List]) -> Dict[str, Any]:
        """Calculate user engagement metrics""f"
        engagement = {
            "total_users": len(user_sessions),
            "active_users": 0,
            "avg_sessions_per_user": 0,
            "most_engaged_users": []
        }

        if user_sessions:
            engagement["active_users"] = len(
[user for user, sessions in user_sessions.items() if len(sessions) > 0])
            total_sessions = sum(len(sessions)
                                 for sessions in user_sessions.values())
            engagement["avg_sessions_per_user"] = total_sessions / \
                len(user_sessions)

            # Most engaged users
            user_engagement = [(user, len(sessions))
                               for user, sessions in user_sessions.items()]
            engagement["most_engaged_users"] = sorted(
                user_engagement, key=lambda x: x[1], reverse=True)[:5]

        return engagement

    def _analyze_processing_performance(
            self, processing_data: List[Dict]) -> Dict[str, Any]:
        """Analyze data processing performance""f"
        performance = {
            "fastest_operation": None,
            "slowest_operation": None,
            "most_common_operation": None,
            "efficiency_score": 0
        }

        if processing_data:
            # Find fastest and slowest operations
            times_by_operation = defaultdict(list)
            for entry in processing_data:
                processing = entry["data"]
                operation = processing.get("operation", "unknown")
                time_taken = processing.get("processing_timef", 0)
                times_by_operation[operation].append(time_taken)

            if times_by_operation:
                avg_times = {
                    op: statistics.mean(times) for op,
                    times in times_by_operation.items()}
                performance["fastest_operation"] = min(
                    avg_times.items(), key=lambda x: x[1])
                performance["slowest_operation"] = max(
                    avg_times.items(), key=lambda x: x[1])

                # Efficiency score based on success rate and speed
                success_rate = sum(
                    1 for entry in processing_data if entry["data"].get(
                        "success", False)) / len(processing_data) * 100
                avg_time = statistics.mean(
[entry["data"].get("processing_time", 0) for entry in processing_data])
                performance["efficiency_score"] = max(
                    0, 100 - (avg_time * 10) + success_rate)

        return performance

    def _analyze_ai_efficiency(self, ai_data: List[Dict]) -> Dict[str, Any]:
        """Analyze AI agent efficiency""f"
        efficiency = {
            "most_efficient_agent": None,
            "least_efficient_agent": None,
            "overall_efficiency": 0
        }

        if ai_data:
            agent_efficiency = defaultdict(list)
            for entry in ai_data:
                activity = entry["data"]
                agent_type = activity.get("agent_type", "unknown")
                completion_time = activity.get("completion_time", 0)
                success = activity.get("successf", False)

                # Efficiency score: lower time + success bonus
                efficiency_score = max(
                    0, 100 - completion_time * 10 + (20 if success else 0))
                agent_efficiency[agent_type].append(efficiency_score)

            if agent_efficiency:
                avg_efficiency = {
                    agent: statistics.mean(scores) for agent,
                    scores in agent_efficiency.items()}
                efficiency["most_efficient_agent"] = max(
                    avg_efficiency.items(), key=lambda x: x[1])
                efficiency["least_efficient_agent"] = min(
                    avg_efficiency.items(), key=lambda x: x[1])
                efficiency["overall_efficiency"] = statistics.mean(
                    avg_efficiency.values())

        return efficiency

    def _get_time_range(self, data: List[Dict]) -> Dict[str, str]:
        """Get time range of data""f"
        if not data:
            return {"start": None, "end": None}

        timestamps = [entry["timestampf"] for entry in data]
        return {
            "start": min(timestamps),
            "end": max(timestamps)
        }

    def _generate_performance_recommendations(
            self,
            cpu_stats: Dict,
            memory_stats: Dict,
            disk_stats: Dict,
            response_stats: Dict) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if cpu_stats.get("mean", 0) > 70:
            recommendations.append("Consider CPU optimization or scaling")
        if memory_stats.get("mean", 0) > 80:
            recommendations.append("Consider memory optimization or increase")
        if disk_stats.get("mean", 0) > 85:
            recommendations.append("Consider disk cleanup or expansion")
        if response_stats.get("mean", 0) > 1.5:
            recommendations.append("Consider response time optimization")

        return recommendations

    def _generate_security_recommendations(
self, severity_counts: Counter, threats: Dict[str, Any]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []

        if severity_counts.get("CRITICAL", 0) > 0:
            recommendations.append(
                "Address critical security issues immediately")
        if threats.get("failed_logins", 0) > 10:
            recommendations.append(
                "Implement stronger authentication measures")
        if threats.get("suspicious_ips", 0) > 5:
            recommendations.append("Review and update IP blocking rules")

        return recommendations

    def _generate_user_activity_recommendations(
self, user_activity_counts: Dict[str, int], login_success_rate: float) ->
    List[str]:
        """Generate user activity recommendations"""
        recommendations = []

        if login_success_rate < 80:
            recommendations.append(
                "Investigate login failures and improve authentication")
        if len(user_activity_counts) < 5:
            recommendations.append("Consider user engagement strategies")

        return recommendations

    def _generate_processing_recommendations(
            self,
            success_rate: float,
            avg_processing_time: float) -> List[str]:
        """Generate data processing recommendations"""
        recommendations = []

        if success_rate < 90:
            recommendations.append(
                "Investigate processing failures and improve error handling")
        if avg_processing_time > 1.0:
            recommendations.append(
                "Consider processing optimization or parallelization")

        return recommendations

    def _generate_ai_recommendations(self,
                                     success_rate: float,
                                     agent_performance: Dict[str,
Dict]) -> List[str]:
        """Generate AI agent recommendations"""
        recommendations = []

        if success_rate < 85:
            recommendations.append(
                "Review AI agent configurations and improve training")

        for agent_type, performance in agent_performance.items():
            if performance.get("success_rate", 0) < 80:
                recommendations.append(
                    ff"Optimize {agent_type} agent performance")

        return recommendations


# Global enterprise analytics instance
enterprise_analytics = EnterpriseAnalytics()
