# 🔄 How to Restart the Application

## The Issue

You were seeing the error because the Streamlit app was running with **old packages** before the fix was applied. Streamlit needs to be restarted to use the updated dependencies.

## ✅ I've Stopped the Old Process

The old Streamlit process has been terminated. Now you need to start it fresh.

## 🚀 How to Start the App (Choose One)

### Method 1: Simple Restart (Recommended)

```bash
cd /Users/balakrishna/Training/gen-ai/genai-app-on-aws
source venv/bin/activate
streamlit run app.py
```

### Method 2: Use the Run Script

```bash
cd /Users/balakrishna/Training/gen-ai/genai-app-on-aws
./run.sh
```

### Method 3: Use START_APP Script

```bash
cd /Users/balakrishna/Training/gen-ai/genai-app-on-aws
./START_APP.sh
```

## 📝 Important Notes

1. **Always activate the virtual environment first**
   ```bash
   source venv/bin/activate
   ```

2. **Check your OpenAI API key is set**
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

3. **If you see the error again**, it means:
   - Virtual environment wasn't activated
   - Old cache needs clearing: `rm -rf ~/.streamlit`

## 🧪 Verify It's Working

After starting, you should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

Open that URL and the app should work without errors!

## 🐛 If You Still See Errors

1. **Stop all Python processes**
   ```bash
   pkill -f "streamlit run"
   ```

2. **Clear caches**
   ```bash
   rm -rf ~/.streamlit
   rm -rf __pycache__
   find . -name "*.pyc" -delete
   ```

3. **Start fresh**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

## ✅ Expected Behavior

Once restarted with new packages:
- ✅ No more "proxies" error
- ✅ No more Pydantic ForwardRef errors
- ✅ App loads successfully
- ✅ Can upload and process documents
- ✅ Can ask questions and get answers

## 💡 Pro Tip

When making package updates in the future:
1. Always stop the Streamlit server first
2. Update packages
3. Restart Streamlit

This ensures the new packages are loaded!

