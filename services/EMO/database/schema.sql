-- EMO Database Schema
-- MongoDB Collections (represented as SQL for reference)

-- Users Collection
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    jps_user_id VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    role ENUM('franchise', 'seller', 'service_provider', 'school', 'agent'),
    sql_level ENUM('free', 'basic', 'normal', 'high', 'vip'),
    sql_expiry_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Businesses Collection
CREATE TABLE businesses (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    business_name VARCHAR(255),
    business_type VARCHAR(100),
    category VARCHAR(100),
    city VARCHAR(100),
    area VARCHAR(100),
    description TEXT,
    status ENUM('pending', 'verified', 'rejected', 'expired'),
    verification_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Documents Collection
CREATE TABLE documents (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    business_id VARCHAR(50),
    document_type ENUM('cnic', 'license', 'certificate', 'other'),
    file_url VARCHAR(500),
    file_hash VARCHAR(255),
    verification_status ENUM('pending', 'verified', 'rejected'),
    verified_by VARCHAR(50),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Complaints Collection
CREATE TABLE complaints (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    business_id VARCHAR(50),
    complaint_type VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    priority ENUM('low', 'medium', 'high', 'urgent'),
    status ENUM('open', 'in_progress', 'resolved', 'escalated'),
    assigned_franchise VARCHAR(50),
    escalation_level INT DEFAULT 1,
    deadline TIMESTAMP,
    resolved_at TIMESTAMP,
    penalty_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Franchises Collection
CREATE TABLE franchises (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    franchise_type ENUM('sub', 'master', 'corporate'),
    area_assigned TEXT,
    commission_rate DECIMAL(5,2),
    total_earnings DECIMAL(10,2),
    active_orders INT DEFAULT 0,
    resolved_complaints INT DEFAULT 0,
    status ENUM('active', 'inactive', 'suspended'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- SQL Level History
CREATE TABLE sql_history (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    old_level VARCHAR(20),
    new_level VARCHAR(20),
    reason TEXT,
    approved_by VARCHAR(50),
    blockchain_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Wallet Transactions
CREATE TABLE wallet_transactions (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    transaction_type ENUM('deposit', 'withdrawal', 'penalty', 'bonus', 'commission'),
    amount DECIMAL(10,2),
    blockchain_hash VARCHAR(255),
    status ENUM('pending', 'completed', 'failed'),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- AI Integration Logs
CREATE TABLE ai_logs (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    action_type VARCHAR(100),
    input_data TEXT,
    output_data TEXT,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Notifications
CREATE TABLE notifications (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    title VARCHAR(255),
    message TEXT,
    type ENUM('email', 'sms', 'push', 'in_app'),
    status ENUM('sent', 'delivered', 'failed'),
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
); 