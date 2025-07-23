const express = require('express');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const Application = require('../models/Application');
const router = express.Router();

// Validation middleware
const validateProfileUpdate = [
    body('first_name').optional().trim().isLength({ min: 2 }),
    body('last_name').optional().trim().isLength({ min: 2 }),
    body('phone').optional().trim(),
    body('profile_image').optional().trim(),
    body('resume_url').optional().trim(),
    body('preferences').optional().isObject()
];

// @route   GET /api/users/profile
// @desc    Get current user profile
// @access  Private
router.get('/profile', async (req, res) => {
    try {
        // Get user from token (implement middleware)
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const user = await User.findByPk(userId);
        if (!user) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }

        res.json({
            success: true,
            data: { user: user.toJSON() }
        });

    } catch (error) {
        console.error('Get profile error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching profile'
        });
    }
});

// @route   PUT /api/users/profile
// @desc    Update user profile
// @access  Private
router.put('/profile', validateProfileUpdate, async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({
                success: false,
                message: 'Validation failed',
                errors: errors.array()
            });
        }

        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const user = await User.findByPk(userId);
        if (!user) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }

        const updateData = req.body;
        await user.update(updateData);

        res.json({
            success: true,
            message: 'Profile updated successfully',
            data: { user: user.toJSON() }
        });

    } catch (error) {
        console.error('Update profile error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while updating profile'
        });
    }
});

// @route   GET /api/users/applications
// @desc    Get user's job applications
// @access  Private
router.get('/applications', async (req, res) => {
    try {
        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const { page = 1, limit = 10, status } = req.query;
        const offset = (page - 1) * limit;
        const where = { user_id: userId };

        if (status) {
            where.status = status;
        }

        const { count, rows } = await Application.findAndCountAll({
            where,
            include: [
                {
                    model: require('../models/Job'),
                    as: 'job',
                    include: [
                        {
                            model: require('../models/Company'),
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

// @route   GET /api/users/applications/:id
// @desc    Get specific application details
// @access  Private
router.get('/applications/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const application = await Application.findOne({
            where: { id, user_id: userId },
            include: [
                {
                    model: require('../models/Job'),
                    as: 'job',
                    include: [
                        {
                            model: require('../models/Company'),
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

// @route   POST /api/users/applications
// @desc    Apply for a job
// @access  Private
router.post('/applications', [
    body('job_id').isInt(),
    body('cover_letter').optional().trim(),
    body('resume_url').optional().trim(),
    body('salary_expectation').optional().isInt({ min: 0 }),
    body('availability').optional().trim()
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

        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const {
            job_id,
            cover_letter,
            resume_url,
            salary_expectation,
            availability
        } = req.body;

        // Check if already applied
        const existingApplication = await Application.findOne({
            where: { job_id, user_id: userId }
        });

        if (existingApplication) {
            return res.status(400).json({
                success: false,
                message: 'You have already applied for this job'
            });
        }

        // Create application
        const application = await Application.create({
            job_id,
            user_id: userId,
            cover_letter,
            resume_url,
            salary_expectation: salary_expectation ? parseInt(salary_expectation) : null,
            availability
        });

        // Increment job applications count
        const job = await require('../models/Job').findByPk(job_id);
        if (job) {
            await job.incrementApplications();
        }

        res.status(201).json({
            success: true,
            message: 'Application submitted successfully',
            data: { application }
        });

    } catch (error) {
        console.error('Create application error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while submitting application'
        });
    }
});

// @route   DELETE /api/users/applications/:id
// @desc    Withdraw application
// @access  Private
router.delete('/applications/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const application = await Application.findOne({
            where: { id, user_id: userId }
        });

        if (!application) {
            return res.status(404).json({
                success: false,
                message: 'Application not found'
            });
        }

        // Only allow withdrawal if status is pending
        if (application.status !== 'pending') {
            return res.status(400).json({
                success: false,
                message: 'Cannot withdraw application that has been reviewed'
            });
        }

        await application.destroy();

        res.json({
            success: true,
            message: 'Application withdrawn successfully'
        });

    } catch (error) {
        console.error('Withdraw application error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while withdrawing application'
        });
    }
});

// @route   GET /api/users/stats
// @desc    Get user statistics
// @access  Private
router.get('/stats', async (req, res) => {
    try {
        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        // Get application statistics
        const applicationStats = await Application.getStats();

        // Get user's application count
        const totalApplications = await Application.count({
            where: { user_id: userId }
        });

        // Get recent applications
        const recentApplications = await Application.findAll({
            where: { user_id: userId },
            order: [['applied_at', 'DESC']],
            limit: 5,
            include: [
                {
                    model: require('../models/Job'),
                    as: 'job',
                    attributes: ['id', 'title', 'company_id'],
                    include: [
                        {
                            model: require('../models/Company'),
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
                total_applications: totalApplications,
                application_stats: applicationStats,
                recent_applications: recentApplications
            }
        });

    } catch (error) {
        console.error('Get user stats error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching user statistics'
        });
    }
});

// @route   POST /api/users/upload-resume
// @desc    Upload user resume
// @access  Private
router.post('/upload-resume', async (req, res) => {
    try {
        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        // TODO: Implement file upload logic
        // For now, just return success
        const resumeUrl = 'uploads/resumes/user_' + userId + '_resume.pdf';

        const user = await User.findByPk(userId);
        await user.update({ resume_url: resumeUrl });

        res.json({
            success: true,
            message: 'Resume uploaded successfully',
            data: { resume_url: resumeUrl }
        });

    } catch (error) {
        console.error('Upload resume error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while uploading resume'
        });
    }
});

module.exports = router;
