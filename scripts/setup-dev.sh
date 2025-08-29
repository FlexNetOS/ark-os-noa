#!/bin/bash
# Development Environment Setup Script for ark-os-noa
# This script automates the development environment setup process

set -e  # Exit on any error

echo "🚀 Setting up ark-os-noa development environment..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is required but not installed."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is required but not installed."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is required but not installed."
        exit 1
    fi
    
    echo "✅ Prerequisites check passed"
}

# Setup Python virtual environment
setup_venv() {
    echo "🐍 Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✅ Virtual environment created"
    else
        echo "✅ Virtual environment already exists"
    fi
    
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
        echo "✅ Development dependencies installed"
    fi
}

# Setup infrastructure services
setup_infrastructure() {
    echo "🏗️  Starting infrastructure services..."
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        echo "❌ docker-compose.yml not found"
        exit 1
    fi
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check service health
    echo "🔍 Checking service health..."
    
    # Check Redis
    if docker-compose exec redis redis-cli ping | grep -q PONG; then
        echo "✅ Redis is ready"
    else
        echo "⚠️  Redis may not be ready yet"
    fi
    
    # Check Postgres
    if docker-compose exec postgres pg_isready -U noa | grep -q "accepting connections"; then
        echo "✅ Postgres is ready"
    else
        echo "⚠️  Postgres may not be ready yet"
    fi
    
    echo "✅ Infrastructure setup complete"
}

# Run tests to verify setup
verify_setup() {
    echo "🧪 Running tests to verify setup..."
    
    source venv/bin/activate
    
    if python -m pytest tests/ -v; then
        echo "✅ All tests passed"
    else
        echo "❌ Some tests failed"
        exit 1
    fi
}

# Setup git hooks (if pre-commit is installed)
setup_git_hooks() {
    if command -v pre-commit &> /dev/null; then
        echo "🪝 Setting up git hooks..."
        pre-commit install
        echo "✅ Git hooks installed"
    fi
}

# Main execution
main() {
    echo "======================================"
    echo "ark-os-noa Development Setup"
    echo "======================================"
    
    check_prerequisites
    setup_venv
    setup_infrastructure
    verify_setup
    setup_git_hooks
    
    echo ""
    echo "🎉 Development environment setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Start a service: uvicorn services.intake.main:app --reload --port 8001"
    echo "3. View services: docker-compose ps"
    echo "4. Run tests: python -m pytest tests/"
    echo "5. Check MinIO console: http://localhost:9001 (admin/admin)"
    echo "6. Check registry: http://localhost:5000/v2/_catalog"
    echo ""
}

# Run main function
main "$@"