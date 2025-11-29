"""Streamlit frontend for RAG Application."""
import os
import tempfile
from typing import List

import streamlit as st

from src.config import Config
from src.logger import Logger
from src.rag_engine import RAGEngine, DOCX_SUPPORT


# Configure page
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = Logger.get_logger("streamlit_app")


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False


def save_uploaded_files(uploaded_files) -> List[str]:
    """
    Save uploaded files to temporary directory.
    
    Args:
        uploaded_files: List of uploaded files from Streamlit
        
    Returns:
        List of file paths
    """
    file_paths = []
    
    for uploaded_file in uploaded_files:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_paths.append(tmp_file.name)
            logger.info(f"Saved uploaded file: {uploaded_file.name}")
    
    return file_paths


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.title("🤖 RAG Application")
    st.markdown("**Retrieval-Augmented Generation powered by LangChain and OpenAI**")
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Document Management")
        
        # File upload
        file_types = ["pdf", "txt"]
        help_text = "Upload PDF or TXT files"
        if DOCX_SUPPORT:
            file_types.append("docx")
            help_text = "Upload PDF, TXT, or DOCX files"
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=file_types,
            accept_multiple_files=True,
            help=help_text
        )
        
        if not DOCX_SUPPORT:
            st.info("ℹ️ DOCX support is currently disabled. Only PDF and TXT files are supported.")
        
        # Text input option
        st.markdown("---")
        st.subheader("Or paste text directly:")
        text_input = st.text_area(
            "Text Input",
            height=200,
            placeholder="Paste your text here..."
        )
        
        # Process button
        if st.button("🚀 Process Documents", type="primary", use_container_width=True):
            if not uploaded_files and not text_input:
                st.error("Please upload files or enter text first!")
            else:
                with st.spinner("Processing documents..."):
                    try:
                        # Initialize RAG engine
                        if st.session_state.rag_engine is None:
                            st.session_state.rag_engine = RAGEngine()
                        
                        documents = []
                        
                        # Process uploaded files
                        if uploaded_files:
                            file_paths = save_uploaded_files(uploaded_files)
                            documents.extend(st.session_state.rag_engine.load_documents(file_paths))
                            
                            # Clean up temp files
                            for file_path in file_paths:
                                os.unlink(file_path)
                        
                        # Process text input
                        if text_input:
                            text_docs = st.session_state.rag_engine.process_text(text_input)
                            documents.extend(text_docs)
                        
                        # Create vector store
                        st.session_state.rag_engine.create_vector_store(documents)
                        st.session_state.documents_loaded = True
                        st.session_state.chat_history = []
                        
                        st.success(f"✅ Processed {len(documents)} document(s) successfully!")
                        logger.info(f"Successfully processed {len(documents)} documents")
                        
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
                        logger.error(f"Error in document processing: {str(e)}")
        
        # Reset button
        if st.button("🔄 Reset", use_container_width=True):
            if st.session_state.rag_engine:
                st.session_state.rag_engine.reset()
            st.session_state.documents_loaded = False
            st.session_state.chat_history = []
            st.success("System reset successfully!")
            logger.info("System reset by user")
        
        # Configuration section
        st.markdown("---")
        st.subheader("⚙️ Configuration")
        st.info(f"**Model:** {Config.MODEL_NAME}")
        st.info(f"**Temperature:** {Config.TEMPERATURE}")
        st.info(f"**Max Tokens:** {Config.MAX_TOKENS}")
        
        # Status
        st.markdown("---")
        st.subheader("📊 Status")
        if st.session_state.documents_loaded:
            st.success("✅ Documents loaded")
        else:
            st.warning("⚠️ No documents loaded")
    
    # Main chat interface
    if st.session_state.documents_loaded:
        st.markdown("### 💬 Ask Questions")
        
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"**Q{i+1}:** {question}")
                st.markdown(f"**A{i+1}:** {answer}")
                st.markdown("---")
        
        # Query input
        with st.form(key="query_form", clear_on_submit=True):
            query = st.text_input(
                "Your Question:",
                placeholder="Enter your question here...",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                submit_button = st.form_submit_button("🔍 Ask", type="primary")
            with col2:
                show_sources = st.checkbox("Show sources", value=False)
        
        if submit_button and query:
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.rag_engine.query(query)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((query, result["answer"]))
                    
                    # Display answer
                    st.markdown("### 📝 Answer:")
                    st.markdown(result["answer"])
                    
                    # Display sources if requested
                    if show_sources and result["source_documents"]:
                        st.markdown("### 📚 Sources:")
                        for idx, doc in enumerate(result["source_documents"], 1):
                            with st.expander(f"Source {idx}"):
                                st.markdown(f"**Content:** {doc['content'][:500]}...")
                                st.markdown(f"**Metadata:** {doc['metadata']}")
                    
                    logger.info(f"Query answered: {query}")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
                    logger.error(f"Error in query processing: {str(e)}")
    
    else:
        st.info("👈 Please upload documents or enter text in the sidebar to get started!")
        
        # Instructions
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Upload Documents**: Use the sidebar to upload PDF, TXT, or DOCX files
        2. **Or Paste Text**: Alternatively, paste text directly in the text area
        3. **Process**: Click the "Process Documents" button
        4. **Ask Questions**: Once processed, ask questions about your documents
        
        ### 💡 Features
        
        - 📄 Support for PDF, TXT, and DOCX files
        - 🔍 Intelligent semantic search using embeddings
        - 💬 Interactive chat interface
        - 📚 Source document references
        - 🎯 Context-aware responses
        
        ### 🔧 Technology Stack
        
        - **LangChain**: RAG framework
        - **OpenAI**: Language model and embeddings
        - **Chroma**: In-memory vector database
        - **Streamlit**: Web interface
        """)


if __name__ == "__main__":
    main()

