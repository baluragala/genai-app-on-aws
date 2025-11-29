#!/bin/bash

# Automated EC2 Deployment Script for RAG Application
# Run this script on a fresh EC2 instance (Amazon Linux 2023 or Ubuntu)

set -e

echo "=========================================="
echo "RAG Application - EC2 Deployment Script"
echo "=========================================="
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ Cannot detect OS"
    exit 1
fi

echo "📍 Detected OS: $OS"
echo ""

# Step 1: Update system
echo "📦 Step 1/6: Updating system..."
if [ "$OS" = "amzn" ]; then
    sudo yum update -y
elif [ "$OS" = "ubuntu" ]; then
    sudo apt update && sudo apt upgrade -y
fi
echo "✅ System updated"
echo ""

# Step 2: Install Docker
echo "🐳 Step 2/6: Installing Docker..."
if [ "$OS" = "amzn" ]; then
    sudo yum install docker -y
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ec2-user
elif [ "$OS" = "ubuntu" ]; then
    sudo apt install docker.io -y
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
fi
echo "✅ Docker installed"
echo ""

# Step 3: Install Docker Compose
echo "🔧 Step 3/6: Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
echo "✅ Docker Compose installed"
echo ""

# Step 4: Install Git
echo "📥 Step 4/6: Installing Git..."
if [ "$OS" = "amzn" ]; then
    sudo yum install git -y
elif [ "$OS" = "ubuntu" ]; then
    sudo apt install git -y
fi
echo "✅ Git installed"
echo ""

# Step 5: Clone repository
echo "📂 Step 5/6: Cloning repository..."
cd ~
if [ -d "genai-app-on-aws" ]; then
    echo "⚠️  Directory already exists. Updating..."
    cd genai-app-on-aws
    git pull origin main
else
    git clone https://github.com/baluragala/genai-app-on-aws.git
    cd genai-app-on-aws
fi
echo "✅ Repository cloned"
echo ""

# Step 6: Configure environment
echo "⚙️  Step 6/6: Configuring environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: You need to edit .env file with your OpenAI API key!"
    echo ""
    echo "Run the following commands:"
    echo "  cd ~/genai-app-on-aws"
    echo "  nano .env"
    echo ""
    echo "Then add your OPENAI_API_KEY and save."
else
    echo "✅ .env file already exists"
fi
echo ""

# Display next steps
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Configure your OpenAI API key:"
echo "   cd ~/genai-app-on-aws"
echo "   nano .env"
echo "   (Add your OPENAI_API_KEY)"
echo ""
echo "2. Logout and login again for Docker group to take effect:"
echo "   exit"
if [ "$OS" = "amzn" ]; then
    echo "   ssh -i your-key.pem ec2-user@YOUR_EC2_IP"
elif [ "$OS" = "ubuntu" ]; then
    echo "   ssh -i your-key.pem ubuntu@YOUR_EC2_IP"
fi
echo ""
echo "3. Start the application:"
echo "   cd ~/genai-app-on-aws"
echo "   docker-compose up -d --build"
echo ""
echo "4. Check status:"
echo "   docker-compose ps"
echo "   docker-compose logs -f"
echo ""
echo "5. Access application:"
echo "   http://YOUR_EC2_PUBLIC_IP:8501"
echo ""
echo "=========================================="
echo "📚 For detailed instructions, see:"
echo "   DEPLOYMENT_AWS_EC2.md"
echo "=========================================="

