#!/usr/bin/env python3
"""
EHB-5 Enterprise Dashboard System
Advanced enterprise dashboard with real-time monitoring
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from enterprise_security import enterprise_security
from enterprise_monitoring import enterprise_monitor
from enterprise_analytics import enterprise_analytics


class EnterpriseDashboard:
    """Enterprise-grade dashboard system"""

    def __init__(self):
        self.dashboard_config = {
            "refresh_interval": 30,  # seconds
            "max_data_points": 1000,
            "alert_thresholds": {
                "critical": 90,
                "warning": 70,
                "info": 50
            }
        }
        self.dashboard_data = {}
        self.last_update = None

    def get_comprehensive_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        try:
            # Get all system data
            system_metrics = enterprise_monitor.get_enterprise_dashboard_data()
            security_analytics = enterprise_security.get_security_analytics()

            # Generate analytics reports
performance_report = enterprise_analytics.generate_system_performance_report()
security_report = enterprise_analytics.generate_security_analysis_report()
user_activity_report = enterprise_analytics.generate_user_activity_report()
processing_report = enterprise_analytics.generate_data_processing_report()
ai_analytics_report = enterprise_analytics.generate_ai_agent_analytics_report()

            # Compile dashboard data
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "system_overview": self._get_system_overview(system_metrics),
                "security_overview": self._get_security_overview(
                    security_analytics,
                    security_report),
"performance_overview": self._get_performance_overview(performance_report),
                "user_overview": self._get_user_overview(user_activity_report),
"processing_overview": self._get_processing_overview(processing_report),
                "ai_overview": self._get_ai_overview(ai_analytics_report),
                "alerts": self._get_active_alerts(
                    system_metrics,
                    security_analytics),
                "recommendations": self._get_dashboard_recommendations(
                    system_metrics,
                    security_analytics,
                    performance_report),
                "status": self._get_overall_status(
                    system_metrics,
                    security_analytics)}

            self.dashboard_data = dashboard_data
            self.last_update = datetime.now()

            return dashboard_data

        except Exception as e:
            return {
                "error": f"Dashboard data error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _get_system_overview(
            self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Get system overview data"""
        try:
            current_metrics = system_metrics.get("current_metrics", {})
            averages = system_metrics.get("averages", {})

            return {
                "status": system_metrics.get(
                    "system_health",
                    {}).get(
                    "status",
                    "unknown"),
                "health_score": system_metrics.get(
                    "system_health",
                    {}).get(
                    "score",
                    0),
                "uptime": current_metrics.get(
                    "uptime",
                        "Unknown"),
                "current_metrics": {
                    "cpu_percent": current_metrics.get(
                        "system",
                        {}).get(
                        "cpu",
                        {}).get(
                        "percent",
                        0),
                    "memory_percent": current_metrics.get(
                        "system",
                        {}).get(
                        "memory",
                        {}).get(
                        "percent",
                        0),
                    "disk_percent": current_metrics.get(
                        "system",
                        {}).get(
                        "disk",
                        {}).get(
                        "percent",
                        0)},
                "average_metrics": averages,
                "monitoring_status": system_metrics.get(
                    "monitoring_status",
                    {})}
        except Exception as e:
            return {"error": f"System overview error: {str(e)}"}

    def _get_security_overview(self,
                               security_analytics: Dict[str,
                                                        Any],
                               security_report: Dict[str,
                                                     Any]) -> Dict[str,
                                                                   Any]:
        """Get security overview data"""
        try:
            return {
                "security_score": security_analytics.get("security_score", 0),
"total_events_24h": security_analytics.get("total_events_24h", 0),
                "blocked_ips": security_analytics.get("blocked_ips", 0),
"active_sessions": security_analytics.get("active_sessions", 0),
"threat_level": self._calculate_threat_level(security_analytics),
                "recent_events": security_analytics.get("event_breakdown", {}),
                "security_metrics": security_report.get("metrics", {})
            }
        except Exception as e:
            return {"error": f"Security overview error: {str(e)}"}

    def _get_performance_overview(
            self, performance_report: Dict[str, Any]) -> Dict[str, Any]:
        """Get performance overview data"""
        try:
            return {
                "performance_score": performance_report.get(
"performance_score", 0), "data_points": performance_report.get(
                    "data_points", 0), "metrics": performance_report.get(
                    "metrics", {}), "trends": performance_report.get(
                    "trends", {}), "recommendations": performance_report.get(
                        "recommendations", [])}
        except Exception as e:
            return {"error": f"Performance overview error: {str(e)}"}

    def _get_user_overview(
            self, user_activity_report: Dict[str, Any]) -> Dict[str, Any]:
        """Get user activity overview data"""
        try:
            return {
                "total_users": user_activity_report.get(
"total_users", 0), "total_activities": user_activity_report.get(
"total_activities", 0), "login_success_rate": user_activity_report.get(
                    "metrics", {}).get(
"login_success_rate", 0), "user_engagement": user_activity_report.get(
"user_engagement", {}), "most_active_users": user_activity_report.get(
                            "metrics", {}).get(
                                "most_active_users", [])}
        except Exception as e:
            return {"error": f"User overview error: {str(e)}"}

    def _get_processing_overview(
            self, processing_report: Dict[str, Any]) -> Dict[str, Any]:
        """Get data processing overview data"""
        try:
            return {
                "total_operations": processing_report.get(
                    "total_operations",
                    0),
                "success_rate": processing_report.get(
                    "metrics",
                    {}).get(
                    "success_rate",
                    0),
                "avg_processing_time": processing_report.get(
                    "metrics",
                    {}).get(
                        "avg_processing_time",
                        0),
                "operation_distribution": processing_report.get(
                    "metrics",
                    {}).get(
                    "operation_distribution",
                    {}),
                "performance_analysis": processing_report.get(
                    "performance_analysis",
                    {})}
        except Exception as e:
            return {"error": f"Processing overview error: {str(e)}"}

    def _get_ai_overview(
            self, ai_analytics_report: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI agent overview data"""
        try:
            return {
                "total_tasks": ai_analytics_report.get(
                    "total_tasks",
                    0),
                "success_rate": ai_analytics_report.get(
                    "metrics",
                    {}).get(
                    "success_rate",
                    0),
                "avg_completion_time": ai_analytics_report.get(
                    "metrics",
                    {}).get(
                        "avg_completion_time",
                        0),
                "agent_distribution": ai_analytics_report.get(
                    "metrics",
                    {}).get(
                    "agent_distribution",
                    {}),
                "agent_performance": ai_analytics_report.get(
                    "metrics",
                    {}).get(
                    "agent_performance",
                    {}),
                "efficiency_analysis": ai_analytics_report.get(
                    "efficiency_analysis",
                    {})}
        except Exception as e:
            return {"error": f"AI overview error: {str(e)}"}

    def _get_active_alerts(self,
                           system_metrics: Dict[str,
                                                Any],
                           security_analytics: Dict[str,
                                                    Any]) -> List[Dict[str,
                                                                       Any]]:
        """Get active alerts"""
        alerts = []

        # System alerts
        recent_alerts = system_metrics.get("recent_alerts", [])
        for alert in recent_alerts:
            alerts.append({
                "type": alert.get("type", "unknown"),
                "severity": alert.get("severity", "info"),
                "message": alert.get("message", ""),
                "timestamp": alert.get("timestamp", ""),
                "category": alert.get("category", "system")
            })

        # Security alerts
        if security_analytics.get("total_events_24h", 0) > 50:
            alerts.append({
                "type": "high_security_events",
                "severity": "warning",
"message": f"High security events: {security_analytics['total_events_24h']} in
    24h",
                "timestamp": datetime.now().isoformat(),
                "category": "security"
            })

        return alerts

    def _get_dashboard_recommendations(self,
                                       system_metrics: Dict[str,
                                                            Any],
                                       security_analytics: Dict[str,
                                                                Any],
                                       performance_report: Dict[str,
Any]) -> List[str]:
        """Get dashboard recommendations"""
        recommendations = []

        # System recommendations
        health_score = system_metrics.get("system_health", {}).get("score", 0)
        if health_score < 70:
            recommendations.append(
                "System health is poor - investigate issues immediately")

        # Security recommendations
        security_score = security_analytics.get("security_score", 0)
        if security_score < 80:
            recommendations.append(
                "Security score is low - review security measures")

        # Performance recommendations
        performance_recommendations = performance_report.get(
            "recommendations", [])
        # Top 3 recommendations
        recommendations.extend(performance_recommendations[:3])

        return recommendations

    def _get_overall_status(self,
                            system_metrics: Dict[str,
                                                 Any],
                            security_analytics: Dict[str,
                                                     Any]) -> Dict[str,
                                                                   Any]:
        """Get overall system status"""
        try:
            # Calculate overall status
            system_health = system_metrics.get(
                "system_health", {}).get(
                "score", 0)
            security_score = security_analytics.get("security_score", 0)

            # Weighted average (system health 60%, security 40%)
            overall_score = (system_health * 0.6) + (security_score * 0.4)

            # Determine status
            if overall_score >= 90:
                status = "excellent"
                color = "green"
            elif overall_score >= 70:
                status = "good"
                color = "blue"
            elif overall_score >= 50:
                status = "fair"
                color = "yellow"
            else:
                status = "poor"
                color = "red"

            return {
                "status": status,
                "score": round(overall_score, 1),
                "color": color,
                "last_updated": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "score": 0,
                "color": "red",
                "error": str(e)
            }

    def _calculate_threat_level(
            self, security_analytics: Dict[str, Any]) -> str:
        """Calculate threat level"""
        try:
            critical_events = security_analytics.get(
                "event_breakdown", {}).get("CRITICAL", 0)
            warning_events = security_analytics.get(
                "event_breakdown", {}).get("WARNING", 0)

            if critical_events > 5:
                return "high"
            elif critical_events > 0 or warning_events > 10:
                return "medium"
            else:
                return "low"

        except Exception:
            return "unknown"

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary for quick overview"""
        try:
            dashboard_data = self.get_comprehensive_dashboard_data()

            return {
                "overall_status": dashboard_data.get(
                    "status", {}), "system_health": dashboard_data.get(
                    "system_overview", {}).get(
                    "health_score", 0), "security_score": dashboard_data.get(
                    "security_overview", {}).get(
"security_score", 0), "performance_score": dashboard_data.get(
                            "performance_overview", {}).get(
                                "performance_score", 0), "active_alerts": len(
                                    dashboard_data.get(
"alerts", [])), "recommendations_count": len(
                                            dashboard_data.get(
"recommendations", [])), "last_updated": dashboard_data.get(
                                                    "timestamp", "")}

        except Exception as e:
            return {
                "error": f"Dashboard summary error: {str(e)}",
                "overall_status": {"status": "error", "score": 0}
            }

    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics for live dashboard"""
        try:
            # Get current system metrics
            system_metrics = enterprise_monitor.get_enterprise_dashboard_data()
            current_metrics = system_metrics.get("current_metrics", {})

            # Get current security status
            security_analytics = enterprise_security.get_security_analytics()

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": current_metrics.get(
                    "system",
                    {}).get(
                    "cpu",
                    {}).get(
                    "percent",
                    0),
                "memory_percent": current_metrics.get(
                    "system",
                    {}).get(
                        "memory",
                        {}).get(
                            "percent",
                            0),
                "disk_percent": current_metrics.get(
                    "system",
                    {}).get(
                    "disk",
                    {}).get(
                    "percent",
                    0),
                "active_sessions": security_analytics.get(
                    "active_sessions",
                    0),
                "blocked_ips": security_analytics.get(
                    "blocked_ips",
                    0),
                "security_events_24h": security_analytics.get(
                    "total_events_24h",
                    0),
                "system_health": system_metrics.get(
                    "system_health",
                    {}).get(
                    "status",
                    "unknown")}

        except Exception as e:
            return {
                "error": f"Real-time metrics error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def export_dashboard_report(
            self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Export dashboard report"""
        try:
            if report_type == "comprehensive":
                data = self.get_comprehensive_dashboard_data()
            elif report_type == "summary":
                data = self.get_dashboard_summary()
            elif report_type == "real_time":
                data = self.get_real_time_metrics()
            else:
                return {"error": f"Unknown report type: {report_type}"}

            return {
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "data": data,
                "export_format": "json"
            }

        except Exception as e:
            return {
                "error": f"Export error: {str(e)}",
                "report_type": report_type,
                "generated_at": datetime.now().isoformat()
            }


# Global enterprise dashboard instance
enterprise_dashboard = EnterpriseDashboard()
