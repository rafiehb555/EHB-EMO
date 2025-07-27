const express = require('express');
const router = express.Router();

// AI Business Analysis Service for EMO Business Management
class BusinessAnalysisService {
  constructor() {
    this.analyses = new Map();
    this.businessProfiles = new Map();
  }

  async analyzeBusinessProfile(businessData) {
    try {
      const {
        businessType,
        industry,
        revenue,
        employeeCount,
        location,
        yearsInBusiness,
        documents
      } = businessData;

      // AI-powered business analysis
      const analysis = {
        businessId: businessData.businessId,
        riskAssessment: this.assessBusinessRisk(businessData),
        growthPotential: this.analyzeGrowthPotential(businessData),
        marketPosition: this.analyzeMarketPosition(businessData),
        financialHealth: this.analyzeFinancialHealth(businessData),
        recommendations: this.generateBusinessRecommendations(businessData),
        sqlLevel: this.recommendSQLLevel(businessData),
        timestamp: new Date().toISOString()
      };

      // Store analysis
      this.analyses.set(analysis.businessId, analysis);

      return {
        success: true,
        businessId: analysis.businessId,
        analysis,
        timestamp: analysis.timestamp
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  assessBusinessRisk(businessData) {
    const riskFactors = [];
    let riskScore = 0;

    // Financial risk assessment
    if (businessData.revenue < 50000) {
      riskFactors.push('low_revenue');
      riskScore += 20;
    }

    if (businessData.yearsInBusiness < 2) {
      riskFactors.push('new_business');
      riskScore += 15;
    }

    if (businessData.employeeCount < 5) {
      riskFactors.push('small_team');
      riskScore += 10;
    }

    // Industry risk assessment
    const highRiskIndustries = ['gambling', 'adult_entertainment', 'cryptocurrency'];
    if (highRiskIndustries.includes(businessData.industry.toLowerCase())) {
      riskFactors.push('high_risk_industry');
      riskScore += 30;
    }

    // Location risk assessment
    if (businessData.location.includes('offshore') || businessData.location.includes('tax_haven')) {
      riskFactors.push('offshore_location');
      riskScore += 25;
    }

    return {
      score: Math.min(riskScore, 100),
      level: riskScore < 30 ? 'low' : riskScore < 60 ? 'medium' : 'high',
      factors: riskFactors,
      recommendations: this.generateRiskMitigationRecommendations(riskFactors)
    };
  }

  analyzeGrowthPotential(businessData) {
    let growthScore = 0;
    const growthFactors = [];

    // Revenue growth potential
    if (businessData.revenue > 100000) {
      growthFactors.push('established_revenue');
      growthScore += 25;
    }

    // Market demand analysis
    const highGrowthIndustries = ['technology', 'healthcare', 'ecommerce', 'education'];
    if (highGrowthIndustries.includes(businessData.industry.toLowerCase())) {
      growthFactors.push('high_growth_industry');
      growthScore += 20;
    }

    // Team size and scalability
    if (businessData.employeeCount > 10) {
      growthFactors.push('scalable_team');
      growthScore += 15;
    }

    // Business maturity
    if (businessData.yearsInBusiness > 5) {
      growthFactors.push('mature_business');
      growthScore += 20;
    }

    return {
      score: Math.min(growthScore, 100),
      level: growthScore < 30 ? 'low' : growthScore < 60 ? 'medium' : 'high',
      factors: growthFactors
    };
  }

  analyzeMarketPosition(businessData) {
    const marketAnalysis = {
      competitiveAdvantage: this.assessCompetitiveAdvantage(businessData),
      marketShare: this.estimateMarketShare(businessData),
      customerBase: this.analyzeCustomerBase(businessData),
      brandStrength: this.assessBrandStrength(businessData)
    };

    return marketAnalysis;
  }

  assessCompetitiveAdvantage(businessData) {
    const advantages = [];

    if (businessData.yearsInBusiness > 10) {
      advantages.push('established_brand');
    }

    if (businessData.employeeCount > 50) {
      advantages.push('scale_efficiency');
    }

    if (businessData.revenue > 500000) {
      advantages.push('financial_strength');
    }

    if (businessData.industry === 'technology') {
      advantages.push('innovation_focus');
    }

    return {
      advantages,
      score: advantages.length * 25
    };
  }

  estimateMarketShare(businessData) {
    // Simplified market share estimation
    let marketShare = 0;

    if (businessData.revenue > 1000000) {
      marketShare = 15; // 15% market share
    } else if (businessData.revenue > 500000) {
      marketShare = 8; // 8% market share
    } else if (businessData.revenue > 100000) {
      marketShare = 3; // 3% market share
    } else {
      marketShare = 1; // 1% market share
    }

    return {
      percentage: marketShare,
      level: marketShare > 10 ? 'leader' : marketShare > 5 ? 'challenger' : 'niche'
    };
  }

  analyzeCustomerBase(businessData) {
    // Analyze customer base based on business type
    const customerAnalysis = {
      size: this.estimateCustomerSize(businessData),
      loyalty: this.assessCustomerLoyalty(businessData),
      growth: this.assessCustomerGrowth(businessData)
    };

    return customerAnalysis;
  }

  estimateCustomerSize(businessData) {
    // Simplified customer size estimation
    const revenuePerCustomer = {
      'retail': 100,
      'service': 500,
      'technology': 1000,
      'healthcare': 800,
      'education': 300
    };

    const avgRevenuePerCustomer = revenuePerCustomer[businessData.industry] || 200;
    const estimatedCustomers = Math.round(businessData.revenue / avgRevenuePerCustomer);

    return {
      count: estimatedCustomers,
      level: estimatedCustomers > 1000 ? 'large' : estimatedCustomers > 100 ? 'medium' : 'small'
    };
  }

  assessCustomerLoyalty(businessData) {
    // Simplified loyalty assessment
    let loyaltyScore = 50; // Base score

    if (businessData.yearsInBusiness > 5) {
      loyaltyScore += 20;
    }

    if (businessData.industry === 'healthcare' || businessData.industry === 'education') {
      loyaltyScore += 15;
    }

    if (businessData.revenue > 200000) {
      loyaltyScore += 15;
    }

    return {
      score: Math.min(loyaltyScore, 100),
      level: loyaltyScore > 80 ? 'high' : loyaltyScore > 60 ? 'medium' : 'low'
    };
  }

  assessCustomerGrowth(businessData) {
    // Simplified growth assessment
    const growthRate = businessData.revenue > 500000 ? 15 : businessData.revenue > 200000 ? 10 : 5;

    return {
      rate: growthRate,
      trend: growthRate > 10 ? 'accelerating' : growthRate > 5 ? 'stable' : 'declining'
    };
  }

  assessBrandStrength(businessData) {
    let brandScore = 0;
    const brandFactors = [];

    if (businessData.yearsInBusiness > 10) {
      brandFactors.push('longevity');
      brandScore += 25;
    }

    if (businessData.revenue > 500000) {
      brandFactors.push('financial_success');
      brandScore += 25;
    }

    if (businessData.employeeCount > 20) {
      brandFactors.push('scale');
      brandScore += 20;
    }

    if (businessData.industry === 'technology' || businessData.industry === 'healthcare') {
      brandFactors.push('industry_reputation');
      brandScore += 15;
    }

    return {
      score: Math.min(brandScore, 100),
      level: brandScore > 70 ? 'strong' : brandScore > 40 ? 'moderate' : 'developing',
      factors: brandFactors
    };
  }

  analyzeFinancialHealth(businessData) {
    const financialAnalysis = {
      revenueStability: this.assessRevenueStability(businessData),
      profitability: this.assessProfitability(businessData),
      cashFlow: this.assessCashFlow(businessData),
      debtLevel: this.assessDebtLevel(businessData)
    };

    return financialAnalysis;
  }

  assessRevenueStability(businessData) {
    // Simplified revenue stability assessment
    let stabilityScore = 50;

    if (businessData.yearsInBusiness > 5) {
      stabilityScore += 20;
    }

    if (businessData.revenue > 200000) {
      stabilityScore += 20;
    }

    if (businessData.industry === 'healthcare' || businessData.industry === 'education') {
      stabilityScore += 10;
    }

    return {
      score: Math.min(stabilityScore, 100),
      level: stabilityScore > 80 ? 'high' : stabilityScore > 60 ? 'medium' : 'low'
    };
  }

  assessProfitability(businessData) {
    // Simplified profitability assessment
    const estimatedProfitMargin = businessData.industry === 'technology' ? 25 : 
                                 businessData.industry === 'healthcare' ? 20 :
                                 businessData.industry === 'service' ? 15 : 10;

    return {
      margin: estimatedProfitMargin,
      level: estimatedProfitMargin > 20 ? 'high' : estimatedProfitMargin > 10 ? 'medium' : 'low'
    };
  }

  assessCashFlow(businessData) {
    // Simplified cash flow assessment
    const cashFlowScore = businessData.revenue > 300000 ? 80 : 
                         businessData.revenue > 100000 ? 60 : 40;

    return {
      score: cashFlowScore,
      level: cashFlowScore > 70 ? 'strong' : cashFlowScore > 50 ? 'adequate' : 'weak'
    };
  }

  assessDebtLevel(businessData) {
    // Simplified debt assessment
    const debtLevel = businessData.revenue > 500000 ? 'low' : 
                     businessData.revenue > 200000 ? 'moderate' : 'high';

    return {
      level: debtLevel,
      risk: debtLevel === 'high' ? 'elevated' : debtLevel === 'moderate' ? 'moderate' : 'low'
    };
  }

  generateBusinessRecommendations(businessData) {
    const recommendations = [];

    // Risk mitigation recommendations
    if (businessData.revenue < 100000) {
      recommendations.push('Focus on revenue growth to improve business stability');
    }

    if (businessData.yearsInBusiness < 3) {
      recommendations.push('Build track record and establish market presence');
    }

    if (businessData.employeeCount < 10) {
      recommendations.push('Consider expanding team for better scalability');
    }

    // Growth recommendations
    if (businessData.industry === 'technology') {
      recommendations.push('Leverage technology trends for market expansion');
    }

    if (businessData.revenue > 200000) {
      recommendations.push('Consider diversification and new market entry');
    }

    return recommendations;
  }

  recommendSQLLevel(businessData) {
    let sqlLevel = 'Free';

    // SQL level recommendation based on business metrics
    if (businessData.revenue > 1000000 && businessData.yearsInBusiness > 5) {
      sqlLevel = 'VIP';
    } else if (businessData.revenue > 500000 && businessData.yearsInBusiness > 3) {
      sqlLevel = 'High';
    } else if (businessData.revenue > 200000 && businessData.yearsInBusiness > 2) {
      sqlLevel = 'Normal';
    } else if (businessData.revenue > 50000) {
      sqlLevel = 'Basic';
    }

    return {
      recommendedLevel: sqlLevel,
      reasoning: this.getSQLLevelReasoning(businessData, sqlLevel),
      upgradePath: this.getUpgradePath(businessData, sqlLevel)
    };
  }

  getSQLLevelReasoning(businessData, level) {
    const reasoning = {
      'VIP': 'High revenue and established business with strong market position',
      'High': 'Strong revenue and business maturity with growth potential',
      'Normal': 'Stable business with moderate revenue and market presence',
      'Basic': 'Developing business with potential for growth',
      'Free': 'New or small business requiring support and growth'
    };

    return reasoning[level] || 'Standard business profile';
  }

  getUpgradePath(businessData, currentLevel) {
    const upgradePaths = {
      'Free': { nextLevel: 'Basic', requirements: 'Revenue > $50K, 1+ year in business' },
      'Basic': { nextLevel: 'Normal', requirements: 'Revenue > $200K, 2+ years in business' },
      'Normal': { nextLevel: 'High', requirements: 'Revenue > $500K, 3+ years in business' },
      'High': { nextLevel: 'VIP', requirements: 'Revenue > $1M, 5+ years in business' },
      'VIP': { nextLevel: 'Maximum', requirements: 'Already at maximum level' }
    };

    return upgradePaths[currentLevel] || { nextLevel: 'N/A', requirements: 'N/A' };
  }

  generateRiskMitigationRecommendations(riskFactors) {
    const recommendations = [];

    if (riskFactors.includes('low_revenue')) {
      recommendations.push('Implement revenue growth strategies and diversify income streams');
    }

    if (riskFactors.includes('new_business')) {
      recommendations.push('Build business track record and establish market credibility');
    }

    if (riskFactors.includes('small_team')) {
      recommendations.push('Consider team expansion for better operational capacity');
    }

    if (riskFactors.includes('high_risk_industry')) {
      recommendations.push('Implement additional compliance and risk management measures');
    }

    if (riskFactors.includes('offshore_location')) {
      recommendations.push('Ensure proper regulatory compliance and transparency measures');
    }

    return recommendations;
  }
}

const businessAnalysisService = new BusinessAnalysisService();

// Routes
router.post('/analyze', async (req, res) => {
  try {
    const { businessData } = req.body;
    
    if (!businessData || !businessData.businessId) {
      return res.status(400).json({
        success: false,
        error: 'Business data and businessId are required'
      });
    }

    const result = await businessAnalysisService.analyzeBusinessProfile(businessData);
    
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

router.get('/analysis/:businessId', async (req, res) => {
  try {
    const { businessId } = req.params;
    
    const analysis = businessAnalysisService.analyses.get(businessId);
    
    if (!analysis) {
      return res.status(404).json({
        success: false,
        error: 'Business analysis not found'
      });
    }

    res.json({
      success: true,
      data: analysis,
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