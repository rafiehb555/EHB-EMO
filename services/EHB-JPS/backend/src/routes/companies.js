const express = require('express');
const { body, validationResult } = require('express-validator');
const Company = require('../models/Company');
const Job = require('../models/Job');
const User = require('../models/User');
const router = express.Router();

// Validation middleware
const validateCompanyCreation = [
    body('company_name').trim().isLength({ min: 2, max: 255 }),
    body('industry').optional().trim(),
    body('company_size').optional().trim(),
    body('website').optional().isURL(),
    body('description').optional().trim(),
    body('location').optional().trim(),
    body('founded_year').optional().isInt({ min: 1800, max: new Date().getFullYear() }),
    body('revenue').optional().trim(),
    body('contact_email').optional().isEmail(),
    body('contact_phone').optional().trim()
];

const validateCompanyUpdate = [
    body('company_name').optional().trim().isLength({ min: 2, max: 255 }),
    body('industry').optional().trim(),
    body('website').optional().isURL(),
    body('description').optional().trim(),
    body('location').optional().trim(),
    body('founded_year').optional().isInt({ min: 1800, max: new Date().getFullYear() }),
    body('revenue').optional().trim(),
    body('contact_email').optional().isEmail(),
    body('contact_phone').optional().trim()
];

// @route   GET /api/companies
// @desc    Get all companies with pagination and filters
// @access  Public
router.get('/', async (req, res) => {
    try {
        const {
            page = 1,
            limit = 10,
            keyword,
            industry,
            location,
            is_verified
        } = req.query;

        const offset = (page - 1) * limit;
        const where = { is_active: true };

        // Apply filters
        if (keyword) {
            where[sequelize.Op.or] = [
                { company_name: { [sequelize.Op.iLike]: `%${keyword}%` } },
                { description: { [sequelize.Op.iLike]: `%${keyword}%` } }
            ];
        }

        if (industry) {
            where.industry = { [sequelize.Op.iLike]: `%${industry}%` };
        }

        if (location) {
            where.location = { [sequelize.Op.iLike]: `%${location}%` };
        }

        if (is_verified !== undefined) {
            where.is_verified = is_verified === 'true';
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
            order: [['company_name', 'ASC']],
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

// @route   GET /api/companies/:id
// @desc    Get company by ID
// @access  Public
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const company = await Company.findByPk(id, {
            include: [
                {
                    model: User,
                    as: 'user',
                    attributes: ['id', 'first_name', 'last_name', 'email']
                },
                {
                    model: Job,
                    as: 'jobs',
                    where: { status: 'active' },
                    required: false,
                    order: [['created_at', 'DESC']],
                    limit: 10
                }
            ]
        });

        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found'
            });
        }

        res.json({
            success: true,
            data: { company }
        });

    } catch (error) {
        console.error('Get company error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching company'
        });
    }
});

// @route   POST /api/companies
// @desc    Create a new company
// @access  Private
router.post('/', validateCompanyCreation, async (req, res) => {
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

        // Check if user already has a company
        const existingCompany = await Company.findByUserId(userId);
        if (existingCompany) {
            return res.status(400).json({
                success: false,
                message: 'User already has a company profile'
            });
        }

        const {
            company_name,
            industry,
            company_size,
            website,
            description,
            location,
            founded_year,
            revenue,
            contact_email,
            contact_phone,
            social_links
        } = req.body;

        const company = await Company.create({
            user_id: userId,
            company_name,
            industry,
            company_size,
            website,
            description,
            location,
            founded_year: founded_year ? parseInt(founded_year) : null,
            revenue,
            contact_email,
            contact_phone,
            social_links: social_links || {}
        });

        res.status(201).json({
            success: true,
            message: 'Company created successfully',
            data: { company }
        });

    } catch (error) {
        console.error('Create company error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while creating company'
        });
    }
});

// @route   PUT /api/companies/:id
// @desc    Update company
// @access  Private
router.put('/:id', validateCompanyUpdate, async (req, res) => {
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
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const company = await Company.findOne({
            where: { id, user_id: userId }
        });

        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found or access denied'
            });
        }

        const updateData = req.body;
        await company.update(updateData);

        res.json({
            success: true,
            message: 'Company updated successfully',
            data: { company }
        });

    } catch (error) {
        console.error('Update company error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while updating company'
        });
    }
});

// @route   DELETE /api/companies/:id
// @desc    Delete company
// @access  Private
router.delete('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const company = await Company.findOne({
            where: { id, user_id: userId }
        });

        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found or access denied'
            });
        }

        // Soft delete by setting is_active to false
        await company.update({ is_active: false });

        res.json({
            success: true,
            message: 'Company deleted successfully'
        });

    } catch (error) {
        console.error('Delete company error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while deleting company'
        });
    }
});

// @route   GET /api/companies/:id/jobs
// @desc    Get jobs by company
// @access  Public
router.get('/:id/jobs', async (req, res) => {
    try {
        const { id } = req.params;
        const { page = 1, limit = 10, status = 'active' } = req.query;

        const offset = (page - 1) * limit;
        const where = { company_id: id };

        if (status) {
            where.status = status;
        }

        const { count, rows } = await Job.findAndCountAll({
            where,
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
        console.error('Get company jobs error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching company jobs'
        });
    }
});

// @route   POST /api/companies/:id/upload-logo
// @desc    Upload company logo
// @access  Private
router.post('/:id/upload-logo', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({
                success: false,
                message: 'User not authenticated'
            });
        }

        const company = await Company.findOne({
            where: { id, user_id: userId }
        });

        if (!company) {
            return res.status(404).json({
                success: false,
                message: 'Company not found or access denied'
            });
        }

        // TODO: Implement file upload logic
        // For now, just return success
        const logoUrl = 'uploads/logos/company_' + id + '_logo.png';

        await company.update({ logo_url: logoUrl });

        res.json({
            success: true,
            message: 'Logo uploaded successfully',
            data: { logo_url: logoUrl }
        });

    } catch (error) {
        console.error('Upload logo error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while uploading logo'
        });
    }
});

// @route   GET /api/companies/search/suggestions
// @desc    Get company search suggestions
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

        const suggestions = await Company.findAll({
            where: {
                is_active: true,
                company_name: { [sequelize.Op.iLike]: `%${keyword}%` }
            },
            attributes: ['company_name'],
            group: ['company_name'],
            limit: 10
        });

        res.json({
            success: true,
            data: {
                suggestions: suggestions.map(s => s.company_name)
            }
        });

    } catch (error) {
        console.error('Company search suggestions error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching suggestions'
        });
    }
});

// @route   GET /api/companies/industries
// @desc    Get all industries
// @access  Public
router.get('/industries', async (req, res) => {
    try {
        const industries = await Company.findAll({
            where: { is_active: true },
            attributes: ['industry'],
            group: ['industry'],
            order: [['industry', 'ASC']]
        });

        res.json({
            success: true,
            data: {
                industries: industries.map(i => i.industry).filter(Boolean)
            }
        });

    } catch (error) {
        console.error('Get industries error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error while fetching industries'
        });
    }
});

module.exports = router;
