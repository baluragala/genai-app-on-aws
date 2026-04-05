# RAG Application

A production-ready Retrieval-Augmented Generation (RAG) application built with LangChain, OpenAI, and Streamlit.

## 🌟 Features

- **Document Processing**: Support for PDF, TXT, and DOCX files
- **Semantic Search**: Powered by OpenAI embeddings and Chroma vector database
- **Interactive UI**: Beautiful Streamlit interface for document upload and querying
- **In-Memory Vector Store**: Fast Chroma database running in memory
- **Logging**: Comprehensive logging with color support
- **Docker Support**: Fully containerized application
- **Environment-based Configuration**: Flexible configuration using environment variables

## 🏗️ Architecture

```
┌─────────────┐
│  Streamlit  │  ← User Interface
└──────┬──────┘
       │
┌──────▼──────┐
│ RAG Engine  │  ← Core Logic
└──────┬──────┘
       │
┌──────▼──────┐
│  LangChain  │  ← Framework
└──────┬──────┘
       │
    ┌──▼───┬────────────┬──────────┐
    │      │            │          │
┌───▼──┐ ┌─▼────┐ ┌────▼────┐ ┌──▼────┐
│OpenAI│ │Chroma│ │Document │ │Logging│
│ LLM  │ │Vector│ │Loaders  │ │System │
└──────┘ │Store │ └─────────┘ └───────┘
         └──────┘
```

## 📋 Prerequisites

- Python 3.11+
- OpenAI API Key
- Docker and Docker Compose (for containerized deployment)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
cd /path/to/genai-app-on-aws
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Access the application**
Open your browser and navigate to `http://localhost:8501`

### Docker Deployment

1. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the application**
Open your browser and navigate to `http://localhost:8501`

4. **View logs**
```bash
docker-compose logs -f rag-app
```

5. **Stop the application**
```bash
docker-compose down
```

## 📁 Project Structure

```
genai-app-on-aws/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   └── rag_engine.py        # RAG core logic
├── docs/                    # All Markdown documentation (see docs/README.md)
├── logs/                    # Application logs
├── data/                    # Data directory (optional)
├── app.py                   # Streamlit application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker ignore rules
└── README.md               # This file
```

For guides, deployment, and troubleshooting, see **[docs/README.md](docs/README.md)**.

## 🔧 Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | **Required** |
| `APP_NAME` | Application name | RAG Application |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `MODEL_NAME` | OpenAI model to use | gpt-3.5-turbo |
| `TEMPERATURE` | LLM temperature (0.0-1.0) | 0.7 |
| `MAX_TOKENS` | Maximum tokens in response | 1000 |
| `CHUNK_SIZE` | Document chunk size | 1000 |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 |
| `STREAMLIT_SERVER_PORT` | Streamlit server port | 8501 |

## 📖 Usage

### Uploading Documents

1. Click on the sidebar "Upload Documents" button
2. Select one or more files (PDF, TXT, or DOCX)
3. Click "Process Documents"

### Pasting Text

1. Use the text area in the sidebar
2. Paste your content
3. Click "Process Documents"

### Asking Questions

1. Once documents are processed, enter your question in the text box
2. Optionally check "Show sources" to see the source documents used
3. Click "Ask" to get your answer

### Resetting

Click the "Reset" button in the sidebar to clear all documents and start fresh.

## 🧪 Testing

### Manual Testing

1. Upload a sample document (e.g., a PDF or text file)
2. Ask various questions about the content
3. Verify the answers are relevant and accurate
4. Check the source documents to ensure proper retrieval

### Health Check

The application includes a health check endpoint:
```bash
curl http://localhost:8501/_stcore/health
```

## 📊 Logging

Logs are stored in the `logs/` directory:
- `application.log`: General application logs
- `rag_engine.log`: RAG engine specific logs
- `streamlit_app.log`: Streamlit interface logs

Console output includes colored logs for better readability.

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive API keys
2. **Use environment variables** - For all sensitive configuration
3. **Rotate API keys regularly** - Update your OpenAI API keys periodically
4. **Limit file upload size** - Configure Streamlit's max upload size
5. **Run with least privileges** - Don't run as root in production

## 🐛 Troubleshooting

### OpenAI API Key Error
```
Error: OPENAI_API_KEY is not set
Solution: Set your API key in .env file or environment variables
```

### Import Errors
```
Error: ModuleNotFoundError
Solution: Ensure all dependencies are installed: pip install -r requirements.txt
```

### Docker Build Issues
```
Error: Docker build failed
Solution: Check Docker daemon is running and .env file exists
```

### Port Already in Use
```
Error: Port 8501 is already allocated
Solution: Change STREAMLIT_SERVER_PORT or stop the conflicting service
```

## 🚀 Performance Optimization

1. **Chunk Size**: Adjust `CHUNK_SIZE` based on your document types
2. **Overlap**: Increase `CHUNK_OVERLAP` for better context preservation
3. **Temperature**: Lower `TEMPERATURE` for more deterministic responses
4. **Model Selection**: Use `gpt-4` for better quality, `gpt-3.5-turbo` for speed

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue in the repository.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - RAG framework
- [OpenAI](https://openai.com/) - Language models and embeddings
- [Streamlit](https://streamlit.io/) - Web interface
- [Chroma](https://www.trychroma.com/) - Vector database

---

**Made with ❤️ using LangChain, OpenAI, and Streamlit**

