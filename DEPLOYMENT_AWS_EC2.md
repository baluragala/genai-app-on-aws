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

   | Type | Protocol | Port Range | Source | Description |
   |------|----------|------------|--------|-------------|
   | SSH | TCP | 22 | My IP | SSH access |
   | Custom TCP | TCP | 8501 | 0.0.0.0/0 | Streamlit App |
   | HTTP | TCP | 80 | 0.0.0.0/0 | Optional |
   | HTTPS | TCP | 443 | 0.0.0.0/0 | Optional |

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

```bash
# Install Docker
sudo yum install docker -y

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ec2-user to docker group
sudo usermod -aG docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes to take effect
exit
```

**Reconnect to EC2:**
```bash
ssh -i ~/Downloads/rag-app-key.pem ec2-user@YOUR_PUBLIC_IP
```

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

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

### Step 1: Install Git (if not installed)

**Amazon Linux:**
```bash
sudo yum install git -y
```

**Ubuntu:**
```bash
sudo apt install git -y
```

### Step 2: Clone the Repository

```bash
cd ~
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws
```

### Step 3: Verify Files

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

### Step 1: Build and Start Container

```bash
docker-compose up -d --build
```

This will:
- Build the Docker image
- Start the container in detached mode
- Map port 8501

### Step 2: Check Container Status

```bash
docker-compose ps
```

You should see:
```
NAME                COMMAND                  SERVICE      STATUS      PORTS
rag-application     "streamlit run app.p…"   rag-app      running     0.0.0.0:8501->8501/tcp
```

### Step 3: View Logs

```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit logs (container keeps running)

### Step 4: Check if App is Running

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

## 📝 Complete Command Summary

```bash
# 1. Connect to EC2
ssh -i rag-app-key.pem ec2-user@YOUR_PUBLIC_IP

# 2. Update system
sudo yum update -y

# 3. Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# 4. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Install Git
sudo yum install git -y

# 6. Clone repository
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws

# 7. Configure environment
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# 8. Run application
docker-compose up -d --build

# 9. Access application
# Open browser: http://YOUR_PUBLIC_IP:8501
```

---

## ✅ Verification Checklist

- [ ] EC2 instance is running
- [ ] Security group allows port 8501 from 0.0.0.0/0
- [ ] Docker and Docker Compose are installed
- [ ] Repository is cloned
- [ ] .env file has valid OPENAI_API_KEY
- [ ] Docker container is running (`docker-compose ps`)
- [ ] Application is accessible on http://PUBLIC_IP:8501
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

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs: `docker-compose logs -f`
3. Check container status: `docker-compose ps`
4. Verify environment: `cat .env`
5. Review security group settings in AWS Console

---

**Deployment Complete!** 🚀

Your RAG Application is now live on AWS EC2!

