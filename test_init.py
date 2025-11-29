"""Test OpenAI initialization."""
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing OpenAI initialization...")
print(f"API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"API Key prefix: {os.getenv('OPENAI_API_KEY', '')[:10]}...")

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

try:
    print("\nTesting ChatOpenAI...")
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    print("✅ ChatOpenAI initialized successfully!")
    print(f"   Model: {llm.model_name}")
    
    print("\nTesting OpenAIEmbeddings...")
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    print("✅ OpenAIEmbeddings initialized successfully!")
    
    print("\n🎉 All initializations successful!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

