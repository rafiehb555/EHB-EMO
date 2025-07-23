const express = require('express');
const { body, validationResult } = require('express-validator');
const Job = require('../models/Job');
const Company = require('../models/Company');
const Application = require('../models/Application');
const router = express.Router();

// Validation middleware
const validateJobCreation = [
    body('title').trim().isLength({ min: 3, max: 255 }),
    body('description').trim().isLength({ min: 10 }),
    body('company_id').isInt(),
    body('job_type').isIn(['full-time', 'part-time', 'contract', 'internship']),
    body('location').optional().trim(),
    body('salary_min').optional().isInt({ min: 0 }),
    body('salary_max').optional().isInt({ min: 0 }),
    body('skills').optional().isArray(),
    body('application_deadline').optional().isISO8601()
];

const validateJobUpdate = [
    body('title').optional().trim().isLength({ min: 3, max: 255 }),
    body('description').optional().trim().isLength({ min: 10 }),
    body('job_type').optional().isIn(['full-time', 'part-time', 'contract', 'internship']),
    body('status').optional().isIn(['active', 'inactive', 'filled', 'expired'])
];

// @route   GET /api/jobs
// @desc    Get all jobs with pagination and filters
// @access  Public
router.get('/', async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            keyword,
            location,
            job_type,
            salary_min,
            salary_max,
            company_id,
            is_remote,
            is_featured
        } = req.query;

        const offset = (page - 1) * limit;
        const where = { status: 'active' };

        // Apply filters
        if (keyword) {
            where[sequelize.Op.or] = [
                { title: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { description: { [sequelize.Op.iLike]: `%${keyword}%` } }
            ];
        }

        if (location) {
            where.location = { [sequelize.Op.iLike]: `%${location}%` };
        }

        if (job_type) {
            where.job_type = job_type;
        }

        if (salary_min) {
            where.salary_min = { [sequelize.Op.gte]: parseInt(salary_min) };
        }

        if (salary_max) {
            where.salary_max = { [sequelize.Op.lte]: parseInt(salary_max) };
        }

        if (company_id) {
            where.company_id = parseInt(company_id);
        }

        if (is_remote !== undefined) {
            where.is_remote = is_remote === 'true';
        }

        if (is_featured !== undefined) {
            where.is_featured = is_featured === 'true';
        }

        const { count, rows } = await Job.findAndCountAll({
            where,
            include: [
                {
                    model: Company,
                    as: 'company',
                    attributes: ['id', 'company_name', 'logo_url', 'location', 'industry']
                }
            ],
            order: [['created_at', 'DESC']],
            limit: parseInt(limit),
            offset: parseInt(offset)
        });

        res.json({
            success: true,
            data: {
                jobs: rows,
                pagination: {
                    current_page: parseInt(page),
                    total_pages: Math.ceil(count / limit),
                    total_items: count,
                    items_per_page: parseInt(limit)
                }
            }
        });

    } catch (error) {
        console.error('Get jobs error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching jobs'
        });
    }
});

// @route   GET /api/jobs/:id
// @desc    Get job by ID
// @access  Public
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const job = await Job.findByPk(id, {
            include: [
                {
                    model: Company,
                    as: 'company',
                    attributes: ['id', 'company_name', 'logo_url', 'location', 'industry', 'description', 'website']
                }
            ]
        });

        if (!job) {
            return res.status(404).json({
                success: false,
                message: 'Job not found'
            });
        }

        // Increment view count
        await job.incrementViews();

        res.json({
            success: true,
            data: { job }
        });

    } catch (error) {
        console.error('Get job error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching job'
        });
    }
});

// @route   POST /api/jobs
// @desc    Create a new job
// @access  Private (Company only)
router.post('/', validateJobCreation, async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({
                success: false,
                message: 'Validation failed',
                errors: errors.array()
            });
        }

        const {
            title,
            description,
            requirements,
            company_id,
            salary_min,
            salary_max,
            location,
            job_type,
            experience_level,
            skills,
            is_remote,
            application_deadline,
            tags
        } = req.body;

        // Verify company exists and user has permission
        const company = await Company.findByPk(company_id);
        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found'
            });
        }

        const job = await Job.create({
            title,
            description,
            requirements,
            company_id,
            salary_min: salary_min ? parseInt(salary_min) : null,
            salary_max: salary_max ? parseInt(salary_max) : null,
            location,
            job_type,
            experience_level,
            skills: skills || [],
            is_remote: is_remote || false,
            application_deadline: application_deadline ? new Date(application_deadline) : null,
            tags: tags || []
        });

        res.status(201).json({
            success: true,
            message: 'Job created successfully',
            data: { job }
        });

    } catch (error) {
        console.error('Create job error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while creating job'
        });
    }
});

// @route   PUT /api/jobs/:id
// @desc    Update job
// @access  Private (Company only)
router.put('/:id', validateJobUpdate, async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({
                success: false,
                message: 'Validation failed',
                errors: errors.array()
            });
        }

        const { id } = req.params;
        const updateData = req.body;

        const job = await Job.findByPk(id);
        if (!job) {
            return res.status(404).json({
                success: false,
                message: 'Job not found'
            });
        }

        // Update job
        await job.update(updateData);

        res.json({
            success: true,
            message: 'Job updated successfully',
            data: { job }
        });

    } catch (error) {
        console.error('Update job error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while updating job'
        });
    }
});

// @route   DELETE /api/jobs/:id
// @desc    Delete job
// @access  Private (Company only)
router.delete('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const job = await Job.findByPk(id);
        if (!job) {
            return res.status(404).json({
                success: false,
                message: 'Job not found'
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
            message: 'Server error while deleting job'
        });
    }
});

// @route   GET /api/jobs/:id/applications
// @desc    Get applications for a job
// @access  Private (Company only)
router.get('/:id/applications', async (req, res) => {
    try {
        const { id } = req.params;
        const { page = 1, limit = 10, status } = req.query;

        const offset = (page - 1) * limit;
        const where = { job_id: id };

        if (status) {
            where.status = status;
        }

        const { count, rows } = await Application.findAndCountAll({
            where,
            include: [
                {
                    model: require('../models/User'),
                    as: 'user',
                    attributes: ['id', 'first_name', 'last_name', 'email', 'profile_image']
                }
            ],
            order: [['applied_at', 'DESC']],
            limit: parseInt(limit),
            offset: parseInt(offset)
        });

        res.json({
            success: true,
            data: {
                applications: rows,
                pagination: {
                    current_page: parseInt(page),
                    total_pages: Math.ceil(count / limit),
                    total_items: count,
                    items_per_page: parseInt(limit)
                }
            }
        });

    } catch (error) {
        console.error('Get applications error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching applications'
        });
    }
});

// @route   GET /api/jobs/search/suggestions
// @desc    Get job search suggestions
// @access  Public
router.get('/search/suggestions', async (req, res) => {
    try {
        const { keyword } = req.query;

        if (!keyword || keyword.length < 2) {
            return res.json({
                success: true,
                data: { suggestions: [] }
            });
        }

        const suggestions = await Job.findAll({
            where: {
                status: 'active',
                title: { [sequelize.Op.iLike]: `%${keyword}%` }
            },
            attributes: ['title'],
            group: ['title'],
            limit: 10
        });

        res.json({
            success: true,
            data: {
                suggestions: suggestions.map(s => s.title)
            }
        });

    } catch (error) {
        console.error('Search suggestions error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching suggestions'
        });
    }
});

// @route   GET /api/jobs/featured
// @desc    Get featured jobs
// @access  Public
router.get('/featured', async (req, res) => {
    try {
        const featuredJobs = await Job.findAll({
            where: {
                status: 'active',
                is_featured: true
            },
            include: [
                {
                    model: Company,
                    as: 'company',
                    attributes: ['id', 'company_name', 'logo_url', 'location']
                }
            ],
            order: [['created_at', 'DESC']],
            limit: 10
        });

        res.json({
            success: true,
            data: { jobs: featuredJobs }
        });

    } catch (error) {
        console.error('Get featured jobs error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching featured jobs'
        });
    }
});

module.exports = router;
