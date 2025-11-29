# 🐳 Docker Installation for Amazon Linux 2023 - CORRECT METHOD

## ❌ The Problem

Amazon Linux 2023 is NOT compatible with CentOS repositories. You'll get this error:

```
Error: Failed to download metadata for repo 'docker-ce-stable'
```

## ✅ Correct Installation Method for Amazon Linux 2023

Amazon Linux 2023 has Docker in its **native repositories**. Use these commands:

### Method 1: Install from Amazon Linux Repos (RECOMMENDED)

```bash
# Clean up any failed attempts
sudo yum remove docker docker-compose -y 2>/dev/null || true
sudo yum-config-manager --disable docker-ce-stable 2>/dev/null || true
sudo rm -f /etc/yum.repos.d/docker-ce.repo

# Update system
sudo yum update -y

# Install Docker from Amazon Linux repositories
sudo yum install -y docker

# Install Docker Compose (standalone)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ec2-user

# Verify installation
docker --version
docker-compose --version

# IMPORTANT: Logout and login again
exit
```

### After Reconnecting:

```bash
# Verify Docker works without sudo
docker ps

# Navigate to project
cd ~/genai-app-on-aws

# Pull latest code
git pull origin main

# Use legacy build (to avoid buildx issues)
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Build and run
docker-compose up -d --build

# Check status
docker-compose ps
```

---

## Method 2: Use Amazon Linux Extras (Alternative)

If Method 1 doesn't work, try this:

```bash
# Install docker using amazon-linux-extras
sudo amazon-linux-extras install docker -y

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start and enable
sudo systemctl start docker
sudo systemctl enable docker

# Add user to group
sudo usermod -aG docker ec2-user

# Logout and login again
exit
```

---

## Method 3: Complete Clean Install Script

Run this all-in-one script:

```bash
#!/bin/bash
# Complete Docker installation for Amazon Linux 2023

# Remove any existing Docker installations
sudo yum remove -y docker docker-client docker-client-latest docker-common \
    docker-latest docker-latest-logrotate docker-logrotate docker-engine \
    docker-compose

# Remove Docker CE repo if it was added
sudo rm -f /etc/yum.repos.d/docker-ce.repo

# Update system
sudo yum update -y

# Install Docker from Amazon Linux repository
sudo yum install -y docker

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
DOCKER_COMPOSE_VERSION="v2.23.0"
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create symlink for docker compose (optional)
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verify installations
echo "Docker version:"
sudo docker --version

echo "Docker Compose version:"
docker-compose --version

echo ""
echo "✅ Installation complete!"
echo ""
echo "⚠️  IMPORTANT: You must logout and login again for group changes to take effect!"
echo ""
echo "After logging back in, run:"
echo "  docker ps"
echo "  cd ~/genai-app-on-aws"
echo "  docker-compose up -d --build"
```

Save this as `install-docker-al2023.sh` and run:

```bash
chmod +x install-docker-al2023.sh
./install-docker-al2023.sh
exit
```

---

## 🧪 Verification Steps

After reconnecting, verify everything works:

```bash
# 1. Docker is installed and running
docker --version
sudo systemctl status docker

# 2. Docker works without sudo
docker ps

# 3. Docker Compose is installed
docker-compose --version

# 4. User is in docker group
groups | grep docker

# If all above work, proceed to run your app
cd ~/genai-app-on-aws
git pull origin main
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
docker-compose up -d --build
```

---

## 📋 Complete Deployment Command Sequence

Copy and paste this entire sequence on your EC2 instance:

```bash
# 1. Clean up and install Docker
sudo yum remove docker docker-compose -y 2>/dev/null || true
sudo rm -f /etc/yum.repos.d/docker-ce.repo
sudo yum update -y
sudo yum install -y docker

# 2. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# 4. Add user to group
sudo usermod -aG docker ec2-user

# 5. Verify (with sudo, since we haven't logged out yet)
sudo docker --version
docker-compose --version

echo ""
echo "✅ Docker installed successfully!"
echo "⚠️  Now you MUST logout and login again!"
echo ""

# 6. Logout
exit
```

**After reconnecting:**

```bash
# 1. Verify Docker works
docker ps

# 2. Clone/update repository
cd ~
if [ -d "genai-app-on-aws" ]; then
    cd genai-app-on-aws
    git pull origin main
else
    git clone https://github.com/baluragala/genai-app-on-aws.git
    cd genai-app-on-aws
fi

# 3. Configure environment
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Edit .env and add your OPENAI_API_KEY:"
    echo "nano .env"
else
    echo "✅ .env file exists"
fi

# 4. Set legacy build mode
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# 5. Build and run
docker-compose up -d --build

# 6. Check status
docker-compose ps

# 7. View logs
docker-compose logs -f
```

---

## 🎯 Why This Works

| Issue | Why Previous Failed | Why This Works |
|-------|-------------------|----------------|
| **Repository** | CentOS repo doesn't support AL2023 | Uses Amazon Linux native repos |
| **Docker packages** | docker-ce not available | Uses `docker` package from Amazon |
| **Buildx** | Old version in repos | Use legacy build mode |
| **Compose** | Need to install separately | Install from GitHub releases |

---

## 🔍 Understanding Amazon Linux 2023

Amazon Linux 2023 is **NOT** based on CentOS. It's based on Fedora. Key differences:

- Uses `dnf` (though `yum` is aliased to it)
- Has its own package repositories
- Doesn't support CentOS or RHEL repos directly
- Docker is available in AL2023 repos as `docker` package

**DO NOT** try to add CentOS, RHEL, or Fedora Docker repos to AL2023!

---

## 🐛 Troubleshooting

### If Docker install fails:

```bash
# Check what's available
sudo yum search docker

# Try extras (if available)
sudo amazon-linux-extras list | grep docker
sudo amazon-linux-extras install docker

# Check system version
cat /etc/os-release
```

### If still having issues:

```bash
# Check repository configuration
sudo yum repolist

# Remove any Docker CE repos
sudo rm -f /etc/yum.repos.d/docker*.repo

# Clean yum cache
sudo yum clean all

# Try again
sudo yum install docker -y
```

---

## ✅ Expected Result

After following these steps:

```bash
$ docker --version
Docker version 20.10.x, build xxxxx

$ docker-compose --version
Docker Compose version v2.23.0

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ cd ~/genai-app-on-aws && docker-compose up -d --build
[+] Building...
[+] Running 2/2
 ✔ Network genai-app-on-aws_rag-network  Created
 ✔ Container rag-application             Started

$ docker-compose ps
NAME                COMMAND                  SERVICE      STATUS      PORTS
rag-application     "streamlit run app.p…"   rag-app      running     0.0.0.0:8501->8501/tcp
```

Access your app: **http://YOUR_EC2_PUBLIC_IP:8501**

---

## 🚀 Quick Reference

**Install Docker:**
```bash
sudo yum install -y docker
sudo systemctl start docker && sudo systemctl enable docker
```

**Install Docker Compose:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Add user to docker group:**
```bash
sudo usermod -aG docker ec2-user
exit  # MUST logout and login
```

**Run application:**
```bash
export DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0
docker-compose up -d --build
```

---

**TL;DR: Use `sudo yum install docker` NOT the CentOS repo for Amazon Linux 2023!** 🎯

