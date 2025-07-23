const express = require('express');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const Job = require('../models/Job');
const Company = require('../models/Company');
const Application = require('../models/Application');
const auth = require('../middleware/auth');
const router = express.Router();

// Admin middleware - check if user is admin
const adminAuth = (req, res, next) => {
    if (req.user.user_type !== 'admin') {
        return res.status(403).json({
            success: false,
            message: 'Access denied. Admin only.'
        });
    }
    next();
};

// Validation middleware
const validateUserUpdate = [
    body('first_name').optional().trim().isLength({ min: 2 }),
    body('last_name').optional().trim().isLength({ min: 2 }),
    body('email').optional().isEmail(),
    body('user_type').optional().isIn(['jobseeker', 'company', 'admin']),
    body('is_active').optional().isBoolean(),
    body('is_verified').optional().isBoolean()
];

// @route   GET /api/admin/dashboard
// @desc    Get admin dashboard statistics
// @access  Private (Admin)
router.get('/dashboard', auth, adminAuth, async (req, res) => {
    try {
        // Get total counts
        const totalUsers = await User.count();
        const totalJobs = await Job.count();
        const totalCompanies = await Company.count();
        const totalApplications = await Application.count();

        // Get active counts
        const activeUsers = await User.count({ where: { is_active: true } });
        const activeJobs = await Job.count({ where: { status: 'active' } });
        const activeCompanies = await Company.count({ where: { is_active: true } });

        // Get user type distribution
        const userTypes = await User.findAll({
            attributes: [
                'user_type',
                [sequelize.fn('COUNT', sequelize.col('id')), 'count']
            ],
            group: ['user_type']
        });

        // Get recent activities
        const recentUsers = await User.findAll({
            order: [['created_at', 'DESC']],
            limit: 5,
            attributes: ['id', 'first_name', 'last_name', 'email', 'user_type', 'created_at']
        });

        const recentJobs = await Job.findAll({
            order: [['created_at', 'DESC']],
            limit: 5,
            include: [
                {
                    model: Company,
                    as: 'company',
                    attributes: ['company_name']
                }
            ]
        });

        const recentApplications = await Application.findAll({
            order: [['applied_at', 'DESC']],
            limit: 5,
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['first_name', 'last_name']
                },
                {
                    model: Job,
                    as: 'job',
                    attributes: ['title']
                }
            ]
        });

        res.json({
            success: true,
            data: {
                stats: {
                    total_users: totalUsers,
                    total_jobs: totalJobs,
                    total_companies: totalCompanies,
                    total_applications: totalApplications,
                    active_users: activeUsers,
                    active_jobs: activeJobs,
                    active_companies: activeCompanies
                },
                user_types: userTypes,
                recent_users: recentUsers,
                recent_jobs: recentJobs,
                recent_applications: recentApplications
            }
        });

    } catch (error) {
        console.error('Get admin dashboard error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching dashboard data'
        });
    }
});

// @route   GET /api/admin/users
// @desc    Get all users with pagination and filters
// @access  Private (Admin)
router.get('/users', auth, adminAuth, async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            user_type,
            is_active,
            is_verified,
            keyword
        } = req.query;

        const offset = (page - 1) * limit;
        const where = {};

        // Apply filters
        if (user_type) {
            where.user_type = user_type;
        }

        if (is_active !== undefined) {
            where.is_active = is_active === 'true';
        }

        if (is_verified !== undefined) {
            where.is_verified = is_verified === 'true';
        }

        if (keyword) {
            where[sequelize.Op.or] = [
                { first_name: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { last_name: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { email: { [sequelize.Op.iLike]: `%${keyword}%` } }
            ];
        }

        const { count, rows } = await User.findAndCountAll({
            where,
            order: [['created_at', 'DESC']],
            limit: parseInt(limit),
            offset: parseInt(offset)
        });

        res.json({
            success: true,
            data: {
                users: rows,
                pagination: {
                    current_page: parseInt(page),
                    total_pages: Math.ceil(count / limit),
                    total_items: count,
                    items_per_page: parseInt(limit)
                }
            }
        });

    } catch (error) {
        console.error('Get users error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching users'
        });
    }
});

// @route   GET /api/admin/users/:id
// @desc    Get user by ID
// @access  Private (Admin)
router.get('/users/:id', auth, adminAuth, async (req, res) => {
    try {
        const { id } = req.params;

        const user = await User.findByPk(id, {
            include: [
                {
                    model: Company,
                    as: 'company'
                },
                {
                    model: Application,
                    as: 'applications',
                    include: [
                        {
                            model: Job,
                            as: 'job',
                            include: [
                                {
                                    model: Company,
                                    as: 'company',
                                    attributes: ['company_name']
                                }
                            ]
                        }
                    ]
                }
            ]
        });

        if (!user) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }

        res.json({
            success: true,
            data: { user }
        });

    } catch (error) {
        console.error('Get user error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching user'
        });
    }
});

// @route   PUT /api/admin/users/:id
// @desc    Update user
// @access  Private (Admin)
router.put('/users/:id', auth, adminAuth, validateUserUpdate, async (req, res) => {
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

        const user = await User.findByPk(id);
        if (!user) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }

        await user.update(updateData);

        res.json({
            success: true,
            message: 'User updated successfully',
            data: { user }
        });

    } catch (error) {
        console.error('Update user error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while updating user'
        });
    }
});

// @route   DELETE /api/admin/users/:id
// @desc    Delete user
// @access  Private (Admin)
router.delete('/users/:id', auth, adminAuth, async (req, res) => {
    try {
        const { id } = req.params;

        const user = await User.findByPk(id);
        if (!user) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }

        // Soft delete by setting is_active to false
        await user.update({ is_active: false });

        res.json({
            success: true,
            message: 'User deleted successfully'
        });

    } catch (error) {
        console.error('Delete user error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while deleting user'
        });
    }
});

// @route   GET /api/admin/jobs
// @desc    Get all jobs with pagination and filters
// @access  Private (Admin)
router.get('/jobs', auth, adminAuth, async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            status,
            company_id,
            keyword
        } = req.query;

        const offset = (page - 1) * limit;
        const where = {};

        // Apply filters
        if (status) {
            where.status = status;
        }

        if (company_id) {
            where.company_id = parseInt(company_id);
        }

        if (keyword) {
            where[sequelize.Op.or] = [
                { title: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { description: { [sequelize.Op.iLike]: `%${keyword}%` } }
            ];
        }

        const { count, rows } = await Job.findAndCountAll({
            where,
            include: [
                {
                    model: Company,
                    as: 'company',
                    attributes: ['id', 'company_name', 'logo_url']
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

// @route   PUT /api/admin/jobs/:id
// @desc    Update job status
// @access  Private (Admin)
router.put('/jobs/:id', auth, adminAuth, [
    body('status').isIn(['active', 'inactive', 'filled', 'expired']),
    body('is_featured').optional().isBoolean()
], async (req, res) => {
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
        const { status, is_featured } = req.body;

        const job = await Job.findByPk(id);
        if (!job) {
            return res.status(404).json({
                success: false,
                message: 'Job not found'
            });
        }

        await job.update({ status, is_featured });

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

// @route   GET /api/admin/companies
// @desc    Get all companies with pagination and filters
// @access  Private (Admin)
router.get('/companies', auth, adminAuth, async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            is_verified,
            is_active,
            industry,
            keyword
        } = req.query;

        const offset = (page - 1) * limit;
        const where = {};

        // Apply filters
        if (is_verified !== undefined) {
            where.is_verified = is_verified === 'true';
        }

        if (is_active !== undefined) {
            where.is_active = is_active === 'true';
        }

        if (industry) {
            where.industry = { [sequelize.Op.iLike]: `%${industry}%` };
        }

        if (keyword) {
            where[sequelize.Op.or] = [
                { company_name: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { description: { [sequelize.Op.iLike]: `%${keyword}%` } }
            ];
        }

        const { count, rows } = await Company.findAndCountAll({
            where,
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['id', 'first_name', 'last_name', 'email']
                }
            ],
            order: [['created_at', 'DESC']],
            limit: parseInt(limit),
            offset: parseInt(offset)
        });

        res.json({
            success: true,
            data: {
                companies: rows,
                pagination: {
                    current_page: parseInt(page),
                    total_pages: Math.ceil(count / limit),
                    total_items: count,
                    items_per_page: parseInt(limit)
                }
            }
        });

    } catch (error) {
        console.error('Get companies error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching companies'
        });
    }
});

// @route   PUT /api/admin/companies/:id/verify
// @desc    Verify company
// @access  Private (Admin)
router.put('/companies/:id/verify', auth, adminAuth, async (req, res) => {
    try {
        const { id } = req.params;

        const company = await Company.findByPk(id);
        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found'
            });
        }

        await company.update({ is_verified: true });

        res.json({
            success: true,
            message: 'Company verified successfully',
            data: { company }
        });

    } catch (error) {
        console.error('Verify company error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while verifying company'
        });
    }
});

// @route   GET /api/admin/system/health
// @desc    Get system health information
// @access  Private (Admin)
router.get('/system/health', auth, adminAuth, async (req, res) => {
    try {
        const healthInfo = {
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
            memory: process.memoryUsage(),
            cpu: process.cpuUsage(),
            environment: process.env.NODE_ENV || 'development',
            database: {
                connected: true, // TODO: Add actual DB connection check
                tables: {
                    users: await User.count(),
                    jobs: await Job.count(),
                    companies: await Company.count(),
                    applications: await Application.count()
                }
            }
        };

        res.json({
            success: true,
            data: healthInfo
        });

    } catch (error) {
        console.error('Get system health error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching system health'
        });
    }
});

module.exports = router;
