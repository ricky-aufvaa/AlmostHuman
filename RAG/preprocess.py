from constants import PDF_PATH, MD_PATH
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def find_all_pdfs(folder_path: str):
    pdf_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                pdf_files.append(full_path)

    return pdf_files


def load_pdf(folder_path=PDF_PATH):
    """Load all PDF files from the specified folder and return documents"""
    pdf_files = find_all_pdfs(folder_path)
    all_documents = []
    
    for file in pdf_files:
        loader = PyPDFLoader(file)
        documents = loader.load()
        all_documents.extend(documents)
    
    return all_documents
    

def splitting(documents):
    """Split documents into chunks using RecursiveCharacterTextSplitter"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    return splits

def initialise_embed():
    """Initialize embedding function using AWS Bedrock with credentials from environment"""
    embedding_function = OllamaEmbeddings(model="llama3.1:8b")
    return embedding_function

def initialise_vectorstore(md_header_splits,embedding_function):
    """Create and save FAISS vector store"""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    faiss_path = os.path.join(current_dir, "faiss_embed")
    
    vectorstore = FAISS.from_documents(documents=md_header_splits,embedding=embedding_function)
    vectorstore.save_local(faiss_path)


if __name__=="__main__":
    """Main preprocessing pipeline to load PDFs, split them, and create vector store"""
    print("Starting preprocessing pipeline...")
    
    # Step 1: Load all PDF documents
    print(f"Loading PDFs from {PDF_PATH}...")
    documents = load_pdf()
    print(f"Loaded {len(documents)} document pages")
    
    # Step 2: Split documents into chunks
    print("Splitting documents into chunks...")
    splits = splitting(documents)
    print(f"Created {len(splits)} document chunks")
    
    # Step 3: Initialize embedding function
    print("Initializing embedding function...")
    embedding_function = initialise_embed()
    
    # Step 4: Create and save vector store
    print("Creating vector store and saving embeddings...")
    initialise_vectorstore(splits, embedding_function)
    print(f"Vector store saved successfully to ./faiss_embed")
