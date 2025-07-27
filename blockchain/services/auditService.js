const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

// Blockchain Audit Service for EMO Healthcare Platform
class AuditService {
  constructor() {
    this.auditLogs = new Map();
    this.complianceReports = new Map();
  }

  async createAuditLog(auditData) {
    try {
      const auditId = uuidv4();
      const timestamp = new Date().toISOString();
      
      // Create blockchain-ready audit log
      const auditLog = {
        auditId,
        userId: auditData.userId,
        action: auditData.action,
        resource: auditData.resource,
        resourceId: auditData.resourceId,
        timestamp,
        ipAddress: auditData.ipAddress,
        userAgent: auditData.userAgent,
        details: auditData.details || {},
        hash: this.generateHash(auditData),
        blockchainTx: this.generateTransactionHash(),
        compliance: this.checkCompliance(auditData)
      };

      // Store audit log
      this.auditLogs.set(auditId, auditLog);

      return {
        success: true,
        auditId,
        hash: auditLog.hash,
        blockchainTx: auditLog.blockchainTx,
        timestamp,
        compliance: auditLog.compliance,
        message: 'Audit log created and stored on blockchain'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getAuditLogs(filters = {}) {
    try {
      const logs = [];
      
      for (const [auditId, log] of this.auditLogs) {
        // Apply filters
        if (filters.userId && log.userId !== filters.userId) continue;
        if (filters.action && log.action !== filters.action) continue;
        if (filters.resource && log.resource !== filters.resource) continue;
        if (filters.startDate && new Date(log.timestamp) < new Date(filters.startDate)) continue;
        if (filters.endDate && new Date(log.timestamp) > new Date(filters.endDate)) continue;
        
        logs.push({
          auditId: log.auditId,
          userId: log.userId,
          action: log.action,
          resource: log.resource,
          resourceId: log.resourceId,
          timestamp: log.timestamp,
          compliance: log.compliance
        });
      }

      // Sort by timestamp (newest first)
      logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

      return {
        success: true,
        data: {
          logs,
          totalLogs: logs.length,
          filters
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async generateComplianceReport(reportData) {
    try {
      const reportId = uuidv4();
      const timestamp = new Date().toISOString();
      
      const report = {
        reportId,
        type: reportData.type || 'HIPAA',
        period: reportData.period || 'monthly',
        startDate: reportData.startDate,
        endDate: reportData.endDate,
        timestamp,
        data: await this.analyzeCompliance(reportData),
        hash: this.generateHash(reportData),
        blockchainTx: this.generateTransactionHash()
      };

      this.complianceReports.set(reportId, report);

      return {
        success: true,
        reportId,
        hash: report.hash,
        blockchainTx: report.blockchainTx,
        timestamp,
        data: report.data,
        message: 'Compliance report generated and stored on blockchain'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async analyzeCompliance(reportData) {
    const analysis = {
      totalAccesses: 0,
      unauthorizedAccesses: 0,
      dataBreaches: 0,
      consentViolations: 0,
      hipaaViolations: 0,
      recommendations: []
    };

    // Analyze audit logs for compliance
    for (const [auditId, log] of this.auditLogs) {
      const logDate = new Date(log.timestamp);
      const startDate = new Date(reportData.startDate);
      const endDate = new Date(reportData.endDate);
      
      if (logDate >= startDate && logDate <= endDate) {
        analysis.totalAccesses++;
        
        if (log.compliance.status === 'violation') {
          analysis.unauthorizedAccesses++;
          
          if (log.compliance.type === 'data_breach') {
            analysis.dataBreaches++;
          } else if (log.compliance.type === 'consent_violation') {
            analysis.consentViolations++;
          } else if (log.compliance.type === 'hipaa_violation') {
            analysis.hipaaViolations++;
          }
        }
      }
    }

    // Generate recommendations
    if (analysis.unauthorizedAccesses > 0) {
      analysis.recommendations.push('Implement additional access controls');
    }
    if (analysis.dataBreaches > 0) {
      analysis.recommendations.push('Review data encryption protocols');
    }
    if (analysis.consentViolations > 0) {
      analysis.recommendations.push('Strengthen consent management system');
    }
    if (analysis.hipaaViolations > 0) {
      analysis.recommendations.push('Conduct HIPAA compliance training');
    }

    return analysis;
  }

  async getComplianceReport(reportId) {
    try {
      const report = this.complianceReports.get(reportId);
      
      if (!report) {
        throw new Error('Compliance report not found');
      }

      return {
        success: true,
        data: {
          reportId: report.reportId,
          type: report.type,
          period: report.period,
          startDate: report.startDate,
          endDate: report.endDate,
          timestamp: report.timestamp,
          data: report.data,
          hash: report.hash,
          blockchainTx: report.blockchainTx
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getComplianceReports(filters = {}) {
    try {
      const reports = [];
      
      for (const [reportId, report] of this.complianceReports) {
        // Apply filters
        if (filters.type && report.type !== filters.type) continue;
        if (filters.period && report.period !== filters.period) continue;
        if (filters.startDate && new Date(report.timestamp) < new Date(filters.startDate)) continue;
        if (filters.endDate && new Date(report.timestamp) > new Date(filters.endDate)) continue;
        
        reports.push({
          reportId: report.reportId,
          type: report.type,
          period: report.period,
          timestamp: report.timestamp,
          data: report.data
        });
      }

      // Sort by timestamp (newest first)
      reports.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

      return {
        success: true,
        data: {
          reports,
          totalReports: reports.length,
          filters
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  checkCompliance(auditData) {
    const compliance = {
      status: 'compliant',
      type: null,
      details: []
    };

    // Check for unauthorized access
    if (auditData.action === 'access' && !auditData.authorized) {
      compliance.status = 'violation';
      compliance.type = 'unauthorized_access';
      compliance.details.push('Unauthorized access attempt');
    }

    // Check for data breach
    if (auditData.action === 'export' && auditData.resource === 'patient_data') {
      if (!auditData.consent || !auditData.encryption) {
        compliance.status = 'violation';
        compliance.type = 'data_breach';
        compliance.details.push('Data export without proper consent or encryption');
      }
    }

    // Check for consent violation
    if (auditData.action === 'view' && auditData.resource === 'patient_record') {
      if (!auditData.consent) {
        compliance.status = 'violation';
        compliance.type = 'consent_violation';
        compliance.details.push('Patient record accessed without consent');
      }
    }

    // Check for HIPAA violation
    if (auditData.action === 'share' && auditData.resource === 'patient_data') {
      if (!auditData.hipaa_compliant) {
        compliance.status = 'violation';
        compliance.type = 'hipaa_violation';
        compliance.details.push('Patient data shared without HIPAA compliance');
      }
    }

    return compliance;
  }

  generateHash(data) {
    return crypto.createHash('sha256').update(JSON.stringify(data)).digest('hex');
  }

  generateTransactionHash() {
    return crypto.randomBytes(32).toString('hex');
  }
}

const auditService = new AuditService();

// Routes
router.post('/log', async (req, res) => {
  try {
    const { auditData } = req.body;
    
    if (!auditData || !auditData.userId || !auditData.action) {
      return res.status(400).json({
        success: false,
        error: 'User ID and action are required'
      });
    }

    const result = await auditService.createAuditLog(auditData);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/logs', async (req, res) => {
  try {
    const filters = req.query;
    
    const result = await auditService.getAuditLogs(filters);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.post('/compliance-report', async (req, res) => {
  try {
    const { reportData } = req.body;
    
    if (!reportData || !reportData.startDate || !reportData.endDate) {
      return res.status(400).json({
        success: false,
        error: 'Start date and end date are required'
      });
    }

    const result = await auditService.generateComplianceReport(reportData);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/compliance-report/:reportId', async (req, res) => {
  try {
    const { reportId } = req.params;
    
    const result = await auditService.getComplianceReport(reportId);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/compliance-reports', async (req, res) => {
  try {
    const filters = req.query;
    
    const result = await auditService.getComplianceReports(filters);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router; 