# 🔧 Docker Buildx Version Fix

## Error Message

```
compose build requires buildx 0.17 or later
```

This means your Docker Buildx plugin is outdated.

---

## ✅ Solution 1: Use Legacy Build (QUICKEST)

Instead of using the new build system, use the legacy Docker build:

```bash
# Set environment variable to use legacy builder
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Now run docker-compose
docker-compose up -d --build
```

### Make it permanent:

```bash
# Add to your shell profile
echo 'export DOCKER_BUILDKIT=0' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=0' >> ~/.bashrc

# Reload
source ~/.bashrc

# Run application
docker-compose up -d --build
```

---

## ✅ Solution 2: Update Docker and Docker Compose (RECOMMENDED)

### For Amazon Linux 2023:

```bash
# Remove old Docker
sudo yum remove docker docker-compose -y

# Install Docker from official repository
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install latest Docker
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ec2-user

# Logout and login again
exit
```

**After reconnecting:**

```bash
# Verify versions
docker --version
docker compose version  # Note: 'compose' not 'docker-compose'

# Use new docker compose (no hyphen)
cd ~/genai-app-on-aws
docker compose up -d --build
```

### For Ubuntu:

```bash
# Remove old versions
sudo apt remove docker docker-compose -y

# Install prerequisites
sudo apt update
sudo apt install ca-certificates curl gnupg -y

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ubuntu

# Logout and login again
exit
```

**After reconnecting:**

```bash
docker --version
docker compose version

cd ~/genai-app-on-aws
docker compose up -d --build  # Note: 'compose' not 'docker-compose'
```

---

## ✅ Solution 3: Update Buildx Only

If you want to keep your current Docker but just update Buildx:

```bash
# Download latest buildx
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/buildx/releases/download/v0.18.0/buildx-v0.18.0.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx

# Make it executable
chmod +x ~/.docker/cli-plugins/docker-buildx

# Verify
docker buildx version
```

Then try again:

```bash
docker-compose up -d --build
```

---

## ✅ Solution 4: Use Pre-built Image (FASTEST)

Skip building entirely by using a simple Dockerfile that doesn't need buildx:

### Option A: Build locally then copy

On your local machine:

```bash
# Build the image
docker build -t rag-app:latest .

# Save to tar
docker save rag-app:latest > rag-app.tar

# Copy to EC2
scp -i your-key.pem rag-app.tar ec2-user@YOUR_EC2_IP:~/
```

On EC2:

```bash
# Load the image
docker load < rag-app.tar

# Modify docker-compose.yml to use pre-built image
# Change 'build:' to 'image: rag-app:latest'

# Run
docker-compose up -d
```

### Option B: Use standard docker build

```bash
# Don't use docker-compose for building
docker build -t rag-application .

# Then just start with docker run
docker run -d \
  --name rag-application \
  -p 8501:8501 \
  -e OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2) \
  --restart unless-stopped \
  rag-application
```

---

## 🎯 Recommended Approach

**For EC2 deployment, use Solution 1 (Legacy Build) as it's the quickest:**

```bash
# On your EC2 instance
cd ~/genai-app-on-aws

# Pull latest code
git pull origin main

# Use legacy build
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Build and run
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 🧪 Verification

After applying any solution, verify it works:

```bash
# Check Docker version
docker --version

# Check if buildx is available (if updated)
docker buildx version

# Check running containers
docker ps

# Check application
curl http://localhost:8501
```

---

## 📋 Quick Comparison

| Solution | Time | Pros | Cons |
|----------|------|------|------|
| Legacy Build | 1 min | Quick, works immediately | Uses older build system |
| Update Docker | 5 min | Modern, best practice | Requires reinstall, logout |
| Update Buildx | 2 min | Just updates plugin | May have dependency issues |
| Pre-built Image | 10 min | No build on EC2 | Extra steps |

---

## 🚀 Complete Quick Fix Commands

Copy and paste this on your EC2 instance:

```bash
# Navigate to project
cd ~/genai-app-on-aws

# Pull latest changes
git pull origin main

# Set legacy build mode
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Build and run
docker-compose up -d --build

# Check status
docker-compose ps

# If running successfully, make it permanent
echo 'export DOCKER_BUILDKIT=0' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=0' >> ~/.bashrc
```

---

## 🔍 Understanding the Issue

**Why this happens:**
- Amazon Linux's default Docker package includes an old version of Buildx
- Docker Compose v2+ requires Buildx 0.17+
- The legacy build system (BuildKit disabled) doesn't need Buildx

**Modern vs Legacy:**
- **Modern (Buildx)**: Faster, parallel builds, better caching
- **Legacy**: Slower but more compatible, works everywhere

**For production:** Update to latest Docker for best performance
**For quick testing:** Use legacy build

---

## 💡 Alternative: Use Docker Compose V1

If you prefer the old docker-compose (with hyphen):

```bash
# Install standalone docker-compose v1
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose version

# Run (this won't complain about buildx)
docker-compose up -d --build
```

---

## ✅ Expected Result

After applying the fix:

```bash
$ docker-compose up -d --build
[+] Building 45.2s (15/15) FINISHED
[+] Running 2/2
 ✔ Network genai-app-on-aws_rag-network  Created
 ✔ Container rag-application             Started

$ docker-compose ps
NAME                COMMAND                  SERVICE      STATUS      PORTS
rag-application     "streamlit run app.p…"   rag-app      running     0.0.0.0:8501->8501/tcp
```

Access your app at: **http://YOUR_EC2_PUBLIC_IP:8501**

---

**TL;DR: Use legacy build mode by setting `DOCKER_BUILDKIT=0` - it's the fastest fix!** 🚀

