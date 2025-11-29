"""RAG Engine implementation using LangChain and Chroma."""
from typing import List, Optional

from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

# Try to import UnstructuredWordDocumentLoader, but make it optional
try:
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document

from src.config import Config
from src.logger import Logger


logger = Logger.get_logger("rag_engine")

# Log DOCX support status
if not DOCX_SUPPORT:
    logger.warning("UnstructuredWordDocumentLoader not available. DOCX support disabled.")


class RAGEngine:
    """RAG Engine for document processing and question answering."""
    
    def __init__(self):
        """Initialize RAG Engine."""
        logger.info("Initializing RAG Engine")
        
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            api_key=Config.OPENAI_API_KEY,
        )
        
        self.embeddings = OpenAIEmbeddings(
            api_key=Config.OPENAI_API_KEY
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        self.vector_store: Optional[Chroma] = None
        self.qa_chain: Optional[RetrievalQA] = None
        
        logger.info("RAG Engine initialized successfully")
    
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Load documents from file paths.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            List of loaded documents
        """
        logger.info(f"Loading {len(file_paths)} documents")
        documents = []
        
        for file_path in file_paths:
            try:
                if file_path.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                elif file_path.endswith('.txt'):
                    loader = TextLoader(file_path)
                elif file_path.endswith('.docx'):
                    if DOCX_SUPPORT:
                        loader = UnstructuredWordDocumentLoader(file_path)
                    else:
                        logger.warning(f"DOCX support not available. Skipping: {file_path}")
                        continue
                else:
                    logger.warning(f"Unsupported file type: {file_path}")
                    continue
                
                docs = loader.load()
                documents.extend(docs)
                logger.info(f"Loaded {len(docs)} pages from {file_path}")
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
        
        return documents
    
    def process_text(self, text: str) -> List[Document]:
        """
        Process raw text into documents.
        
        Args:
            text: Raw text to process
            
        Returns:
            List of document chunks
        """
        logger.info("Processing raw text input")
        document = Document(page_content=text, metadata={"source": "text_input"})
        chunks = self.text_splitter.split_documents([document])
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Create vector store from documents.
        
        Args:
            documents: List of documents to index
        """
        logger.info(f"Creating vector store with {len(documents)} documents")
        
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split documents into {len(chunks)} chunks")
            
            # Create in-memory Chroma vector store
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                collection_name="rag_collection",
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True,
            )
            
            logger.info("Vector store and QA chain created successfully")
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def query(self, question: str) -> dict:
        """
        Query the RAG system.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            logger.error("QA chain not initialized. Please load documents first.")
            raise ValueError("No documents loaded. Please upload documents before querying.")
        
        logger.info(f"Processing query: {question}")
        
        try:
            result = self.qa_chain.invoke({"query": question})
            
            response = {
                "answer": result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in result.get("source_documents", [])
                ]
            }
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def reset(self) -> None:
        """Reset the RAG engine."""
        logger.info("Resetting RAG Engine")
        self.vector_store = None
        self.qa_chain = None
        logger.info("RAG Engine reset successfully")

