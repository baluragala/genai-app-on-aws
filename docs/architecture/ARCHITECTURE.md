# RAG Application Architecture

## Overview

This document provides a comprehensive overview of the RAG (Retrieval-Augmented Generation) application architecture, components, and data flow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                      (Streamlit - app.py)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Document   │  │     Text     │  │    Query     │        │
│  │    Upload    │  │    Input     │  │   Interface  │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
          ┌──────────────────▼──────────────────┐
          │         RAG Engine Core             │
          │       (src/rag_engine.py)           │
          │                                     │
          │  ┌─────────────────────────────┐   │
          │  │  Document Processing        │   │
          │  │  - Load documents           │   │
          │  │  - Text splitting           │   │
          │  │  - Chunk creation           │   │
          │  └────────────┬────────────────┘   │
          │               │                     │
          │  ┌────────────▼────────────────┐   │
          │  │  Vector Store Creation      │   │
          │  │  - Embedding generation     │   │
          │  │  - Chroma DB indexing       │   │
          │  └────────────┬────────────────┘   │
          │               │                     │
          │  ┌────────────▼────────────────┐   │
          │  │  Query Processing           │   │
          │  │  - Semantic search          │   │
          │  │  - Context retrieval        │   │
          │  │  - Answer generation        │   │
          │  └─────────────────────────────┘   │
          └──────────────┬──────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼─────┐ ┌───────▼────────┐
│   LangChain    │ │  Chroma  │ │   OpenAI API   │
│   Framework    │ │  Vector  │ │                │
│                │ │  Store   │ │  - Embeddings  │
│  - Chains      │ │          │ │  - LLM (GPT)   │
│  - Retrievers  │ │ In-memory│ │                │
│  - Loaders     │ │          │ │                │
└────────────────┘ └──────────┘ └────────────────┘
```

## Component Details

### 1. User Interface Layer (`app.py`)

**Responsibility**: Provide interactive web interface for users

**Key Features**:
- File upload (PDF, TXT, DOCX)
- Text input area
- Chat interface
- Document processing controls
- Source document display

**Technologies**:
- Streamlit (Python web framework)
- Session state management

### 2. Configuration Module (`src/config.py`)

**Responsibility**: Centralized configuration management

**Key Features**:
- Environment variable loading
- Configuration validation
- Default value management
- Path configuration

**Configuration Parameters**:
- OpenAI API key
- Model settings (name, temperature, max tokens)
- Chunk settings (size, overlap)
- Application settings

### 3. Logging Module (`src/logger.py`)

**Responsibility**: Comprehensive logging system

**Key Features**:
- Color-coded console output
- File-based logging
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- Separate loggers for different components

**Log Files**:
- `logs/application.log`: General application logs
- `logs/rag_engine.log`: RAG engine specific logs
- `logs/streamlit_app.log`: UI interaction logs

### 4. RAG Engine (`src/rag_engine.py`)

**Responsibility**: Core RAG functionality

**Key Components**:

#### A. Document Loading
```python
Supported formats:
- PDF: PyPDFLoader
- TXT: TextLoader
- DOCX: UnstructuredWordDocumentLoader
```

#### B. Text Processing
```python
Process:
1. Split documents into chunks
2. Configure chunk size and overlap
3. Maintain context across chunks
```

#### C. Vector Store Creation
```python
Process:
1. Generate embeddings (OpenAI)
2. Store in Chroma (in-memory)
3. Create retrieval interface
```

#### D. Query Processing
```python
Process:
1. Embed user query
2. Semantic search in vector store
3. Retrieve top-k relevant chunks
4. Generate answer with LLM
5. Return answer + sources
```

## Data Flow

### Document Processing Flow

```
┌──────────────┐
│ User uploads │
│  document    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  File saved  │
│ temporarily  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Document   │
│    loaded    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Split into   │
│   chunks     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Generate    │
│  embeddings  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Store in     │
│   Chroma     │
└──────────────┘
```

### Query Processing Flow

```
┌──────────────┐
│ User enters  │
│   question   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Embed      │
│   query      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Semantic    │
│   search     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Retrieve    │
│  top chunks  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  LLM with    │
│  context     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Generate    │
│   answer     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Display to  │
│    user      │
└──────────────┘
```

## Technology Stack

### Core Framework
- **LangChain**: RAG orchestration and chain management
- **Python 3.11**: Primary programming language

### AI/ML
- **OpenAI GPT-3.5/4**: Language model for generation
- **OpenAI Embeddings**: Text embedding generation
- **Chroma**: Vector database (in-memory)

### Frontend
- **Streamlit**: Web application framework
- **Streamlit Components**: UI elements

### Document Processing
- **PyPDF**: PDF document parsing
- **python-docx**: Word document parsing
- **unstructured**: Additional document format support

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

### Utilities
- **python-dotenv**: Environment variable management
- **colorlog**: Enhanced logging with colors
- **tiktoken**: Token counting for OpenAI

## Deployment Architectures

### Local Development

```
┌──────────────────────────────────┐
│      Developer Machine           │
│                                  │
│  ┌────────────────────────────┐ │
│  │  Python Virtual Env        │ │
│  │                            │ │
│  │  ┌──────────────────────┐ │ │
│  │  │   Streamlit App      │ │ │
│  │  │   (Port 8501)        │ │ │
│  │  └──────────────────────┘ │ │
│  │                            │ │
│  │  ┌──────────────────────┐ │ │
│  │  │   RAG Engine         │ │ │
│  │  │   (In-memory)        │ │ │
│  │  └──────────────────────┘ │ │
│  └────────────────────────────┘ │
└──────────────┬───────────────────┘
               │
               ▼
      ┌─────────────────┐
      │   OpenAI API    │
      │   (Cloud)       │
      └─────────────────┘
```

### Docker Deployment

```
┌──────────────────────────────────────┐
│         Docker Host                  │
│                                      │
│  ┌────────────────────────────────┐ │
│  │    Docker Container            │ │
│  │    (rag-application)           │ │
│  │                                │ │
│  │  ┌──────────────────────────┐ │ │
│  │  │   Streamlit App          │ │ │
│  │  │   (Port 8501)            │ │ │
│  │  └──────────────────────────┘ │ │
│  │                                │ │
│  │  ┌──────────────────────────┐ │ │
│  │  │   RAG Engine             │ │ │
│  │  └──────────────────────────┘ │ │
│  │                                │ │
│  │  Volumes:                      │ │
│  │  - logs/  (persistent)         │ │
│  │  - data/  (persistent)         │ │
│  └────────────────────────────────┘ │
└──────────────┬───────────────────────┘
               │
               ▼
      ┌─────────────────┐
      │   OpenAI API    │
      │   (Cloud)       │
      └─────────────────┘
```

## Security Considerations

### API Key Management
- Store in `.env` file (never commit)
- Use environment variables in production
- Rotate keys regularly

### Data Privacy
- Documents processed in-memory
- No persistent storage by default
- Temporary files cleaned up after processing

### Network Security
- CORS protection enabled
- XSRF protection enabled
- Health check endpoints

## Performance Optimization

### Chunking Strategy
- **Chunk Size**: 1000 tokens (configurable)
- **Overlap**: 200 tokens (configurable)
- Balances context preservation and search precision

### Retrieval Optimization
- **Top-k**: 3 documents (default)
- Semantic similarity threshold
- Efficient vector search with Chroma

### Caching Strategy
- Session state for document storage
- In-memory vector store for fast retrieval
- Persistent logs for debugging

## Monitoring and Observability

### Logging Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General operational information
- **WARNING**: Warning messages
- **ERROR**: Error messages

### Metrics to Monitor
- Document processing time
- Query response time
- Token usage
- Error rates
- API call latency

## Scalability Considerations

### Current Limitations
- In-memory vector store (lost on restart)
- Single-instance deployment
- No load balancing

### Future Enhancements
- Persistent vector store (Chroma with persistence)
- Distributed deployment
- Load balancer
- Caching layer (Redis)
- Background job processing

## Best Practices

### Development
1. Use virtual environments
2. Follow PEP 8 style guide
3. Write comprehensive logs
4. Handle errors gracefully
5. Test with various document types

### Deployment
1. Use environment variables for configuration
2. Implement health checks
3. Set up monitoring and alerting
4. Use Docker for consistency
5. Document deployment procedures

### Maintenance
1. Regular dependency updates
2. Monitor API usage and costs
3. Review logs for issues
4. Backup configuration and data
5. Test with production-like data

## Troubleshooting Guide

### Common Issues

#### 1. OpenAI API Errors
- **Cause**: Invalid or missing API key
- **Solution**: Check `.env` file configuration

#### 2. Memory Issues
- **Cause**: Large documents or many chunks
- **Solution**: Adjust chunk size or process fewer documents

#### 3. Slow Queries
- **Cause**: Large vector store or slow embeddings
- **Solution**: Optimize chunk size and top-k parameter

#### 4. Docker Issues
- **Cause**: Port conflicts or missing environment variables
- **Solution**: Check docker-compose.yml and .env file

## Conclusion

This RAG application provides a robust, scalable foundation for building intelligent document query systems. The modular architecture allows for easy customization and extension based on specific requirements.

