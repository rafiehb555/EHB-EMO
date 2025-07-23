const { DataTypes } = require('sequelize');
const sequelize = require('../database/connection');

const Job = sequelize.define('Job', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    company_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'companies',
            key: 'id'
        }
    },
    title: {
        type: DataTypes.STRING(255),
        allowNull: false
    },
    description: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    requirements: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    salary_min: {
        type: DataTypes.INTEGER,
        allowNull: true
    },
    salary_max: {
        type: DataTypes.INTEGER,
        allowNull: true
    },
    location: {
        type: DataTypes.STRING(255),
        allowNull: true
    },
    job_type: {
        type: DataTypes.ENUM('full-time', 'part-time', 'contract', 'internship'),
        allowNull: false,
        defaultValue: 'full-time'
    },
    experience_level: {
        type: DataTypes.STRING(50),
        allowNull: true
    },
    skills: {
        type: DataTypes.ARRAY(DataTypes.STRING),
        allowNull: true,
        defaultValue: []
    },
    status: {
        type: DataTypes.ENUM('active', 'inactive', 'filled', 'expired'),
        defaultValue: 'active',
        allowNull: false
    },
    is_featured: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    is_remote: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    application_deadline: {
        type: DataTypes.DATE,
        allowNull: true
    },
    views_count: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    applications_count: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    tags: {
        type: DataTypes.ARRAY(DataTypes.STRING),
        allowNull: true,
        defaultValue: []
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
    tableName: 'jobs',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
});

// Instance methods
Job.prototype.getSalaryRange = function() {
    if (this.salary_min && this.salary_max) {
        return `${this.salary_min.toLocaleString()} - ${this.salary_max.toLocaleString()}`;
    } else if (this.salary_min) {
        return `From ${this.salary_min.toLocaleString()}`;
    } else if (this.salary_max) {
        return `Up to ${this.salary_max.toLocaleString()}`;
    }
    return 'Salary not specified';
};

Job.prototype.isExpired = function() {
    if (!this.application_deadline) return false;
    return new Date() > new Date(this.application_deadline);
};

Job.prototype.incrementViews = async function() {
    this.views_count += 1;
    await this.save();
};

Job.prototype.incrementApplications = async function() {
    this.applications_count += 1;
    await this.save();
};

// Class methods
Job.findActive = function() {
    return this.findAll({
        where: { status: 'active' },
        order: [['created_at', 'DESC']]
    });
};

Job.findByCompany = function(companyId) {
    return this.findAll({
        where: { company_id: companyId },
        order: [['created_at', 'DESC']]
    });
};

Job.searchJobs = function(searchParams) {
    const where = { status: 'active' };

    if (searchParams.keyword) {
        where[sequelize.Op.or] = [
            { title: { [sequelize.Op.iLike]: `%${searchParams.keyword}%` } },
            { description: { [sequelize.Op.iLike]: `%${searchParams.keyword}%` } }
        ];
    }

    if (searchParams.location) {
        where.location = { [sequelize.Op.iLike]: `%${searchParams.location}%` };
    }

    if (searchParams.job_type) {
        where.job_type = searchParams.job_type;
    }

    if (searchParams.salary_min) {
        where.salary_min = { [sequelize.Op.gte]: searchParams.salary_min };
    }

    if (searchParams.salary_max) {
        where.salary_max = { [sequelize.Op.lte]: searchParams.salary_max };
    }

    return this.findAll({
        where,
        order: [['created_at', 'DESC']]
    });
};

module.exports = Job;
