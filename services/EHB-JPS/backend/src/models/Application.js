const { DataTypes } = require('sequelize');
const sequelize = require('../database/connection');

const Application = sequelize.define('Application', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    job_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'jobs',
            key: 'id'
        }
    },
    user_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'users',
            key: 'id'
        }
    },
    resume_url: {
        type: DataTypes.STRING(255),
        allowNull: true
    },
    cover_letter: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    status: {
        type: DataTypes.ENUM('pending', 'reviewed', 'shortlisted', 'rejected', 'hired'),
        defaultValue: 'pending',
        allowNull: false
    },
    applied_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    reviewed_at: {
        type: DataTypes.DATE,
        allowNull: true
    },
    reviewed_by: {
        type: DataTypes.INTEGER,
        allowNull: true,
        references: {
            model: 'users',
            key: 'id'
        }
    },
    review_notes: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    interview_date: {
        type: DataTypes.DATE,
        allowNull: true
    },
    interview_location: {
        type: DataTypes.STRING(255),
        allowNull: true
    },
    interview_notes: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    salary_expectation: {
        type: DataTypes.INTEGER,
        allowNull: true
    },
    availability: {
        type: DataTypes.STRING(100),
        allowNull: true
    },
    additional_files: {
        type: DataTypes.JSON,
        allowNull: true
    },
    created_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    updated_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    }
}, {
    tableName: 'applications',
    timestamps: true,
    createdAt: 'applied_at',
    updatedAt: 'updated_at'
});

// Instance methods
Application.prototype.updateStatus = async function(newStatus, reviewedBy = null, notes = null) {
    this.status = newStatus;
    this.reviewed_at = new Date();
    this.reviewed_by = reviewedBy;
    this.review_notes = notes;
    await this.save();
};

Application.prototype.scheduleInterview = async function(date, location, notes = null) {
    this.interview_date = date;
    this.interview_location = location;
    this.interview_notes = notes;
    this.status = 'shortlisted';
    await this.save();
};

Application.prototype.getStatusInfo = function() {
    const statusInfo = {
        pending: { label: 'Pending Review', color: '#f39c12' },
        reviewed: { label: 'Under Review', color: '#3498db' },
        shortlisted: { label: 'Shortlisted', color: '#27ae60' },
        rejected: { label: 'Rejected', color: '#e74c3c' },
        hired: { label: 'Hired', color: '#2ecc71' }
    };

    return statusInfo[this.status] || statusInfo.pending;
};

// Class methods
Application.findByUser = function(userId) {
    return this.findAll({
        where: { user_id: userId },
        order: [['applied_at', 'DESC']]
    });
};

Application.findByJob = function(jobId) {
    return this.findAll({
        where: { job_id: jobId },
        order: [['applied_at', 'ASC']]
    });
};

Application.findByStatus = function(status) {
    return this.findAll({
        where: { status },
        order: [['applied_at', 'DESC']]
    });
};

Application.getStats = async function() {
    const stats = await this.findAll({
        attributes: [
            'status',
            [sequelize.fn('COUNT', sequelize.col('id')), 'count']
        ],
        group: ['status']
    });

    return stats.reduce((acc, stat) => {
        acc[stat.status] = parseInt(stat.dataValues.count);
        return acc;
    }, {});
};

Application.findRecent = function(limit = 10) {
    return this.findAll({
        order: [['applied_at', 'DESC']],
        limit
    });
};

module.exports = Application;
