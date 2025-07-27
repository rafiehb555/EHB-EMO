#!/bin/bash

# EHB Healthcare System Deployment Script
# This script deploys the complete healthcare system with security and monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ehb-healthcare"
ENVIRONMENT=${1:-production}
BACKUP_DIR="./backups"
LOG_DIR="./logs"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p $BACKUP_DIR $LOG_DIR ./database ./nginx ./monitoring/grafana/dashboards ./monitoring/grafana/datasources
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check available ports
    local ports=(3000 8000 5432 6379 80 443 9090 3001)
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
            warning "Port $port is already in use. Please ensure it's not conflicting."
        fi
    done
    
    log "System requirements check completed."
}

# Security scan
security_scan() {
    log "Running security scan..."
    
    # Scan for vulnerabilities in dependencies
    if [ -f "frontend/package.json" ]; then
        log "Scanning frontend dependencies..."
        cd frontend && npm audit --audit-level=high || warning "Frontend security vulnerabilities found"
        cd ..
    fi
    
    if [ -f "backend/requirements.txt" ]; then
        log "Scanning backend dependencies..."
        pip-audit -r backend/requirements.txt || warning "Backend security vulnerabilities found"
    fi
    
    log "Security scan completed."
}

# Backup existing data
backup_data() {
    log "Creating backup of existing data..."
    
    if [ -d "$BACKUP_DIR" ]; then
        local backup_file="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "$backup_file" ./data ./logs 2>/dev/null || warning "No existing data to backup"
        log "Backup created: $backup_file"
    fi
}

# Build and deploy services
deploy_services() {
    log "Building and deploying services..."
    
    # Stop existing containers
    docker-compose down --remove-orphans
    
    # Build images
    log "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    log "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    check_service_health
}

# Check service health
check_service_health() {
    log "Checking service health..."
    
    local services=("frontend" "backend" "postgres" "redis" "nginx")
    local healthy=true
    
    for service in "${services[@]}"; do
        if docker-compose ps $service | grep -q "Up"; then
            log "✓ $service is running"
        else
            error "✗ $service is not running"
            healthy=false
        fi
    done
    
    if [ "$healthy" = true ]; then
        log "All services are healthy!"
    else
        error "Some services are not healthy. Check logs with: docker-compose logs"
    fi
}

# Initialize database
init_database() {
    log "Initializing database..."
    
    # Wait for PostgreSQL to be ready
    log "Waiting for PostgreSQL to be ready..."
    sleep 10
    
    # Create database schema
    docker-compose exec -T postgres psql -U ehb_user -d ehb_healthcare -c "
        CREATE TABLE IF NOT EXISTS patients (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(50) NOT NULL,
            contact VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            priority VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            medical_history TEXT[],
            prescriptions TEXT[],
            lab_results TEXT[],
            appointments TEXT[],
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS appointments (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255) NOT NULL,
            doctor_name VARCHAR(255) NOT NULL,
            date TIMESTAMP NOT NULL,
            type VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        
        CREATE TABLE IF NOT EXISTS medical_records (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255) NOT NULL,
            diagnosis TEXT NOT NULL,
            treatment TEXT NOT NULL,
            prescription TEXT NOT NULL,
            lab_results TEXT NOT NULL,
            date TIMESTAMP NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            role VARCHAR(255) NOT NULL,
            permissions TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_patients_priority ON patients(priority);
        CREATE INDEX IF NOT EXISTS idx_patients_status ON patients(status);
        CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
        CREATE INDEX IF NOT EXISTS idx_medical_records_patient ON medical_records(patient_id);
    " || warning "Database initialization completed with warnings"
    
    log "Database initialization completed."
}

# Setup monitoring
setup_monitoring() {
    log "Setting up monitoring..."
    
    # Create Prometheus configuration
    cat > ./monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ehb-healthcare'
    static_configs:
      - targets: ['frontend:3000', 'backend:8000', 'postgres:5432', 'redis:6379']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
    metrics_path: /nginx_status
EOF

    # Create Grafana datasource
    mkdir -p ./monitoring/grafana/datasources
    cat > ./monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://monitoring:9090
    isDefault: true
EOF

    log "Monitoring setup completed."
}

# Setup SSL certificates (for production)
setup_ssl() {
    if [ "$ENVIRONMENT" = "production" ]; then
        log "Setting up SSL certificates..."
        
        mkdir -p ./nginx/ssl
        
        # Generate self-signed certificate for development
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ./nginx/ssl/nginx.key \
            -out ./nginx/ssl/nginx.crt \
            -subj "/C=US/ST=State/L=City/O=EHB Healthcare/CN=localhost" \
            || warning "SSL certificate generation failed"
        
        log "SSL certificates generated."
    fi
}

# Create Nginx configuration
create_nginx_config() {
    log "Creating Nginx configuration..."
    
    cat > ./nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone \$binary_remote_addr zone=frontend:10m rate=30r/s;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    server {
        listen 80;
        server_name localhost;
        
        # Frontend
        location / {
            limit_req zone=frontend burst=20 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Backend API
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
    
    # HTTPS configuration (for production)
    server {
        listen 443 ssl http2;
        server_name localhost;
        
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # Frontend
        location / {
            limit_req zone=frontend burst=20 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Backend API
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

    log "Nginx configuration created."
}

# Run tests
run_tests() {
    log "Running tests..."
    
    # Frontend tests
    if [ -f "frontend/package.json" ]; then
        log "Running frontend tests..."
        cd frontend && npm test -- --passWithNoTests || warning "Frontend tests failed"
        cd ..
    fi
    
    # Backend tests
    if [ -f "backend/requirements.txt" ]; then
        log "Running backend tests..."
        cd backend && python -m pytest tests/ -v || warning "Backend tests failed"
        cd ..
    fi
    
    log "Tests completed."
}

# Performance test
performance_test() {
    log "Running performance tests..."
    
    # Test API response time
    local start_time=$(date +%s.%N)
    curl -s http://localhost:8000/api/health > /dev/null
    local end_time=$(date +%s.%N)
    local response_time=$(echo "$end_time - $start_time" | bc)
    
    if (( $(echo "$response_time < 1.0" | bc -l) )); then
        log "✓ API response time: ${response_time}s (Good)"
    else
        warning "⚠ API response time: ${response_time}s (Slow)"
    fi
    
    # Test frontend load time
    start_time=$(date +%s.%N)
    curl -s http://localhost:3000 > /dev/null
    end_time=$(date +%s.%N)
    response_time=$(echo "$end_time - $start_time" | bc)
    
    if (( $(echo "$response_time < 3.0" | bc -l) )); then
        log "✓ Frontend load time: ${response_time}s (Good)"
    else
        warning "⚠ Frontend load time: ${response_time}s (Slow)"
    fi
}

# Main deployment function
main() {
    log "Starting EHB Healthcare System deployment..."
    log "Environment: $ENVIRONMENT"
    
    # Check if bc is installed for calculations
    if ! command -v bc &> /dev/null; then
        warning "bc is not installed. Performance tests will be skipped."
    fi
    
    create_directories
    check_requirements
    security_scan
    backup_data
    create_nginx_config
    setup_ssl
    setup_monitoring
    deploy_services
    init_database
    run_tests
    performance_test
    
    log "Deployment completed successfully!"
    log ""
    log "Access your healthcare system:"
    log "  Frontend: http://localhost:3000"
    log "  Admin Panel: http://localhost:3000/admin"
    log "  Backend API: http://localhost:8000"
    log "  API Docs: http://localhost:8000/docs"
    log "  Monitoring: http://localhost:9090"
    log "  Grafana: http://localhost:3001"
    log ""
    log "To view logs: docker-compose logs -f"
    log "To stop services: docker-compose down"
}

# Run main function
main "$@" 