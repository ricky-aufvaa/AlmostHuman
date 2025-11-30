from langchain_community.vectorstores import FAISS
from langchain_aws import ChatBedrock
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def vectorstore(embedding_function):
    """Load FAISS vector store and return a retriever"""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    faiss_path = os.path.join(current_dir, "faiss_embed")
    
    vectorstore = FAISS.load_local(faiss_path, embeddings=embedding_function, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    return retriever

def get_chat_model():
    """Initialize and return ChatOllama LLM (llama3.1:8b)"""
    # llm = ChatOllama(model="llama3.1:8b")
    llm = ChatBedrock(
        model=os.getenv("BEDROCK_MODEL_ID"),
        region_name=os.getenv("AWS_REGION")
    )
    return llm

def format_docs(docs):
    """Format documents into a single string"""
    return "\n\n".join(doc.page_content for doc in docs)
