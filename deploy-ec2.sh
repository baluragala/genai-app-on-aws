#!/bin/bash

# Complete Automated EC2 Deployment Script for RAG Application
# Run this script on EC2 instance (Amazon Linux 2023 or Ubuntu)
# This script will install Docker, clone/update repo, and start the application

set -e

echo "=========================================="
echo "RAG Application - Complete Deployment"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Please do not run this script as root (no sudo)"
    echo "Run as: ./deploy-ec2.sh"
    exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    OS_VERSION=$VERSION_ID
else
    echo "❌ Cannot detect OS"
    exit 1
fi

echo "📍 Detected OS: $PRETTY_NAME"
echo ""

# Check if this is first run or update
FIRST_RUN=false
if ! command -v docker &> /dev/null; then
    FIRST_RUN=true
    echo "🆕 First time installation detected"
else
    echo "🔄 Existing installation detected - will update"
fi
echo ""

# Step 1: Update system
echo "📦 Step 1/8: Updating system..."
if [ "$OS" = "amzn" ]; then
    sudo yum update -y
elif [ "$OS" = "ubuntu" ]; then
    sudo apt update && sudo apt upgrade -y
fi
echo "✅ System updated"
echo ""

# Step 2: Install/Update Docker
echo "🐳 Step 2/8: Setting up Docker..."
if [ "$OS" = "amzn" ]; then
    # Clean up any previous Docker CE attempts
    sudo yum remove docker-ce docker-ce-cli containerd.io -y 2>/dev/null || true
    sudo rm -f /etc/yum.repos.d/docker-ce.repo
    
    # Install Docker from Amazon Linux repos
    sudo yum install -y docker git
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add user to docker group
    sudo usermod -aG docker ec2-user
    
elif [ "$OS" = "ubuntu" ]; then
    sudo apt install -y docker.io git
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
fi
echo "✅ Docker installed/updated"
echo ""

# Step 3: Install Docker Compose
echo "🔧 Step 3/8: Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null || [ "$FIRST_RUN" = true ]; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi
echo ""

# Step 4: Verify Docker installation
echo "🧪 Step 4/8: Verifying Docker..."
sudo docker --version
docker-compose --version
echo "✅ Docker verified"
echo ""

# Step 5: Clone or update repository
echo "📂 Step 5/8: Setting up repository..."
cd ~
if [ -d "genai-app-on-aws" ]; then
    echo "📥 Updating existing repository..."
    cd genai-app-on-aws
    git pull origin main
    echo "✅ Repository updated"
else
    echo "📥 Cloning repository..."
    git clone https://github.com/baluragala/genai-app-on-aws.git
    cd genai-app-on-aws
    echo "✅ Repository cloned"
fi
echo ""

# Step 6: Configure environment
echo "⚙️  Step 6/8: Configuring environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please enter your OpenAI API key"
    read -p "Enter your OPENAI_API_KEY (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        sed -i "s/your-openai-api-key-here/$api_key/g" .env
        echo "✅ API key configured"
    else
        echo "⚠️  Skipped API key configuration - you'll need to edit .env manually"
        echo "   Run: nano ~/genai-app-on-aws/.env"
    fi
else
    echo "✅ .env file already exists"
    if grep -q "your-openai-api-key-here" .env; then
        echo "⚠️  Warning: .env still contains placeholder API key"
        read -p "Do you want to enter your OPENAI_API_KEY now? (y/n): " answer
        if [ "$answer" = "y" ]; then
            read -p "Enter your OPENAI_API_KEY: " api_key
            if [ ! -z "$api_key" ]; then
                sed -i "s/your-openai-api-key-here/$api_key/g" .env
                echo "✅ API key configured"
            fi
        fi
    fi
fi
echo ""

# Step 7: Check if we need to logout for docker group
if [ "$FIRST_RUN" = true ]; then
    echo "=========================================="
    echo "⚠️  FIRST TIME INSTALLATION"
    echo "=========================================="
    echo ""
    echo "Docker group was just added. You need to:"
    echo ""
    echo "1. Logout and login again:"
    echo "   exit"
    echo ""
    if [ "$OS" = "amzn" ]; then
        echo "2. Reconnect: ssh -i your-key.pem ec2-user@YOUR_EC2_IP"
    else
        echo "2. Reconnect: ssh -i your-key.pem ubuntu@YOUR_EC2_IP"
    fi
    echo ""
    echo "3. Run this script again:"
    echo "   cd ~/genai-app-on-aws"
    echo "   ./deploy-ec2.sh"
    echo ""
    echo "=========================================="
    exit 0
fi

# Step 7: Set legacy build mode
echo "🔧 Step 7/8: Configuring Docker build..."
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Add to bashrc if not already there
if ! grep -q "DOCKER_BUILDKIT=0" ~/.bashrc; then
    echo 'export DOCKER_BUILDKIT=0' >> ~/.bashrc
    echo 'export COMPOSE_DOCKER_CLI_BUILD=0' >> ~/.bashrc
    echo "✅ Build mode configured in ~/.bashrc"
else
    echo "✅ Build mode already configured"
fi
echo ""

# Step 8: Build and start application
echo "🚀 Step 8/8: Building and starting application..."
echo "⏳ This may take 3-5 minutes on first build..."
echo ""

# Check if API key is set
if grep -q "your-openai-api-key-here" .env; then
    echo "❌ Cannot start application: OpenAI API key not configured"
    echo ""
    echo "Please configure your API key:"
    echo "  cd ~/genai-app-on-aws"
    echo "  nano .env"
    echo ""
    echo "Then run: docker-compose up -d --build"
    exit 1
fi

# Build and start
if docker-compose up -d --build; then
    echo ""
    echo "✅ Application started successfully!"
    echo ""
    
    # Wait a moment for container to initialize
    sleep 3
    
    # Check status
    echo "📊 Container Status:"
    docker-compose ps
    echo ""
    
    # Get public IP
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "YOUR_EC2_IP")
    
    echo "=========================================="
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "✅ Application is running!"
    echo ""
    echo "🌐 Access your application at:"
    echo "   http://$PUBLIC_IP:8501"
    echo ""
    echo "📝 Useful commands:"
    echo "   View logs:    docker-compose logs -f"
    echo "   Stop app:     docker-compose down"
    echo "   Restart app:  docker-compose restart"
    echo "   Check status: docker-compose ps"
    echo ""
    echo "📚 Documentation:"
    echo "   ~/genai-app-on-aws/DEPLOYMENT_AWS_EC2.md"
    echo ""
    echo "=========================================="
else
    echo ""
    echo "❌ Failed to start application"
    echo ""
    echo "🔍 Check logs:"
    echo "   docker-compose logs"
    echo ""
    echo "🔧 Common issues:"
    echo "   - Check .env file: cat .env | grep OPENAI_API_KEY"
    echo "   - Check Docker: docker ps"
    echo "   - See troubleshooting: cat DEPLOYMENT_AWS_EC2.md"
    exit 1
fi

