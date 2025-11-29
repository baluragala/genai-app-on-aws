# EC2 Deployment - Quick Reference Card

## 🚀 One-Command Deployment

After creating EC2 instance and connecting via SSH, run:

```bash
curl -o- https://raw.githubusercontent.com/baluragala/genai-app-on-aws/main/deploy-ec2.sh | bash
```

## 📋 Manual Deployment - Copy & Paste Commands

### Amazon Linux 2023

```bash
# Update and install dependencies
sudo yum update -y
sudo yum install docker git -y
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and configure
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws
cp .env.example .env

# Edit .env file - ADD YOUR OPENAI_API_KEY
nano .env

# Logout and login again
exit
```

**After reconnecting:**

```bash
cd genai-app-on-aws
docker-compose up -d --build
```

### Ubuntu 22.04

```bash
# Update and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io git -y
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and configure
git clone https://github.com/baluragala/genai-app-on-aws.git
cd genai-app-on-aws
cp .env.example .env

# Edit .env file - ADD YOUR OPENAI_API_KEY
nano .env

# Logout and login again
exit
```

**After reconnecting:**

```bash
cd genai-app-on-aws
docker-compose up -d --build
```

## 🔑 AWS EC2 Setup

### Security Group Rules

| Type | Port | Source | Description |
|------|------|--------|-------------|
| SSH | 22 | My IP | SSH access |
| Custom TCP | 8501 | 0.0.0.0/0 | Streamlit App |

### Instance Configuration

- **Type:** t3.medium
- **vCPUs:** 2
- **Memory:** 4 GiB
- **Storage:** 20 GiB gp3
- **OS:** Amazon Linux 2023 or Ubuntu 22.04

## 🔧 Common Commands

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Restart application
docker-compose restart

# Check status
docker-compose ps

# Rebuild
docker-compose up -d --build

# Update from git
git pull origin main
docker-compose down
docker-compose up -d --build
```

## 🌐 Access Application

```
http://YOUR_EC2_PUBLIC_IP:8501
```

## 🐛 Quick Troubleshooting

```bash
# Check if running
docker-compose ps

# View logs
docker-compose logs --tail=50

# Check port
sudo netstat -tlnp | grep 8501

# Restart
docker-compose restart

# Full restart
docker-compose down && docker-compose up -d --build
```

## 📝 .env Configuration

Required in `.env` file:

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
```

## 💡 Tips

- Always use `exit` and reconnect after adding user to docker group
- Check security group if can't access port 8501
- Use `docker-compose logs -f` to debug issues
- Keep .env file secure (`chmod 600 .env`)

## 📚 Full Documentation

See `DEPLOYMENT_AWS_EC2.md` for complete step-by-step guide.

---

**Quick Access:**
- Documentation: `cat DEPLOYMENT_AWS_EC2.md`
- Automated script: `./deploy-ec2.sh`
- Application URL: `http://PUBLIC_IP:8501`

