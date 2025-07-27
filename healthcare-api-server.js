#!/usr/bin/env node

/**
 * Healthcare API Server
 * EHB Healthcare System - Complete API for patient management
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();
const prisma = new PrismaClient();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
    credentials: true
}));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }

    jwt.verify(token, process.env.JWT_SECRET || 'ehb-healthcare-secret', (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
    });
};

// Role-based access control
const requireRole = (roles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Authentication required' });
        }
        
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }
        
        next();
    };
};

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'EHB Healthcare API',
        version: '1.0.0'
    });
});

// Patient Routes
app.post('/api/patients', authenticateToken, requireRole(['doctor', 'admin']), async (req, res) => {
    try {
        const {
            patientId,
            firstName,
            lastName,
            dateOfBirth,
            gender,
            bloodType,
            phone,
            email,
            address,
            emergencyContact,
            insuranceNumber
        } = req.body;

        // Validate required fields
        if (!patientId || !firstName || !lastName || !dateOfBirth) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        // Check if patient already exists
        const existingPatient = await prisma.patient.findUnique({
            where: { patientId }
        });

        if (existingPatient) {
            return res.status(409).json({ error: 'Patient already exists' });
        }

        // Create new patient
        const patient = await prisma.patient.create({
            data: {
                patientId,
                firstName,
                lastName,
                dateOfBirth: new Date(dateOfBirth),
                gender,
                bloodType,
                phone,
                email,
                address,
                emergencyContact,
                insuranceNumber
            }
        });

        res.status(201).json({
            message: 'Patient created successfully',
            patient
        });

    } catch (error) {
        console.error('Error creating patient:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/patients', authenticateToken, requireRole(['doctor', 'admin', 'nurse']), async (req, res) => {
    try {
        const { page = 1, limit = 10, search } = req.query;
        const skip = (page - 1) * limit;

        const where = search ? {
            OR: [
                { firstName: { contains: search, mode: 'insensitive' } },
                { lastName: { contains: search, mode: 'insensitive' } },
                { patientId: { contains: search, mode: 'insensitive' } }
            ]
        } : {};

        const patients = await prisma.patient.findMany({
            where,
            skip: parseInt(skip),
            take: parseInt(limit),
            orderBy: { createdAt: 'desc' }
        });

        const total = await prisma.patient.count({ where });

        res.json({
            patients,
            pagination: {
                page: parseInt(page),
                limit: parseInt(limit),
                total,
                pages: Math.ceil(total / limit)
            }
        });

    } catch (error) {
        console.error('Error fetching patients:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/patients/:patientId', authenticateToken, requireRole(['doctor', 'admin', 'nurse']), async (req, res) => {
    try {
        const { patientId } = req.params;

        const patient = await prisma.patient.findUnique({
            where: { patientId },
            include: {
                medicalRecords: {
                    include: { doctor: true },
                    orderBy: { recordDate: 'desc' }
                },
                appointments: {
                    include: { doctor: true },
                    orderBy: { appointmentDate: 'desc' }
                },
                prescriptions: {
                    include: { doctor: true },
                    orderBy: { prescribedAt: 'desc' }
                },
                labResults: {
                    orderBy: { testDate: 'desc' }
                },
                allergies: true,
                medications: true
            }
        });

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        res.json({ patient });

    } catch (error) {
        console.error('Error fetching patient:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Medical Records Routes
app.post('/api/medical-records', authenticateToken, requireRole(['doctor']), async (req, res) => {
    try {
        const {
            patientId,
            diagnosis,
            symptoms,
            treatment,
            notes,
            ipfsHash
        } = req.body;

        // Validate required fields
        if (!patientId || !diagnosis) {
            return res.status(400).json({ error: 'Patient ID and diagnosis are required' });
        }

        // Check if patient exists
        const patient = await prisma.patient.findUnique({
            where: { patientId }
        });

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        // Create medical record
        const record = await prisma.medicalRecord.create({
            data: {
                recordId: `MR-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                patientId,
                doctorId: req.user.doctorId,
                diagnosis,
                symptoms,
                treatment,
                notes,
                ipfsHash
            },
            include: {
                patient: true,
                doctor: true
            }
        });

        res.status(201).json({
            message: 'Medical record created successfully',
            record
        });

    } catch (error) {
        console.error('Error creating medical record:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/medical-records/:patientId', authenticateToken, requireRole(['doctor', 'admin', 'nurse']), async (req, res) => {
    try {
        const { patientId } = req.params;

        const records = await prisma.medicalRecord.findMany({
            where: { patientId },
            include: {
                doctor: true
            },
            orderBy: { recordDate: 'desc' }
        });

        res.json({ records });

    } catch (error) {
        console.error('Error fetching medical records:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Appointment Routes
app.post('/api/appointments', authenticateToken, requireRole(['doctor', 'admin', 'nurse']), async (req, res) => {
    try {
        const {
            patientId,
            doctorId,
            appointmentDate,
            duration,
            notes
        } = req.body;

        // Validate required fields
        if (!patientId || !doctorId || !appointmentDate) {
            return res.status(400).json({ error: 'Patient ID, Doctor ID, and appointment date are required' });
        }

        // Check if patient and doctor exist
        const [patient, doctor] = await Promise.all([
            prisma.patient.findUnique({ where: { patientId } }),
            prisma.doctor.findUnique({ where: { doctorId } })
        ]);

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        if (!doctor) {
            return res.status(404).json({ error: 'Doctor not found' });
        }

        // Create appointment
        const appointment = await prisma.appointment.create({
            data: {
                appointmentId: `APT-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                patientId,
                doctorId,
                appointmentDate: new Date(appointmentDate),
                duration: duration || 30,
                notes
            },
            include: {
                patient: true,
                doctor: true
            }
        });

        res.status(201).json({
            message: 'Appointment created successfully',
            appointment
        });

    } catch (error) {
        console.error('Error creating appointment:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/appointments', authenticateToken, requireRole(['doctor', 'admin', 'nurse']), async (req, res) => {
    try {
        const { patientId, doctorId, status, date } = req.query;

        const where = {};
        if (patientId) where.patientId = patientId;
        if (doctorId) where.doctorId = doctorId;
        if (status) where.status = status;
        if (date) {
            where.appointmentDate = {
                gte: new Date(date),
                lt: new Date(new Date(date).getTime() + 24 * 60 * 60 * 1000)
            };
        }

        const appointments = await prisma.appointment.findMany({
            where,
            include: {
                patient: true,
                doctor: true
            },
            orderBy: { appointmentDate: 'asc' }
        });

        res.json({ appointments });

    } catch (error) {
        console.error('Error fetching appointments:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Prescription Routes
app.post('/api/prescriptions', authenticateToken, requireRole(['doctor']), async (req, res) => {
    try {
        const {
            patientId,
            medication,
            dosage,
            frequency,
            duration,
            instructions
        } = req.body;

        // Validate required fields
        if (!patientId || !medication || !dosage || !frequency) {
            return res.status(400).json({ error: 'Patient ID, medication, dosage, and frequency are required' });
        }

        // Check if patient exists
        const patient = await prisma.patient.findUnique({
            where: { patientId }
        });

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        // Create prescription
        const prescription = await prisma.prescription.create({
            data: {
                prescriptionId: `PRESC-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                patientId,
                doctorId: req.user.doctorId,
                medication,
                dosage,
                frequency,
                duration,
                instructions
            },
            include: {
                patient: true,
                doctor: true
            }
        });

        res.status(201).json({
            message: 'Prescription created successfully',
            prescription
        });

    } catch (error) {
        console.error('Error creating prescription:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Lab Results Routes
app.post('/api/lab-results', authenticateToken, requireRole(['doctor', 'lab_technician']), async (req, res) => {
    try {
        const {
            patientId,
            testName,
            testValue,
            normalRange,
            unit,
            notes
        } = req.body;

        // Validate required fields
        if (!patientId || !testName || !testValue) {
            return res.status(400).json({ error: 'Patient ID, test name, and test value are required' });
        }

        // Check if patient exists
        const patient = await prisma.patient.findUnique({
            where: { patientId }
        });

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        // Determine if result is abnormal
        const isAbnormal = normalRange ? !normalRange.includes(testValue) : false;

        // Create lab result
        const labResult = await prisma.labResult.create({
            data: {
                resultId: `LAB-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
                patientId,
                testName,
                testValue,
                normalRange,
                unit,
                isAbnormal,
                notes
            },
            include: {
                patient: true
            }
        });

        res.status(201).json({
            message: 'Lab result created successfully',
            labResult
        });

    } catch (error) {
        console.error('Error creating lab result:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Allergy Routes
app.post('/api/allergies', authenticateToken, requireRole(['doctor', 'nurse']), async (req, res) => {
    try {
        const {
            patientId,
            allergen,
            severity,
            symptoms,
            notes
        } = req.body;

        // Validate required fields
        if (!patientId || !allergen || !severity) {
            return res.status(400).json({ error: 'Patient ID, allergen, and severity are required' });
        }

        // Check if patient exists
        const patient = await prisma.patient.findUnique({
            where: { patientId }
        });

        if (!patient) {
            return res.status(404).json({ error: 'Patient not found' });
        }

        // Create allergy record
        const allergy = await prisma.allergy.create({
            data: {
                patientId,
                allergen,
                severity,
                symptoms,
                notes
            },
            include: {
                patient: true
            }
        });

        res.status(201).json({
            message: 'Allergy record created successfully',
            allergy
        });

    } catch (error) {
        console.error('Error creating allergy record:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Statistics and Analytics
app.get('/api/stats/overview', authenticateToken, requireRole(['admin', 'doctor']), async (req, res) => {
    try {
        const [
            totalPatients,
            totalDoctors,
            totalAppointments,
            totalRecords
        ] = await Promise.all([
            prisma.patient.count({ where: { isActive: true } }),
            prisma.doctor.count({ where: { isActive: true } }),
            prisma.appointment.count(),
            prisma.medicalRecord.count()
        ]);

        res.json({
            stats: {
                totalPatients,
                totalDoctors,
                totalAppointments,
                totalRecords
            }
        });

    } catch (error) {
        console.error('Error fetching statistics:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🏥 EHB Healthcare API Server running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`🔐 Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    console.log('🔄 Shutting down gracefully...');
    await prisma.$disconnect();
    process.exit(0);
});

module.exports = app; 