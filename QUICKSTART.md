# Quick Start Guide

## 🎯 Goal
Get the RAG application running in under 5 minutes!

## ⚡ Option 1: Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Steps

1. **Clone and navigate to the project**
```bash
cd /path/to/genai-app-on-aws
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Run the application**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

4. **Access the app**
Open `http://localhost:8501` in your browser

**That's it!** 🎉

---

## 💻 Option 2: Local Development

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Steps

1. **Navigate to the project**
```bash
cd /path/to/genai-app-on-aws
```

2. **Run setup script**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Edit .env file**
```bash
nano .env  # or use your favorite editor
# Add your OPENAI_API_KEY
```

4. **Run the application**
```bash
chmod +x run.sh
./run.sh
```

5. **Access the app**
Open `http://localhost:8501` in your browser

**You're all set!** 🎉

---

## 🧪 Test the Application

1. **Upload a document**
   - Click "Browse files" in the sidebar
   - Select a PDF, TXT, or DOCX file
   - Click "Process Documents"

2. **Ask a question**
   - Type a question in the text box
   - Click "Ask"
   - View the AI-generated answer

3. **Try these sample questions**
   - "What is the main topic of this document?"
   - "Summarize the key points"
   - "What are the conclusions?"

---

## 🛠️ Troubleshooting

### Docker not starting?
```bash
# Check if port 8501 is available
lsof -i :8501

# If something is using it, stop it or change the port in docker-compose.yml
```

### Missing OpenAI API Key?
```bash
# Make sure .env file has your key
cat .env | grep OPENAI_API_KEY
```

### Dependencies issues?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore configuration options in `.env.example`
- Check out the source code in `src/` directory

---

**Need help?** Open an issue or check the troubleshooting section in README.md

