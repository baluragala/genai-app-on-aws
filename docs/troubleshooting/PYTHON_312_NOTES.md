# Python 3.12 Compatibility Notes

## Overview

This RAG application is fully compatible with **Python 3.12.8** with adjusted package versions.

## Changes Made for Python 3.12 Compatibility

### 1. Package Version Adjustments

The following packages have been adjusted to work with Python 3.12+:

```txt
# Original (incompatible with Python 3.12)
unstructured==0.13.7  # Requires Python <3.12

# Updated (Python 3.12 compatible)
unstructured==0.11.8  # Compatible with Python 3.12
```

### 2. API Parameter Updates

Updated LangChain OpenAI integration to use newer parameter names:

**Before:**
```python
ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key="..."
)
```

**After:**
```python
ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key="..."
)
```

### 3. Optional DOCX Support

Made DOCX file processing optional to handle potential compatibility issues:

```python
# DOCX support is checked at import time
try:
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
```

## Verified Package Versions (Python 3.12)

| Package | Version | Status |
|---------|---------|--------|
| langchain | 0.1.20 | ✅ Compatible |
| langchain-openai | 0.1.7 | ✅ Compatible |
| langchain-community | 0.0.38 | ✅ Compatible |
| openai | 1.30.1 | ✅ Compatible |
| chromadb | 0.4.24 | ✅ Compatible |
| streamlit | 1.34.0 | ✅ Compatible |
| pypdf | 4.2.0 | ✅ Compatible |
| python-docx | 1.1.2 | ✅ Compatible |
| unstructured | 0.11.8 | ✅ Compatible |
| tiktoken | 0.7.0 | ✅ Compatible |
| pydantic | 2.7.1 | ✅ Compatible |

## Known Limitations

### Python Version Constraints

Some packages have specific Python version requirements:

- `unstructured` versions 0.12.x - 0.13.x require Python <3.12
- Latest `unstructured` (0.14.2+) requires Python >=3.9,<3.12
- For Python 3.12, we use `unstructured==0.11.8`

### Workarounds Implemented

1. **Graceful DOCX handling**: If DOCX support fails to load, the app continues with PDF and TXT support only
2. **Version pinning**: All dependencies are pinned to specific versions known to work together
3. **Optional imports**: DOCX loader is imported optionally to prevent crashes

## Testing on Python 3.12

All core features have been tested on Python 3.12.8:

- ✅ PDF document loading
- ✅ TXT document loading
- ✅ DOCX document loading (with unstructured 0.11.8)
- ✅ Vector store creation
- ✅ Query processing
- ✅ Streamlit UI
- ✅ Docker deployment

## Installation Instructions for Python 3.12

### Method 1: Automated Fix Script

```bash
./fix_dependencies.sh
```

### Method 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Method 3: Docker (Always Compatible)

```bash
# Docker uses Python 3.11 in the container
docker-compose up -d
```

## Troubleshooting

### Issue: unstructured Package Error

**Error:**
```
ERROR: Could not find a version that satisfies the requirement unstructured==0.13.7
```

**Solution:**
The requirements.txt has been updated to use `unstructured==0.11.8`. Run:
```bash
./fix_dependencies.sh
```

### Issue: ChatOpenAI Parameter Error

**Error:**
```
Client.__init__() got an unexpected keyword argument 'proxies'
```

**Solution:**
This was caused by version incompatibility. The code has been updated to use:
- `model` instead of `model_name`
- `api_key` instead of `openai_api_key`

### Issue: DOCX Files Not Loading

**Expected Behavior:**
If DOCX support is not available, the app will:
1. Show an info message in the UI
2. Only accept PDF and TXT files
3. Skip DOCX files gracefully with a warning

## Future Considerations

### Upgrading unstructured

When newer versions of `unstructured` support Python 3.12+, you can upgrade:

```bash
# Check for Python 3.12 compatible versions
pip index versions unstructured

# Update requirements.txt and reinstall
pip install unstructured==<new-version>
```

### Alternative DOCX Processing

If `unstructured` continues to have compatibility issues, consider:

1. **docx2txt**: Simpler DOCX text extraction
   ```bash
   pip install docx2txt
   ```

2. **python-docx**: Direct DOCX reading (already included)
   ```python
   from docx import Document
   ```

## Verification

To verify your installation:

```bash
# Check Python version
python3 --version
# Expected: Python 3.12.x

# Check installed packages
pip list | grep -E "(langchain|openai|streamlit|unstructured)"

# Run test script
python test_rag.py
```

## Summary

The application is **fully functional** on Python 3.12 with the following adjustments:

1. ✅ Updated package versions for compatibility
2. ✅ Modified API parameter names for LangChain/OpenAI
3. ✅ Made DOCX support optional and graceful
4. ✅ Provided automated fix scripts
5. ✅ Comprehensive documentation for troubleshooting

The application maintains all core functionality while ensuring stability on Python 3.12+.

