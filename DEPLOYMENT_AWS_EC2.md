# AWS EC2 Deployment Guide

## Complete step-by-step guide to deploy the RAG Application on AWS EC2

---

## 📋 Prerequisites

- AWS Account with EC2 access
- OpenAI API Key
- SSH client (Terminal on Mac/Linux, PuTTY on Windows)

---

## 🚀 Part 1: Create EC2 Instance

### Step 1: Launch EC2 Instance

1. **Login to AWS Console**

   - Go to https://console.aws.amazon.com/
   - Navigate to EC2 Dashboard

2. **Click "Launch Instance"**

3. **Configure Instance:**

   **Name and Tags:**

   ```
   Name: rag-application-server
   ```

   **Application and OS Images (Amazon Machine Image):**

   ```
   AMI: Amazon Linux 2023 AMI
   Architecture: 64-bit (x86)
   ```

   Alternative: Ubuntu Server 22.04 LTS

   **Instance Type:**

   ```
   Instance Type: t3.medium
   vCPUs: 2
   Memory: 4 GiB
   ```

   **Key Pair (login):**

   - Click "Create new key pair" if you don't have one

   ```
   Key pair name: rag-app-key
   Key pair type: RSA
   Private key file format: .pem (for Mac/Linux) or .ppk (for Windows)
   ```

   - Download and save the key pair file securely

   **Network Settings:**

   - Click "Edit" to configure security group
   - Create security group with following rules:

   | Type       | Protocol | Port Range | Source    | Description   |
   | ---------- | -------- | ---------- | --------- | ------------- |
   | SSH        | TCP      | 22         | My IP     | SSH access    |
   | Custom TCP | TCP      | 8501       | 0.0.0.0/0 | Streamlit App |
   | HTTP       | TCP      | 80         | 0.0.0.0/0 | Optional      |
   | HTTPS      | TCP      | 443        | 0.0.0.0/0 | Optional      |

   **Configure Storage:**

   ```
   Size: 20 GiB
   Volume Type: gp3
   ```

4. **Click "Launch Instance"**

5. **Wait for Instance to Start**
   - Status should show "Running"
   - Note down the **Public IPv4 Address**

---

## 🔧 Part 2: Connect to EC2 Instance

### Step 1: Set Key Pair Permissions (Mac/Linux)

```bash
chmod 400 ~/Downloads/rag-app-key.pem
```

### Step 2: Connect via SSH

**For Amazon Linux 2023:**

```bash
ssh -i ~/Downloads/rag-app-key.pem ec2-user@YOUR_PUBLIC_IP
```

**For Ubuntu:**

```bash
ssh -i ~/Downloads/rag-app-key.pem ubuntu@YOUR_PUBLIC_IP
```

Replace `YOUR_PUBLIC_IP` with your EC2 instance's public IP address.

### Step 3: Update System

**Amazon Linux 2023:**

```bash
sudo yum update -y
```

**Ubuntu:**

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🐳 Part 3: Install Docker

### For Amazon Linux 2023:

⚠️ **IMPORTANT**: For Amazon Linux 2023, use the **native package repository**, NOT Docker CE repository!

```bash
# Clean up any previous installation attempts
sudo yum remove docker docker-compose -y 2>/dev/null || true
sudo rm -f /etc/yum.repos.d/docker-ce.repo

# Update system
sudo yum update -y

# Install Docker from Amazon Linux repository
sudo yum install -y docker

# Install Git (we'll need this later)
sudo yum install -y git

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ec2-user to docker group
sudo usermod -aG docker ec2-user

# Install Docker Compose (standalone binary)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation (using sudo for now)
sudo docker --version
docker-compose --version

echo ""
echo "✅ Docker installed successfully!"
echo "⚠️  IMPORTANT: You MUST logout and login again for group changes!"
echo ""

# Logout and login again for group changes to take effect
exit
```

**Reconnect to EC2:**

```bash
ssh -i ~/Downloads/rag-app-key.pem ec2-user@YOUR_PUBLIC_IP
```

**Verify Installation (WITHOUT sudo):**

```bash
# This should work without sudo now
docker --version
docker ps

# Check Docker Compose
docker-compose --version
```

If `docker ps` works without sudo, you're ready to proceed!

### For Ubuntu:

```bash
# Install Docker
sudo apt install docker.io -y

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
exit
```

---

## 📦 Part 4: Clone Repository

### Step 1: Clone the Repository

Git is already installed from Part 3.

```bash
cd ~
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws
```

### Step 2: Verify Files

```bash
ls -la
```

You should see:

```
app.py
docker-compose.yml
Dockerfile
src/
.env.example
README.md
DEPLOYMENT_AWS_EC2.md
...
```

---

## ⚙️ Part 5: Configure Environment

### Step 1: Create .env File

```bash
cp .env.example .env
```

### Step 2: Edit .env File

```bash
nano .env
```

Update with your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
APP_NAME=RAG Application
LOG_LEVEL=INFO
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

### Step 3: Update docker-compose.yml for Public Access

```bash
nano docker-compose.yml
```

Verify the ports section looks like this:

```yaml
ports:
  - "8501:8501"
```

This maps port 8501 on the EC2 instance to port 8501 in the container.

---

## 🚀 Part 6: Run the Application

### Step 1: Set Legacy Build Mode

To avoid Docker Buildx version issues, set these environment variables:

```bash
# Use legacy build mode (avoids buildx requirement)
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Optional: Make it permanent
echo 'export DOCKER_BUILDKIT=0' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=0' >> ~/.bashrc
```

### Step 2: Build and Start Container

```bash
docker-compose up -d --build
```

This will:

- Build the Docker image using legacy build
- Start the container in detached mode
- Map port 8501

**Note:** First build may take 3-5 minutes. Be patient!

### Step 3: Check Container Status

```bash
docker-compose ps
```

You should see:

```
NAME                COMMAND                  SERVICE      STATUS      PORTS
rag-application     "streamlit run app.p…"   rag-app      running     0.0.0.0:8501->8501/tcp
```

### Step 4: View Logs

```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit logs (container keeps running)

### Step 5: Check if App is Running

```bash
curl http://localhost:8501
```

You should see HTML output.

---

## 🌐 Part 7: Access the Application

### Open in Browser

Navigate to:

```
http://YOUR_EC2_PUBLIC_IP:8501
```

Replace `YOUR_EC2_PUBLIC_IP` with your actual EC2 public IP address.

**Example:**

```
http://54.123.45.67:8501
```

You should see the RAG Application interface!

---

## 🛠️ Management Commands

### View Logs

```bash
docker-compose logs -f
```

### Stop Application

```bash
docker-compose down
```

### Restart Application

```bash
docker-compose restart
```

### Stop and Remove Everything

```bash
docker-compose down -v
```

### Rebuild and Restart

```bash
docker-compose down
docker-compose up -d --build
```

### Check Application Status

```bash
docker-compose ps
docker-compose logs --tail=50
```

### Access Container Shell

```bash
docker-compose exec rag-app /bin/bash
```

---

## 🔒 Security Best Practices

### 1. Restrict SSH Access

Update security group to allow SSH only from your IP:

```
Type: SSH
Port: 22
Source: My IP (not 0.0.0.0/0)
```

### 2. Use HTTPS (Optional but Recommended)

For production, set up HTTPS with:

- AWS Application Load Balancer with SSL certificate
- Or use Nginx reverse proxy with Let's Encrypt

### 3. Protect Environment Variables

```bash
# Set proper permissions on .env file
chmod 600 .env
```

### 4. Regular Updates

```bash
# Update system regularly
sudo yum update -y  # Amazon Linux
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Update Docker images
docker-compose pull
docker-compose up -d
```

---

## 📊 Monitoring

### Check System Resources

```bash
# CPU and Memory usage
htop

# If htop not installed:
sudo yum install htop -y  # Amazon Linux
sudo apt install htop -y  # Ubuntu

# Disk usage
df -h

# Docker stats
docker stats
```

### Check Application Health

```bash
# Health check endpoint
curl http://localhost:8501/_stcore/health

# Container logs
docker-compose logs --tail=100 rag-app
```

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to Docker daemon"

**Solution:**

```bash
# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (if not done)
sudo usermod -aG docker ec2-user

# MUST logout and login again!
exit
```

### Problem: "compose build requires buildx 0.17 or later"

**Solution:**

```bash
# Use legacy build mode
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Then run docker-compose
docker-compose up -d --build
```

### Problem: "Failed to download metadata for repo 'docker-ce-stable'"

**Solution:**

This means you tried to use CentOS Docker repo on Amazon Linux 2023. Remove it:

```bash
# Remove the incompatible repository
sudo rm -f /etc/yum.repos.d/docker-ce.repo

# Install from Amazon Linux native repos
sudo yum install docker -y
```

### Problem: "permission denied while trying to connect to Docker daemon"

**Solution:**

```bash
# Verify you're in docker group
groups

# If docker is not in the list, add yourself:
sudo usermod -aG docker ec2-user

# MUST logout and login again
exit
```

### Problem: Can't connect to EC2

**Solution:**

1. Check security group has port 8501 open
2. Verify EC2 instance is running
3. Check public IP address is correct
4. Ensure you're using HTTP not HTTPS

### Problem: Container won't start

**Solution:**

```bash
# Check logs
docker-compose logs

# Check .env file
cat .env | grep OPENAI_API_KEY

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Problem: Out of memory

**Solution:**

```bash
# Check memory usage
free -h

# Restart container
docker-compose restart

# Consider upgrading to larger instance type
```

### Problem: Port 8501 not accessible

**Solution:**

```bash
# Check if port is listening
sudo netstat -tlnp | grep 8501

# Check Docker port mapping
docker-compose ps

# Verify security group rules in AWS Console
```

### Problem: Application errors

**Solution:**

```bash
# View detailed logs
docker-compose logs -f rag-app

# Check inside container
docker-compose exec rag-app /bin/bash
ls -la
cat .env
```

---

## 💰 Cost Optimization

### EC2 Instance Pricing (Approximate)

- **t3.medium**: ~$0.0416/hour = ~$30/month (On-Demand)
- Use Reserved Instances for ~40% savings
- Use Spot Instances for ~70% savings (if acceptable)

### Stop Instance When Not in Use

```bash
# Stop EC2 instance from AWS Console or CLI
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start again when needed
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

---

## 🔄 Updating the Application

### Pull Latest Changes

```bash
cd ~/genai-app-on-aws

# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

## 📝 Complete Command Summary (Amazon Linux 2023)

### First SSH Session:

```bash
# 1. Connect to EC2
ssh -i rag-app-key.pem ec2-user@YOUR_PUBLIC_IP

# 2. Clean and update system
sudo yum remove docker docker-compose -y 2>/dev/null || true
sudo rm -f /etc/yum.repos.d/docker-ce.repo
sudo yum update -y

# 3. Install Docker and Git
sudo yum install -y docker git

# 4. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# 6. Add user to docker group
sudo usermod -aG docker ec2-user

# 7. Verify
sudo docker --version
docker-compose --version

# 8. Logout (REQUIRED!)
exit
```

### Second SSH Session (After Reconnecting):

```bash
# 1. Reconnect to EC2
ssh -i rag-app-key.pem ec2-user@YOUR_PUBLIC_IP

# 2. Verify Docker works without sudo
docker ps

# 3. Clone repository
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws

# 4. Configure environment
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY and save

# 5. Set legacy build mode
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# 6. Build and run application
docker-compose up -d --build

# 7. Check status
docker-compose ps

# 8. View logs
docker-compose logs -f

# 9. Access application
# Open browser: http://YOUR_PUBLIC_IP:8501
```

---

## ✅ Verification Checklist

- [ ] EC2 instance is running (check AWS Console)
- [ ] Security group allows port 22 from My IP (SSH)
- [ ] Security group allows port 8501 from 0.0.0.0/0 (App)
- [ ] Connected to EC2 via SSH
- [ ] Docker installed: `docker --version` works WITHOUT sudo
- [ ] Docker Compose installed: `docker-compose --version` shows v2.23.0+
- [ ] Repository cloned: `ls ~/genai-app-on-aws` shows files
- [ ] .env file configured: `grep OPENAI_API_KEY ~/genai-app-on-aws/.env` shows valid key
- [ ] Legacy build mode set: `echo $DOCKER_BUILDKIT` shows 0
- [ ] Docker container running: `docker-compose ps` shows "running"
- [ ] Application accessible: Browser opens http://PUBLIC_IP:8501
- [ ] Can upload documents and ask questions

---

## 🎉 Success!

Your RAG Application is now deployed on AWS EC2 and accessible via:

**http://YOUR_EC2_PUBLIC_IP:8501**

### What You Can Do Now:

1. **Upload Documents**: PDF, TXT files
2. **Ask Questions**: Get AI-powered answers
3. **Share Access**: Share the public URL with team members
4. **Monitor**: Check logs and resource usage
5. **Scale**: Upgrade instance type if needed

---

## 📚 Additional Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Project README](README.md)
- [Architecture Documentation](ARCHITECTURE.md)

---

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Review logs: `docker-compose logs -f`
3. Check container status: `docker-compose ps`
4. Verify environment: `cat .env | grep OPENAI_API_KEY`
5. Verify Docker works: `docker ps` (without sudo)
6. Check legacy build: `echo $DOCKER_BUILDKIT` (should be 0)
7. Review security group settings in AWS Console

### Additional Troubleshooting Resources

- **Docker Issues**: See `EC2_DOCKER_FIX.md`
- **Buildx Issues**: See `BUILDX_FIX.md`
- **Amazon Linux 2023 Specific**: See `AMAZON_LINUX_2023_DOCKER.md`

---

**Deployment Complete!** 🚀

Your RAG Application is now live on AWS EC2!
