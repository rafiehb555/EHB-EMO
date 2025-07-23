const express = require('express');
const { body, validationResult } = require('express-validator');
const Application = require('../models/Application');
const Job = require('../models/Job');
const User = require('../models/User');
const Company = require('../models/Company');
const auth = require('../middleware/auth');
const router = express.Router();

// Validation middleware
const validateApplicationUpdate = [
    body('status').optional().isIn(['pending', 'reviewed', 'shortlisted', 'rejected', 'hired']),
    body('review_notes').optional().trim(),
    body('interview_date').optional().isISO8601(),
    body('interview_location').optional().trim(),
    body('interview_notes').optional().trim()
];

// @route   GET /api/applications
// @desc    Get all applications (Admin/Company)
// @access  Private
router.get('/', auth, async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            status,
            job_id,
            user_id,
            company_id
        } = req.query;

        const offset = (page - 1) * limit;
        const where = {};

        // Apply filters
        if (status) {
            where.status = status;
        }

        if (job_id) {
            where.job_id = parseInt(job_id);
        }

        if (user_id) {
            where.user_id = parseInt(user_id);
        }

        // If user is company, only show applications for their jobs
        if (req.user.user_type === 'company') {
            const company = await Company.findOne({
                where: { user_id: req.user.id }
            });
            if (company) {
                const jobIds = await Job.findAll({
                    where: { company_id: company.id },
                    attributes: ['id']
                });
                where.job_id = { [sequelize.Op.in]: jobIds.map(j => j.id) };
            }
        }

        const { count, rows } = await Application.findAndCountAll({
            where,
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['id', 'first_name', 'last_name', 'email', 'profile_image']
                },
                {
                    model: Job,
                    as: 'job',
                    include: [
                        {
                            model: Company,
                            as: 'company',
                            attributes: ['id', 'company_name', 'logo_url']
                        }
                    ]
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

// @route   GET /api/applications/:id
// @desc    Get application by ID
// @access  Private
router.get('/:id', auth, async (req, res) => {
    try {
        const { id } = req.params;

        const application = await Application.findByPk(id, {
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['id', 'first_name', 'last_name', 'email', 'profile_image', 'phone']
                },
                {
                    model: Job,
                    as: 'job',
                    include: [
                        {
                            model: Company,
                            as: 'company',
                            attributes: ['id', 'company_name', 'logo_url', 'location']
                        }
                    ]
                }
            ]
        });

        if (!application) {
            return res.status(404).json({
                success: false,
                message: 'Application not found'
            });
        }

        // Check if user has permission to view this application
        if (req.user.user_type === 'jobseeker' && application.user_id !== req.user.id) {
            return res.status(403).json({
                success: false,
                message: 'Access denied'
            });
        }

        if (req.user.user_type === 'company') {
            const company = await Company.findOne({
                where: { user_id: req.user.id }
            });
            if (!company || application.job.company_id !== company.id) {
                return res.status(403).json({
                    success: false,
                    message: 'Access denied'
                });
            }
        }

        res.json({
            success: true,
            data: { application }
        });

    } catch (error) {
        console.error('Get application error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching application'
        });
    }
});

// @route   PUT /api/applications/:id/status
// @desc    Update application status
// @access  Private (Company/Admin)
router.put('/:id/status', auth, validateApplicationUpdate, async (req, res) => {
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
        const { status, review_notes, interview_date, interview_location, interview_notes } = req.body;

        const application = await Application.findByPk(id, {
            include: [
                {
                    model: Job,
                    as: 'job',
                    include: [
                        {
                            model: Company,
                            as: 'company'
                        }
                    ]
                }
            ]
        });

        if (!application) {
            return res.status(404).json({
                success: false,
                message: 'Application not found'
            });
        }

        // Check if user has permission to update this application
        if (req.user.user_type === 'company') {
            const company = await Company.findOne({
                where: { user_id: req.user.id }
            });
            if (!company || application.job.company_id !== company.id) {
                return res.status(403).json({
                    success: false,
                    message: 'Access denied'
                });
            }
        }

        // Update application
        const updateData = {};
        if (status) updateData.status = status;
        if (review_notes !== undefined) updateData.review_notes = review_notes;
        if (interview_date) updateData.interview_date = new Date(interview_date);
        if (interview_location) updateData.interview_location = interview_location;
        if (interview_notes) updateData.interview_notes = interview_notes;

        await application.updateStatus(
            status || application.status,
            req.user.id,
            review_notes
        );

        // If interview is scheduled, update status to shortlisted
        if (interview_date && interview_location) {
            await application.scheduleInterview(
                new Date(interview_date),
                interview_location,
                interview_notes
            );
        }

        res.json({
            success: true,
            message: 'Application status updated successfully',
            data: { application }
        });

    } catch (error) {
        console.error('Update application status error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while updating application status'
        });
    }
});

// @route   GET /api/applications/stats
// @desc    Get application statistics
// @access  Private (Admin/Company)
router.get('/stats', auth, async (req, res) => {
    try {
        let where = {};

        // If user is company, only show stats for their jobs
        if (req.user.user_type === 'company') {
            const company = await Company.findOne({
                where: { user_id: req.user.id }
            });
            if (company) {
                const jobIds = await Job.findAll({
                    where: { company_id: company.id },
                    attributes: ['id']
                });
                where.job_id = { [sequelize.Op.in]: jobIds.map(j => j.id) };
            }
        }

        // Get application statistics
        const stats = await Application.findAll({
            where,
            attributes: [
                'status',
                [sequelize.fn('COUNT', sequelize.col('id')), 'count']
            ],
            group: ['status']
        });

        const statsObject = stats.reduce((acc, stat) => {
            acc[stat.status] = parseInt(stat.dataValues.count);
            return acc;
        }, {});

        // Get recent applications
        const recentApplications = await Application.findAll({
            where,
            order: [['applied_at', 'DESC']],
            limit: 10,
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['first_name', 'last_name']
                },
                {
                    model: Job,
                    as: 'job',
                    attributes: ['title'],
                    include: [
                        {
                            model: Company,
                            as: 'company',
                            attributes: ['company_name']
                        }
                    ]
                }
            ]
        });

        res.json({
            success: true,
            data: {
                stats: statsObject,
                recent_applications: recentApplications
            }
        });

    } catch (error) {
        console.error('Get application stats error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching application statistics'
        });
    }
});

// @route   POST /api/applications/:id/interview
// @desc    Schedule interview for application
// @access  Private (Company/Admin)
router.post('/:id/interview', auth, [
    body('interview_date').isISO8601(),
    body('interview_location').trim().notEmpty(),
    body('interview_notes').optional().trim()
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
        const { interview_date, interview_location, interview_notes } = req.body;

        const application = await Application.findByPk(id, {
            include: [
                {
                    model: Job,
                    as: 'job',
                    include: [
                        {
                            model: Company,
                            as: 'company'
                        }
                    ]
                }
            ]
        });

        if (!application) {
            return res.status(404).json({
                success: false,
                message: 'Application not found'
            });
        }

        // Check if user has permission
        if (req.user.user_type === 'company') {
            const company = await Company.findOne({
                where: { user_id: req.user.id }
            });
            if (!company || application.job.company_id !== company.id) {
                return res.status(403).json({
                    success: false,
                    message: 'Access denied'
                });
            }
        }

        // Schedule interview
        await application.scheduleInterview(
            new Date(interview_date),
            interview_location,
            interview_notes
        );

        res.json({
            success: true,
            message: 'Interview scheduled successfully',
            data: { application }
        });

    } catch (error) {
        console.error('Schedule interview error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while scheduling interview'
        });
    }
});

// @route   DELETE /api/applications/:id
// @desc    Delete application (Admin only)
// @access  Private (Admin)
router.delete('/:id', auth, async (req, res) => {
    try {
        const { id } = req.params;

        // Only admin can delete applications
        if (req.user.user_type !== 'admin') {
            return res.status(403).json({
                success: false,
                message: 'Access denied. Admin only.'
            });
        }

        const application = await Application.findByPk(id);
        if (!application) {
            return res.status(404).json({
                success: false,
                message: 'Application not found'
            });
        }

        await application.destroy();

        res.json({
            success: true,
            message: 'Application deleted successfully'
        });

    } catch (error) {
        console.error('Delete application error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while deleting application'
        });
    }
});

module.exports = router;
