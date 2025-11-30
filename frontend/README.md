# Streamlit Frontend for RAG System

A simple Streamlit frontend for the RAG System with Authentication API.

## Features

- User authentication (login/signup)
- RAG query interface
- Chat history management
- User profile display
- Session state management
- Error handling and API connectivity checks

## Setup Instructions

### 1. Install Dependencies

Navigate to the frontend directory and install requirements:

```bash
cd frontend
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend

Make sure the FastAPI server is running first:

```bash
# From the root directory
python app.py
```

The API should be running on `http://localhost:8000`

### 3. Run the Streamlit Frontend

```bash
# From the frontend directory
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`

## Usage

### Authentication

1. **Sign Up**: Create a new account with email, username, and password
2. **Login**: Sign in with existing credentials

### RAG Queries

Once authenticated, you can:

1. Ask questions about company policies in the text area
2. View chat history of previous questions and answers
3. Clear chat history when needed
4. View your user profile information

### Features

- **Session Management**: Your login session persists during the browser session
- **Chat History**: Last 10 conversations are stored and displayed
- **Error Handling**: Clear error messages for API connectivity and authentication issues
- **Responsive Design**: Clean, simple interface without icons or emojis

## API Integration

The frontend communicates with the FastAPI backend through these endpoints:

- `GET /health` - Check API server status
- `POST /signup` - User registration
- `POST /signin` - User authentication
- `GET /profile` - Get user profile information
- `POST /query` - Submit RAG queries

## Configuration

The API base URL is configured in the frontend app:

```python
API_BASE_URL = "http://localhost:8000"
```

Change this if your FastAPI server runs on a different host/port.

## File Structure

```
frontend/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **"Cannot connect to API"**: Make sure the FastAPI server is running on port 8000
2. **Authentication errors**: Check that the API server is properly configured with JWT settings
3. **RAG query failures**: Verify that the RAG system is properly initialized with embeddings and documents

### Dependencies

- `streamlit==1.28.1` - Web framework for the frontend
- `requests==2.31.0` - HTTP client for API communication

## Development

### Adding New Features

1. Add new functions for API communication following the `make_request` pattern
2. Add new UI components using Streamlit widgets
3. Update session state management as needed

### Customization

- Modify the UI layout by changing Streamlit components
- Add new form fields or validation rules
- Customize error messages and success notifications
- Add new pages using Streamlit's multipage functionality

## Security Notes

- JWT tokens are stored in Streamlit session state (browser memory)
- Tokens expire after 30 minutes (configurable in the API)
- No sensitive data is stored persistently in the frontend
- All API communication uses proper authentication headers
