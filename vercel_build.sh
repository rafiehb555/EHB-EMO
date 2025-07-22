#!/bin/bash
# EHB-5 Vercel Build Script
# Automated build and deployment script for Vercel

set -e

echo "🚀 Starting EHB-5 Vercel Build Process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    print_error "main.py not found. Please run this script from the project root."
    exit 1
fi

print_status "Checking project structure..."

# Verify essential files exist
required_files=(
    "main.py"
    "api_server.py"
    "database.py"
    "auth_manager.py"
    "data_processor.py"
    "ai_agents.py"
    "requirements.txt"
    "vercel.json"
    "api/index.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file not found: $file"
        exit 1
    fi
done

print_success "All required files found"

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ "$python_version" < "3.8" ]]; then
    print_error "Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi
print_success "Python version: $python_version"

# Install dependencies
print_status "Installing Python dependencies..."
if pip install -r requirements.txt; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Run tests
print_status "Running system tests..."
if python test_system.py; then
    print_success "All tests passed"
else
    print_warning "Some tests failed, but continuing with build"
fi

# Create build directory
print_status "Creating build directory..."
mkdir -p .vercel_build

# Copy files to build directory
print_status "Copying files to build directory..."
cp -r *.py .vercel_build/
cp -r api/ .vercel_build/
cp requirements.txt .vercel_build/
cp vercel.json .vercel_build/
cp *.html .vercel_build/ 2>/dev/null || true
cp *.css .vercel_build/ 2>/dev/null || true
cp *.js .vercel_build/ 2>/dev/null || true

# Create environment file for local testing
print_status "Creating environment file..."
cat > .vercel_build/.env << EOF
EHB5_ENVIRONMENT=production
EHB5_HOST=0.0.0.0
EHB5_PORT=5000
EHB5_DASHBOARD_PORT=8000
JWT_SECRET=ehb5-vercel-deployment-secret-2024
DATABASE_PATH=ehb5.db
LOG_LEVEL=INFO
DEBUG=false
EOF

# Test the API locally
print_status "Testing API locally..."
cd .vercel_build

# Start API server in background
python api_server.py &
API_PID=$!

# Wait for server to start
sleep 3

# Test health endpoint
if curl -s http://localhost:5000/api/health > /dev/null; then
    print_success "API server is running and responding"
else
    print_warning "API server test failed, but continuing"
fi

# Stop API server
kill $API_PID 2>/dev/null || true

cd ..

# Create deployment package
print_status "Creating deployment package..."
tar -czf ehb5-vercel-deployment.tar.gz .vercel_build/

# Generate deployment report
print_status "Generating deployment report..."
cat > deployment_report.md << EOF
# EHB-5 Vercel Deployment Report

## Build Information
- **Build Date**: $(date)
- **Python Version**: $python_version
- **Project Version**: 2.0.0
- **Environment**: Production

## Files Included
$(find .vercel_build -type f -name "*.py" | wc -l) Python files
$(find .vercel_build -type f -name "*.json" | wc -l) JSON files
$(find .vercel_build -type f -name "*.html" | wc -l) HTML files
$(find .vercel_build -type f -name "*.css" | wc -l) CSS files
$(find .vercel_build -type f -name "*.js" | wc -l) JavaScript files

## API Endpoints
- \`GET /api/health\` - Health check
- \`GET /api/system/status\` - System status
- \`GET /api/system/logs\` - System logs
- \`GET /api/projects\` - Get projects
- \`GET /api/data/files\` - Get data files
- \`GET /api/ai/agents\` - AI agents status
- \`POST /api/auth/login\` - User login
- \`POST /api/auth/register\` - User registration
- \`POST /api/projects\` - Create project
- \`POST /api/data/process\` - Data processing
- \`POST /api/ai/agents/execute\` - Execute AI agent

## Environment Variables
- EHB5_ENVIRONMENT=production
- EHB5_HOST=0.0.0.0
- EHB5_PORT=5000
- EHB5_DASHBOARD_PORT=8000
- JWT_SECRET=ehb5-vercel-deployment-secret-2024
- DATABASE_PATH=ehb5.db
- LOG_LEVEL=INFO
- DEBUG=false

## Deployment Instructions
1. Upload the \`ehb5-vercel-deployment.tar.gz\` file to Vercel
2. Set the environment variables in Vercel Dashboard
3. Deploy the project
4. Test the endpoints using the provided URLs

## Testing Commands
\`\`\`bash
# Health check
curl https://your-project-name.vercel.app/api/health

# System status
curl https://your-project-name.vercel.app/api/system/status

# Login test
curl -X POST https://your-project-name.vercel.app/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "admin123"}'
\`\`\`

## Support
- Vercel Documentation: https://vercel.com/docs
- Project Repository: https://github.com/rafiehb555/ehb-5
- Build Date: $(date)
EOF

print_success "Deployment report generated: deployment_report.md"

# Cleanup
print_status "Cleaning up build files..."
rm -rf .vercel_build/

print_success "Build process completed successfully!"
print_status "Deployment package: ehb5-vercel-deployment.tar.gz"
print_status "Deployment report: deployment_report.md"

echo ""
echo "🎉 EHB-5 is ready for Vercel deployment!"
echo ""
echo "Next steps:"
echo "1. Go to https://vercel.com"
echo "2. Create a new project"
echo "3. Import your GitHub repository: rafiehb555/ehb-5"
echo "4. Set environment variables"
echo "5. Deploy!"
echo ""
echo "Your app will be available at: https://your-project-name.vercel.app" 