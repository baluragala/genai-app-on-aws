"""Test script for RAG Engine."""
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.logger import Logger
from src.rag_engine import RAGEngine

logger = Logger.get_logger("test_rag")


def test_rag_engine():
    """Test the RAG engine with sample data."""
    logger.info("Starting RAG Engine test")
    
    try:
        # Initialize RAG engine
        logger.info("Initializing RAG Engine...")
        rag_engine = RAGEngine()
        
        # Test with sample text
        sample_text = """
        Artificial Intelligence (AI) is transforming the world of technology. 
        Machine learning, a subset of AI, enables computers to learn from data 
        without being explicitly programmed. Deep learning, which uses neural 
        networks with multiple layers, has achieved remarkable success in areas 
        like image recognition, natural language processing, and game playing.
        
        Large Language Models (LLMs) like GPT-3 and GPT-4 have revolutionized 
        natural language understanding and generation. These models are trained 
        on vast amounts of text data and can perform a wide variety of language 
        tasks with minimal fine-tuning.
        """
        
        logger.info("Processing sample text...")
        documents = rag_engine.process_text(sample_text)
        logger.info(f"Created {len(documents)} document chunks")
        
        # Create vector store
        logger.info("Creating vector store...")
        rag_engine.create_vector_store(documents)
        logger.info("Vector store created successfully")
        
        # Test queries
        test_queries = [
            "What is artificial intelligence?",
            "What are Large Language Models?",
            "How does machine learning work?",
        ]
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\nTest Query {i}: {query}")
            result = rag_engine.query(query)
            
            print(f"\n{'='*60}")
            print(f"Question: {query}")
            print(f"{'='*60}")
            print(f"Answer: {result['answer']}")
            print(f"\nNumber of source documents: {len(result['source_documents'])}")
            print(f"{'='*60}\n")
        
        logger.info("All tests passed successfully! ✅")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("RAG Engine Test")
    print("="*60 + "\n")
    
    success = test_rag_engine()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

