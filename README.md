# RAG System with Authentication

A FastAPI-based RAG (Retrieval-Augmented Generation) system with JWT authentication, built around your existing RAG implementation.

## Features

- **JWT Authentication**: Secure token-based authentication
- **User Management**: Signup, signin/login endpoints
- **Protected RAG Queries**: Authenticated access to the RAG system
- **Session Management**: User-specific chat sessions
- **SQLite Database**: User data storage
- **CORS Support**: Cross-origin resource sharing enabled

## Project Structure

```
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── test_api.py           # API testing script
├── run_system.py         # Startup script for both backend and frontend
├── .env                  # Environment variables
├── auth/                 # Authentication module
│   ├── __init__.py
│   ├── models.py         # Database and Pydantic models
│   ├── database.py       # Database configuration
│   └── auth_handler.py   # JWT and password handling
├── frontend/             # Streamlit frontend
│   ├── app.py           # Main Streamlit application
│   ├── requirements.txt # Frontend dependencies
│   └── README.md        # Frontend documentation
└── RAG/                  # Existing RAG system
    ├── chains.py
    ├── helpers.py
    ├── main.py
    └── ...
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Make sure your `.env` file contains:
```
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=your_model

# JWT Secret Key
JWT_SECRET_KEY=your-super-secret-jwt-key

```

### 3. Run the Application

#### Option 1: Run Backend Only
```bash
python app.py
```

The API will be available at `http://localhost:8000`

#### Option 2: Run Both Backend and Frontend
```bash
python run_system.py
```

This will start:
- FastAPI backend at `http://localhost:8000`
- Streamlit frontend at `http://localhost:8501`

#### Option 3: Run Frontend Separately
```bash
# Install frontend dependencies
cd frontend
pip install -r requirements.txt

# Start the frontend (make sure backend is running first)
streamlit run app.py
```

## Streamlit Frontend

The project includes a simple Streamlit web interface that provides:

- **User Authentication**: Login and signup forms
- **RAG Query Interface**: Text area for asking questions
- **Chat History**: View previous questions and answers
- **User Profile**: Display user information
- **Session Management**: Persistent login during browser session

### Frontend Features

- Clean, simple interface without icons or emojis
- Real-time API connectivity checking
- Error handling with clear user messages
- Responsive design with proper form validation
- Automatic token management and session handling

### Using the Frontend

1. Start both backend and frontend using `python run_system.py`
2. Open `http://localhost:8501` in your browser
3. Sign up for a new account or login with existing credentials
4. Ask questions about company policies in the query interface
5. View your chat history and user profile information

## API Endpoints

### Authentication Endpoints

#### POST /signup
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

#### POST /signin or POST /login
Sign in with existing credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

### Protected Endpoints

#### GET /profile
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "created_at": "2023-01-01T00:00:00"
}
```

#### POST /query
Query the RAG system (requires authentication).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "question": "What is the company policy on remote work?",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "answer": "Based on the company policy documents...",
  "session_id": "user_id_session_id"
}
```

### Public Endpoints

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

This will test:
- Health endpoint
- User signup
- User signin
- Profile retrieval
- RAG queries (authenticated and unauthorized)

## Usage Examples

### Using curl

1. **Sign up:**
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "password123"}'
```

2. **Query RAG system:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"question": "What is the company policy?", "session_id": "my_session"}'
```

### Using Python requests

```python
import requests

# Sign up
response = requests.post("http://localhost:8000/signup", json={
    "email": "test@example.com",
    "username": "testuser", 
    "password": "password123"
})
token = response.json()["access_token"]

# Query RAG
headers = {"Authorization": f"Bearer {token}"}
response = requests.post("http://localhost:8000/query", 
    json={"question": "What is the company policy?"}, 
    headers=headers)
print(response.json())
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Protected Routes**: RAG queries require valid authentication
- **User Isolation**: Each user has separate chat sessions
- **CORS Protection**: Configurable cross-origin access

## Development

### Adding New Endpoints

1. Add new routes to `app.py`
2. Use `Depends(get_current_user)` for protected routes
3. Follow the existing pattern for error handling

### Database Changes

1. Modify models in `auth/models.py`
2. The database will auto-create tables on startup

### Environment Variables

Add new environment variables to `.env` and load them in the respective modules.

## Production Deployment

1. **Change JWT Secret**: Use a strong, random secret key
2. **Database**: Consider PostgreSQL for production
3. **HTTPS**: Enable SSL/TLS encryption
4. **Environment**: Set proper environment variables
5. **Logging**: Add comprehensive logging
6. **Rate Limiting**: Implement API rate limiting

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Errors**: Check if SQLite file permissions are correct
3. **RAG Errors**: Verify AWS credentials and Bedrock access
4. **Token Errors**: Check JWT secret key configuration

### Logs

The application logs errors to the console. Check for:
- Database connection issues
- Authentication failures
- RAG system errors
- Missing environment variables
