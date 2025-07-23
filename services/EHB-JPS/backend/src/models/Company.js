const { DataTypes } = require('sequelize');
const sequelize = require('../database/connection');

const Company = sequelize.define('Company', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    user_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'users',
            key: 'id'
        }
    },
    company_name: {
        type: DataTypes.STRING(255),
        allowNull: false
    },
    industry: {
        type: DataTypes.STRING(100),
        allowNull: true
    },
    company_size: {
        type: DataTypes.STRING(50),
        allowNull: true
    },
    website: {
        type: DataTypes.STRING(255),
        allowNull: true,
        validate: {
            isUrl: true
        }
    },
    description: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    logo_url: {
        type: DataTypes.STRING(255),
        allowNull: true
    },
    location: {
        type: DataTypes.STRING(255),
        allowNull: true
    },
    founded_year: {
        type: DataTypes.INTEGER,
        allowNull: true
    },
    revenue: {
        type: DataTypes.STRING(100),
        allowNull: true
    },
    is_verified: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    is_active: {
        type: DataTypes.BOOLEAN,
        defaultValue: true
    },
    contact_email: {
        type: DataTypes.STRING(255),
        allowNull: true,
        validate: {
            isEmail: true
        }
    },
    contact_phone: {
        type: DataTypes.STRING(20),
        allowNull: true
    },
    social_links: {
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
    tableName: 'companies',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
});

// Instance methods
Company.prototype.getFullInfo = function() {
    return {
        id: this.id,
        company_name: this.company_name,
        industry: this.industry,
        company_size: this.company_size,
        website: this.website,
        description: this.description,
        logo_url: this.logo_url,
        location: this.location,
        founded_year: this.founded_year,
        revenue: this.revenue,
        is_verified: this.is_verified,
        contact_email: this.contact_email,
        contact_phone: this.contact_phone,
        social_links: this.social_links
    };
};

Company.prototype.getContactInfo = function() {
    return {
        contact_email: this.contact_email,
        contact_phone: this.contact_phone,
        website: this.website
    };
};

// Class methods
Company.findByUserId = function(userId) {
    return this.findOne({ where: { user_id: userId } });
};

Company.findVerified = function() {
    return this.findAll({
        where: {
            is_verified: true,
            is_active: true
        },
        order: [['company_name', 'ASC']]
    });
};

Company.searchCompanies = function(searchParams) {
    const where = { is_active: true };

    if (searchParams.keyword) {
        where[sequelize.Op.or] = [
            { company_name: { [sequelize.Op.iLike]: `%${searchParams.keyword}%` } },
            { description: { [sequelize.Op.iLike]: `%${searchParams.keyword}%` } }
        ];
    }

    if (searchParams.industry) {
        where.industry = { [sequelize.Op.iLike]: `%${searchParams.industry}%` };
    }

    if (searchParams.location) {
        where.location = { [sequelize.Op.iLike]: `%${searchParams.location}%` };
    }

    return this.findAll({
        where,
        order: [['company_name', 'ASC']]
    });
};

module.exports = Company;
