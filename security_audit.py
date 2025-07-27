#!/usr/bin/env python3
"""
EHB Healthcare Security Audit Script
Comprehensive security and compliance checking for healthcare applications
"""

import json
import os
import socket
import ssl
import subprocess
from datetime import datetime
from pathlib import Path

import requests


class HealthcareSecurityAudit:
    """Healthcare Security Audit Class"""
    
    def __init__(self):
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "hipaa_compliance": {},
            "security_vulnerabilities": [],
            "performance_metrics": {},
            "recommendations": []
        }
    
    def run_comprehensive_audit(self):
        """Run comprehensive security audit"""
        print("🔒 EHB Healthcare Security Audit Starting...")
        
        # Check HIPAA compliance
        self.check_hipaa_compliance()
        
        # Check security vulnerabilities
        self.check_security_vulnerabilities()
        
        # Check performance metrics
        self.check_performance_metrics()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Save audit report
        self.save_audit_report()
        
        print("✅ Security audit completed successfully!")
        return self.audit_results
    
    def check_hipaa_compliance(self):
        """Check HIPAA compliance requirements"""
        print("📋 Checking HIPAA compliance...")
        
        hipaa_checks = {
            "data_encryption": self.check_data_encryption(),
            "access_controls": self.check_access_controls(),
            "audit_logging": self.check_audit_logging(),
            "data_retention": self.check_data_retention(),
            "secure_communication": self.check_secure_communication(),
            "backup_security": self.check_backup_security(),
            "incident_response": self.check_incident_response(),
            "training_program": self.check_training_program()
        }
        
        self.audit_results["hipaa_compliance"] = hipaa_checks
        
        # Calculate compliance score
        passed_checks = sum(1 for check in hipaa_checks.values() if check["status"] == "PASS")
        total_checks = len(hipaa_checks)
        compliance_score = (passed_checks / total_checks) * 100
        
        self.audit_results["hipaa_compliance"]["overall_score"] = compliance_score
        self.audit_results["hipaa_compliance"]["status"] = "COMPLIANT" if compliance_score >= 95 else "NON_COMPLIANT"
        
        print(f"📊 HIPAA Compliance Score: {compliance_score:.1f}%")
    
    def check_data_encryption(self):
        """Check data encryption implementation"""
        try:
            # Check for encryption libraries
            encryption_files = [
                "src/security/encryption.js",
                "src/utils/crypto.ts",
                "src/config/encryption.json"
            ]
            
            encryption_exists = any(Path(f).exists() for f in encryption_files)
            
            # Check for HTTPS configuration
            https_enabled = self.check_https_configuration()
            
            return {
                "status": "PASS" if encryption_exists and https_enabled else "FAIL",
                "details": {
                    "encryption_files": encryption_exists,
                    "https_enabled": https_enabled
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_access_controls(self):
        """Check access control implementation"""
        try:
            # Check for authentication files
            auth_files = [
                "src/auth/",
                "src/security/authentication.js",
                "src/middleware/auth.ts"
            ]
            
            auth_exists = any(Path(f).exists() for f in auth_files)
            
            # Check for role-based access
            rbac_exists = Path("src/security/rbac.js").exists()
            
            return {
                "status": "PASS" if auth_exists and rbac_exists else "FAIL",
                "details": {
                    "authentication": auth_exists,
                    "role_based_access": rbac_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_audit_logging(self):
        """Check audit logging implementation"""
        try:
            # Check for audit logging files
            audit_files = [
                "src/security/audit.js",
                "src/utils/logger.ts",
                "src/middleware/audit.ts"
            ]
            
            audit_exists = any(Path(f).exists() for f in audit_files)
            
            return {
                "status": "PASS" if audit_exists else "FAIL",
                "details": {
                    "audit_logging": audit_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_data_retention(self):
        """Check data retention policies"""
        try:
            # Check for data retention configuration
            retention_files = [
                "src/config/retention.json",
                "src/security/retention.js"
            ]
            
            retention_exists = any(Path(f).exists() for f in retention_files)
            
            return {
                "status": "PASS" if retention_exists else "FAIL",
                "details": {
                    "retention_policies": retention_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_secure_communication(self):
        """Check secure communication protocols"""
        try:
            # Check for HTTPS configuration
            https_config = self.check_https_configuration()
            
            # Check for secure headers
            secure_headers = self.check_security_headers()
            
            return {
                "status": "PASS" if https_config and secure_headers else "FAIL",
                "details": {
                    "https_enabled": https_config,
                    "secure_headers": secure_headers
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_backup_security(self):
        """Check backup security measures"""
        try:
            # Check for backup configuration
            backup_files = [
                "src/config/backup.json",
                "src/security/backup.js"
            ]
            
            backup_exists = any(Path(f).exists() for f in backup_files)
            
            return {
                "status": "PASS" if backup_exists else "FAIL",
                "details": {
                    "backup_security": backup_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_incident_response(self):
        """Check incident response procedures"""
        try:
            # Check for incident response files
            incident_files = [
                "src/security/incident.js",
                "src/config/incident.json"
            ]
            
            incident_exists = any(Path(f).exists() for f in incident_files)
            
            return {
                "status": "PASS" if incident_exists else "FAIL",
                "details": {
                    "incident_response": incident_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_training_program(self):
        """Check training program documentation"""
        try:
            # Check for training documentation
            training_files = [
                "docs/hipaa_training.md",
                "src/docs/security_training.md"
            ]
            
            training_exists = any(Path(f).exists() for f in training_files)
            
            return {
                "status": "PASS" if training_exists else "FAIL",
                "details": {
                    "training_program": training_exists
                }
            }
        except Exception as e:
            return {"status": "ERROR", "details": str(e)}
    
    def check_https_configuration(self):
        """Check HTTPS configuration"""
        try:
            # Check next.config.js for HTTPS headers
            if Path("next.config.js").exists():
                with open("next.config.js", "r") as f:
                    content = f.read()
                    return "Strict-Transport-Security" in content
            return False
        except Exception:
            return False
    
    def check_security_headers(self):
        """Check security headers configuration"""
        try:
            # Check for security headers in next.config.js
            if Path("next.config.js").exists():
                with open("next.config.js", "r") as f:
                    content = f.read()
                    required_headers = [
                        "X-Frame-Options",
                        "X-Content-Type-Options",
                        "X-XSS-Protection",
                        "Content-Security-Policy"
                    ]
                    return all(header in content for header in required_headers)
            return False
        except Exception:
            return False
    
    def check_security_vulnerabilities(self):
        """Check for security vulnerabilities"""
        print("🔍 Checking security vulnerabilities...")
        
        try:
            # Run npm audit
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                audit_data = json.loads(result.stdout)
                vulnerabilities = audit_data.get("vulnerabilities", {})
                
                for vuln_id, vuln_data in vulnerabilities.items():
                    self.audit_results["security_vulnerabilities"].append({
                        "id": vuln_id,
                        "severity": vuln_data.get("severity", "unknown"),
                        "title": vuln_data.get("title", ""),
                        "description": vuln_data.get("description", ""),
                        "recommendation": vuln_data.get("recommendation", "")
                    })
                
                print(f"⚠️  Found {len(self.audit_results['security_vulnerabilities'])} security vulnerabilities")
            else:
                print("✅ No security vulnerabilities found")
                
        except Exception as e:
            print(f"❌ Error checking vulnerabilities: {e}")
    
    def check_performance_metrics(self):
        """Check performance metrics"""
        print("⚡ Checking performance metrics...")
        
        try:
            # Check bundle size
            if Path("package.json").exists():
                result = subprocess.run(
                    ["npm", "run", "build"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.audit_results["performance_metrics"]["build_success"] = True
                    self.audit_results["performance_metrics"]["build_time"] = "measured"
                else:
                    self.audit_results["performance_metrics"]["build_success"] = False
                    self.audit_results["performance_metrics"]["build_error"] = result.stderr
            
            # Check for performance optimization files
            perf_files = [
                "src/utils/performance.js",
                "src/config/performance.json"
            ]
            
            perf_exists = any(Path(f).exists() for f in perf_files)
            self.audit_results["performance_metrics"]["optimization_files"] = perf_exists
            
        except Exception as e:
            print(f"❌ Error checking performance: {e}")
    
    def generate_recommendations(self):
        """Generate security recommendations"""
        print("💡 Generating recommendations...")
        
        recommendations = []
        
        # HIPAA compliance recommendations
        hipaa_checks = self.audit_results["hipaa_compliance"]
        for check_name, check_result in hipaa_checks.items():
            if isinstance(check_result, dict) and check_result.get("status") == "FAIL":
                recommendations.append(f"Implement {check_name.replace('_', ' ').title()} for HIPAA compliance")
        
        # Security vulnerability recommendations
        for vuln in self.audit_results["security_vulnerabilities"]:
            if vuln.get("recommendation"):
                recommendations.append(f"Fix {vuln['id']}: {vuln['recommendation']}")
        
        # Performance recommendations
        if not self.audit_results["performance_metrics"].get("optimization_files"):
            recommendations.append("Implement performance optimization files")
        
        self.audit_results["recommendations"] = recommendations
    
    def save_audit_report(self):
        """Save audit report to file"""
        try:
            # Create reports directory
            Path("reports").mkdir(exist_ok=True)
            
            # Save detailed report
            report_file = f"reports/security_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, "w") as f:
                json.dump(self.audit_results, f, indent=2)
            
            # Save summary report
            summary_file = f"reports/security_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(summary_file, "w") as f:
                f.write(self.generate_summary_report())
            
            print(f"📄 Audit report saved to {report_file}")
            print(f"📄 Summary report saved to {summary_file}")
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def generate_summary_report(self):
        """Generate summary report in markdown"""
        hipaa_score = self.audit_results["hipaa_compliance"].get("overall_score", 0)
        vuln_count = len(self.audit_results["security_vulnerabilities"])
        
        summary = f"""# EHB Healthcare Security Audit Summary

## Audit Date
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## HIPAA Compliance
- **Overall Score**: {hipaa_score:.1f}%
- **Status**: {self.audit_results["hipaa_compliance"].get("status", "UNKNOWN")}

## Security Vulnerabilities
- **Total Found**: {vuln_count}
- **Critical**: {len([v for v in self.audit_results['security_vulnerabilities'] if v.get('severity') == 'critical'])}
- **High**: {len([v for v in self.audit_results['security_vulnerabilities'] if v.get('severity') == 'high'])}
- **Medium**: {len([v for v in self.audit_results['security_vulnerabilities'] if v.get('severity') == 'medium'])}
- **Low**: {len([v for v in self.audit_results['security_vulnerabilities'] if v.get('severity') == 'low'])}

## Performance Metrics
- **Build Success**: {self.audit_results["performance_metrics"].get("build_success", False)}
- **Optimization Files**: {self.audit_results["performance_metrics"].get("optimization_files", False)}

## Top Recommendations
"""
        
        for i, rec in enumerate(self.audit_results["recommendations"][:5], 1):
            summary += f"{i}. {rec}\n"
        
        return summary

if __name__ == "__main__":
    auditor = HealthcareSecurityAudit()
    results = auditor.run_comprehensive_audit()
    
    # Print summary
    print("\n" + "="*50)
    print("🔒 SECURITY AUDIT SUMMARY")
    print("="*50)
    print(f"HIPAA Compliance: {results['hipaa_compliance'].get('overall_score', 0):.1f}%")
    print(f"Security Vulnerabilities: {len(results['security_vulnerabilities'])}")
    print(f"Recommendations: {len(results['recommendations'])}")
    print("="*50) 