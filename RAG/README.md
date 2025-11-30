# RAG (Retrieval-Augmented Generation) System

## Overview
This is a complete open-source RAG system that processes PDF documents, creates embeddings, and provides an intelligent chatbot interface with conversation history. All models run locally using Ollama.

## Project Structure

```
RAG/
├── constants.py      # Configuration constants (paths, database)
├── preprocess.py     # PDF loading and preprocessing pipeline
├── helpers.py        # Utility functions (vectorstore, LLM, formatting)
├── db.py            # Database models and chat history management
├── prompts.py       # LangChain prompt templates
├── chains.py        # RAG chain configuration
├── main.py          # Main chatbot application
├── data/            # PDF documents folder
└── faiss_embed/     # Vector store embeddings
```

## Open-Source Stack

### Models Used (All via Ollama)
- **LLM**: llama3.1:8b - For generating responses
- **Embeddings**: llama3.1:8b - For document embeddings
- **Vector Store**: FAISS - For similarity search
- **Database**: SQLite - For chat history

### Why Open Source?
✅ **Privacy**: All data stays on your machine
✅ **Cost**: No API fees or usage limits
✅ **Control**: Full control over models and data
✅ **Offline**: Works without internet connection
✅ **Customizable**: Easy to swap models or fine-tune

## Files Description

### 1. constants.py
Defines configuration constants:
- `PDF_PATH`: Location of PDF documents ("data")
- `MD_PATH`: Location for markdown files ("data/markdown")
- `VDB_PATH`: Vector database path ("faiss_embed")
- `DB_PATH`: SQLite database path ("chat.db")

### 2. preprocess.py
Handles document preprocessing:
- **Functions:**
  - `find_all_pdfs()`: Recursively finds all PDF files in a folder
  - `load_pdf()`: Loads all PDFs and returns documents
  - `splitting()`: Splits documents into chunks (1000 chars, 200 overlap)
  - `initialise_embed()`: Initializes Ollama embeddings (llama3.1:8b)
  - `initialise_vectorstore()`: Creates and saves FAISS vector store
- **Main execution**: Runs complete preprocessing pipeline
- **Models**: Uses OllamaEmbeddings for creating document embeddings

### 3. helpers.py
Utility functions:
- **Functions:**
  - `vectorstore()`: Loads FAISS vector store and returns retriever
  - `get_chat_model()`: Initializes ChatOllama LLM (llama3.1:8b)
  - `format_docs()`: Formats retrieved documents into string
- **Models**: Uses ChatOllama for response generation

### 4. db.py
Database management:
- **Models:**
  - `Session`: Stores chat sessions
  - `Message`: Stores individual messages
- **Functions:**
  - `get_db()`: Database session generator
  - `save_message()`: Saves a message to database
  - `load_session_history()`: Loads chat history from database
  - `get_session_history()`: Gets or creates session history
  - `save_all_sessions()`: Saves all sessions to database

### 5. prompts.py
LangChain prompt templates:
- System prompt with context injection
- Chat history placeholder
- User question input

### 6. chains.py
RAG chain configuration:
- Initializes all components (embeddings, retriever, LLM)
- Creates RAG chain with context retrieval
- Wraps chain with message history

### 7. main.py
Main chatbot application:
- Interactive command-line interface
- Session management
- Error handling
- Exit commands: 'exit', 'quit', 'q'

## Setup Instructions

### 1. Install Ollama
```bash
# Download and install from https://ollama.ai
# Or use package manager:
curl https://ollama.ai/install.sh | sh
```

### 2. Pull Required Models
```bash
# Pull the LLM model
ollama pull llama3.1:8b

# Verify models are available
ollama list
```

### 3. Install Python Dependencies
```bash
pip install langchain langchain-community langchain-ollama
pip install faiss-cpu sqlalchemy python-dotenv pypdf
```

### 4. Add PDF Documents
Place your PDF files in the `RAG/data/` folder.

### 5. Run Preprocessing
```bash
cd RAG
python preprocess.py
```

This will:
- Load all PDFs from the data folder
- Split documents into chunks
- Create embeddings using Ollama (llama3.1:8b)
- Save vector store to `faiss_embed/`

### 6. Run the Chatbot
```bash
python main.py
```

## Key Improvements Made

### Open-Source Architecture
✅ All models run locally via Ollama
✅ No cloud dependencies or API keys needed
✅ Complete privacy - data never leaves your machine
✅ No usage costs or rate limits

### Code Quality
✅ Added proper imports to all files
✅ Added docstrings to all functions
✅ Removed duplicate code
✅ Fixed document loading and return values
✅ Improved splitting function to work with document lists

### Functionality
✅ Completed preprocess.py main block with full pipeline
✅ Created proper main.py with interactive chatbot
✅ Fixed chains.py with all required imports and initialization
✅ Maintained chat history with SQLite database

### Project Organization
✅ Organized all code in RAG folder
✅ Proper separation of concerns across modules
✅ Clear file structure and dependencies

## Usage Example

```python
# After running preprocess.py, start the chatbot:
python main.py

# Example conversation:
You: What information is in the documents?
Assistant: [Response based on PDF content]

You: Tell me more about [specific topic]
Assistant: [Contextual response with chat history]

You: exit
Goodbye!
```

## Technical Details

### LLM Model
- **Model**: llama3.1:8b
- **Provider**: Ollama (local)
- **Purpose**: Response generation

### Embedding Model
- **Model**: llama3.1:8b
- **Provider**: Ollama (local)
- **Purpose**: Document and query embeddings

### Vector Store
- **Type**: FAISS
- **Retrieval**: Similarity search
- **Top K**: 6 documents

### Text Splitting
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Method**: RecursiveCharacterTextSplitter

## Performance Considerations

### System Requirements
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB for models + space for embeddings
- **CPU**: Modern multi-core processor
- **GPU**: Optional but recommended for faster inference

### Response Times
- **First query**: 5-10 seconds (model loading)
- **Subsequent queries**: 2-5 seconds
- **Preprocessing**: Depends on document count

### Optimization Tips
1. Keep Ollama running in background
2. Use GPU if available
3. Adjust chunk size based on document type
4. Limit number of retrieved documents (k parameter)

## Customization

### Change LLM Model
Edit `helpers.py`:
```python
def get_chat_model():
    llm = ChatOllama(model="llama3.1:70b")  # Use larger model
    return llm
```

### Change Embedding Model
Edit `preprocess.py`:
```python
def initialise_embed():
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    return embedding_function
```

### Adjust Retrieval Parameters
Edit `helpers.py`:
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}  # Retrieve more documents
)
```

### Modify Prompts
Edit `prompts.py` to customize system prompts and behavior.

## Troubleshooting

### Ollama Not Running
```bash
# Start Ollama service
ollama serve
```

### Model Not Found
```bash
# Pull the model
ollama pull llama3.1:8b
```

### Out of Memory
- Use smaller model (e.g., llama3.1:7b)
- Reduce chunk size in preprocessing
- Decrease number of retrieved documents

### Slow Performance
- Enable GPU acceleration
- Use quantized models
- Reduce context window size

## Available Ollama Models

### LLM Options
- `llama3.1:8b` - Balanced performance (default)
- `llama3.1:70b` - Higher quality, slower
- `mistral:7b` - Fast and efficient
- `phi3:mini` - Lightweight option

### Embedding Options
- `llama3.1:8b` - General purpose (default)
- `nomic-embed-text` - Optimized for embeddings
- `mxbai-embed-large` - High quality embeddings

## Notes

- The system maintains conversation history in SQLite database
- Each session is identified by a session_id
- Vector embeddings are stored locally in `faiss_embed/`
- All processing happens locally - no data sent to external services
- The system supports multiple PDF documents simultaneously
- Models are cached by Ollama for faster subsequent loads

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Llama 3.1 Model Info](https://ollama.ai/library/llama3.1)
- [FAISS Documentation](https://faiss.ai/)
