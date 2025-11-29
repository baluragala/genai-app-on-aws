# 🔧 EC2 Docker Issues - Quick Fix Guide

## Issues You're Seeing

1. ⚠️ **Warning about `version`**: The `version` field in docker-compose.yml is obsolete
2. ❌ **Docker daemon not running**: Cannot connect to Docker daemon

---

## ✅ Solution 1: Remove Version Warning (FIXED)

The `version: '3.8'` line has been removed from `docker-compose.yml`. 

After you pull the latest code, this warning will be gone.

---

## ✅ Solution 2: Fix Docker Daemon Issue

The issue is that **Docker is not running** or **you don't have permission** to access it.

### Quick Fix Commands:

```bash
# 1. Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 2. Check if Docker is running
sudo systemctl status docker

# 3. Add yourself to docker group (if not already done)
sudo usermod -aG docker $USER

# 4. IMPORTANT: Logout and login again
exit
```

### After Reconnecting:

```bash
# Reconnect to EC2
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Navigate to project
cd ~/genai-app-on-aws

# Pull latest changes (to get docker-compose.yml fix)
git pull origin main

# Verify Docker works WITHOUT sudo
docker ps

# Now run your application
docker-compose up -d --build
```

---

## 📋 Complete Step-by-Step Fix

### Step 1: Ensure Docker is Running

```bash
# Check Docker status
sudo systemctl status docker

# If not running, start it
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 2: Fix Permissions

```bash
# Add current user to docker group
sudo usermod -aG docker $USER

# Verify group membership
groups $USER
```

You should see `docker` in the output.

### Step 3: Apply Group Changes

**CRITICAL:** You MUST logout and login again for group changes to take effect!

```bash
# Logout
exit
```

Then reconnect:

```bash
# For Amazon Linux
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# For Ubuntu
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### Step 4: Verify Docker Works

```bash
# This should work WITHOUT sudo now
docker ps

# If you still get permission denied, check:
ls -la /var/run/docker.sock
groups
```

### Step 5: Update Code and Run

```bash
cd ~/genai-app-on-aws

# Pull latest changes (fixes version warning)
git pull origin main

# Run application
docker-compose up -d --build
```

---

## 🧪 Verification Tests

Run these commands to verify everything is working:

```bash
# 1. Docker daemon is running
sudo systemctl status docker
# Should show: active (running)

# 2. You can run docker commands without sudo
docker ps
# Should NOT give permission error

# 3. Docker Compose is installed
docker-compose --version
# Should show version number

# 4. Application is running
docker-compose ps
# Should show rag-application container running
```

---

## 🐛 Still Having Issues?

### Issue: "permission denied while trying to connect to Docker daemon"

**Solution:**
```bash
# Verify you're in docker group
groups

# If docker is not listed, add yourself:
sudo usermod -aG docker $USER

# MUST logout and login again!
exit
```

### Issue: "Cannot connect to the Docker daemon"

**Solution:**
```bash
# Check if Docker daemon is running
sudo systemctl status docker

# If not running, start it
sudo systemctl start docker

# Enable it to start on boot
sudo systemctl enable docker
```

### Issue: "docker: command not found"

**Solution:**
```bash
# Install Docker
sudo yum install docker -y  # Amazon Linux
sudo apt install docker.io -y  # Ubuntu

# Start and enable
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 📝 Common Mistakes

❌ **Not logging out and back in** after adding user to docker group
   - Group membership doesn't take effect until you logout/login

❌ **Docker service not started** after installation
   - Always run `sudo systemctl start docker`

❌ **Using sudo with docker commands** after adding to group
   - If configured correctly, you shouldn't need sudo

---

## ✅ Expected Result

After following these steps, you should see:

```bash
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker-compose up -d --build
[+] Building...
[+] Running 2/2
 ✔ Network genai-app-on-aws_rag-network  Created
 ✔ Container rag-application             Started

$ docker-compose ps
NAME                COMMAND                  SERVICE      STATUS      PORTS
rag-application     "streamlit run app.p…"   rag-app      running     0.0.0.0:8501->8501/tcp
```

---

## 🚀 Quick Copy-Paste Solution

If you want to fix everything at once, run this:

```bash
# Start Docker and add permissions
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Logout (MUST DO THIS!)
exit

# After reconnecting:
cd ~/genai-app-on-aws
git pull origin main
docker ps  # Should work without sudo
docker-compose up -d --build
```

---

## 📞 Need More Help?

If issues persist:

1. Check Docker installation: `which docker`
2. Check Docker daemon: `sudo systemctl status docker`
3. Check permissions: `ls -la /var/run/docker.sock`
4. Check groups: `groups`
5. View logs: `sudo journalctl -u docker -n 50`

---

**Remember: The most common issue is forgetting to logout and login again after adding user to docker group!** 🔑

