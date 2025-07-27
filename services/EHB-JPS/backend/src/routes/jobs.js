const express = require('express');
const { body, validationResult } = require('express-validator');
const Job = require('../models/Job');
const Company = require('../models/Company');
const User = require('../models/User');

const router = express.Router();

// Validation middleware
const validateJobCreation = [
  body('title').notEmpty().trim(),
  body('description').notEmpty().trim(),
  body('location').notEmpty().trim(),
  body('jobType').isIn(['full-time', 'part-time', 'contract', 'internship']),
  body('experienceLevel').notEmpty().trim(),
  body('salaryMin').optional().isInt({ min: 0 }),
  body('salaryMax').optional().isInt({ min: 0 })
];

// Get all jobs with filters
router.get('/', async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      keyword,
      location,
      jobType,
      experienceLevel,
      salaryMin,
      salaryMax,
      companyId
    } = req.query;

    const offset = (page - 1) * limit;
    const where = { status: 'active' };

    // Add filters
    if (keyword) {
      const { Op } = require('sequelize');
      where[Op.or] = [
        { title: { [Op.like]: `%${keyword}%` } },
        { description: { [Op.like]: `%${keyword}%` } }
      ];
    }

    if (location) {
      const { Op } = require('sequelize');
      where.location = { [Op.like]: `%${location}%` };
    }

    if (jobType) {
      where.jobType = jobType;
    }

    if (experienceLevel) {
      where.experienceLevel = experienceLevel;
    }

    if (salaryMin) {
      const { Op } = require('sequelize');
      where.salaryMin = { [Op.gte]: parseInt(salaryMin) };
    }

    if (salaryMax) {
      const { Op } = require('sequelize');
      where.salaryMax = { [Op.lte]: parseInt(salaryMax) };
    }

    if (companyId) {
      where.companyId = companyId;
    }

    const jobs = await Job.findAndCountAll({
      where,
      include: [
        {
          model: Company,
          as: 'company',
          include: [
            {
              model: User,
              as: 'user',
              attributes: ['id', 'firstName', 'lastName', 'email']
            }
          ]
        }
      ],
      order: [['createdAt', 'DESC']],
      limit: parseInt(limit),
      offset: parseInt(offset)
    });

    res.json({
      success: true,
      data: {
        jobs: jobs.rows,
        pagination: {
          currentPage: parseInt(page),
          totalPages: Math.ceil(jobs.count / limit),
          totalJobs: jobs.count,
          jobsPerPage: parseInt(limit)
        }
      }
    });

  } catch (error) {
    console.error('Get jobs error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Get single job by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const job = await Job.findByPk(id, {
      include: [
        {
          model: Company,
          as: 'company',
          include: [
            {
              model: User,
              as: 'user',
              attributes: ['id', 'firstName', 'lastName', 'email']
            }
          ]
        }
      ]
    });

    if (!job) {
      return res.status(404).json({
        success: false,
        message: 'Job not found'
      });
    }

    // Increment views
    await job.update({ views: job.views + 1 });

    res.json({
      success: true,
      data: { job }
    });

  } catch (error) {
    console.error('Get job error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Create new job (company only)
router.post('/', validateJobCreation, async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    // Get user from token (you'll need to implement auth middleware)
    const userId = req.user?.id; // This will come from auth middleware
    if (!userId) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    // Check if user is a company
    const user = await User.findByPk(userId);
    if (user.userType !== 'company') {
      return res.status(403).json({
        success: false,
        message: 'Only companies can post jobs'
      });
    }

    // Get company
    const company = await Company.findOne({ where: { userId } });
    if (!company) {
      return res.status(400).json({
        success: false,
        message: 'Company profile not found'
      });
    }

    const jobData = {
      ...req.body,
      companyId: company.id,
      skills: req.body.skills || [],
      benefits: req.body.benefits || []
    };

    const job = await Job.create(jobData);

    res.status(201).json({
      success: true,
      message: 'Job created successfully',
      data: { job }
    });

  } catch (error) {
    console.error('Create job error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Update job (company only)
router.put('/:id', validateJobCreation, async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { id } = req.params;
    const userId = req.user?.id;

    // Get job
    const job = await Job.findByPk(id, {
      include: [
        {
          model: Company,
          as: 'company',
          where: { userId }
        }
      ]
    });

    if (!job) {
      return res.status(404).json({
        success: false,
        message: 'Job not found or access denied'
      });
    }

    // Update job
    await job.update(req.body);

    res.json({
      success: true,
      message: 'Job updated successfully',
      data: { job }
    });

  } catch (error) {
    console.error('Update job error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Delete job (company only)
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user?.id;

    // Get job
    const job = await Job.findByPk(id, {
      include: [
        {
          model: Company,
          as: 'company',
          where: { userId }
        }
      ]
    });

    if (!job) {
      return res.status(404).json({
        success: false,
        message: 'Job not found or access denied'
      });
    }

    // Soft delete by setting status to inactive
    await job.update({ status: 'inactive' });

    res.json({
      success: true,
      message: 'Job deleted successfully'
    });

  } catch (error) {
    console.error('Delete job error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Search jobs
router.get('/search', async (req, res) => {
  try {
    const { q, location, jobType, experienceLevel } = req.query;

    const where = { status: 'active' };

    if (q) {
      const { Op } = require('sequelize');
      where[Op.or] = [
        { title: { [Op.like]: `%${q}%` } },
        { description: { [Op.like]: `%${q}%` } },
        { requirements: { [Op.like]: `%${q}%` } }
      ];
    }

    if (location) {
      const { Op } = require('sequelize');
      where.location = { [Op.like]: `%${location}%` };
    }

    if (jobType) {
      where.jobType = jobType;
    }

    if (experienceLevel) {
      where.experienceLevel = experienceLevel;
    }

    const jobs = await Job.findAll({
      where,
      include: [
        {
          model: Company,
          as: 'company'
        }
      ],
      order: [['createdAt', 'DESC']],
      limit: 20
    });

    res.json({
      success: true,
      data: { jobs }
    });

  } catch (error) {
    console.error('Search jobs error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

module.exports = router;
