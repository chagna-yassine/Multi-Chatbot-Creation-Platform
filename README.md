# Multi-Chatbot Creation Platform

This project is a **multi-chatbot creation platform** that allows users to:
- Register and log in.
- Create chatbots with configurable personalities.
- Upload knowledge bases for chatbots (PDF/TXT documents).
- Perform semantic searches and AI-powered responses using a vectorized knowledge base.

## Features
1. **User Management**: Registration, login, and JWT-based authentication.
2. **Chatbot Management**: Create, update, delete, and list chatbots.
3. **Knowledge Base Integration**: Upload documents and generate embeddings for contextual search.
4. **AI-Powered Responses**: Query chatbot knowledge base and receive intelligent responses.

---

## Prerequisites
Ensure the following are installed on your machine:
- Python 3.11 or higher
- pip (Python package manager)
- Redis (required for rate limiting)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Multi-Chatbot-Creation-Platform
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**:
   Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Set Up Redis**:
   Ensure Redis is running for rate-limiting functionality:
   ```bash
   redis-server
   ```

---

## File Structure

```
Multi-Chatbot-Creation-Platform/
├── app/
│   ├── main.py                # Main entry point for the application
│   ├── routes/                # API route files
│   │   ├── auth.py            # Authentication routes
│   │   ├── chatbot.py         # Chatbot-related routes
│   ├── schemas/               # Pydantic schemas for request/response validation
│   ├── models/                # SQLAlchemy models for database tables
│   ├── utils/                 # Utility functions (AI response, file handling, etc.)
│   │   ├── ai_response.py     # AI-powered response generation
│   │   ├── file_handler.py    # File processing utilities
│   │   ├── vector_db.py       # Vector database utilities for knowledge base
│   ├── database.py            # Database configuration
│   └── config.py              # Application configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration for deployment
├── README.md                  # Documentation
└── .gitignore                 # Ignored files for Git
```

---

## API Endpoints and Testing

### **1. User Management**

#### **Register a New User**
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword"
}'
```

#### **Login User**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "testuser@example.com",
    "password": "securepassword"
}'
```

---

### **2. Chatbot Management**

#### **Create a Chatbot**
```bash
curl -X POST "http://127.0.0.1:8000/chatbot/" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
    "name": "Support Bot",
    "description": "Helps with customer support",
    "tone": "Professional and empathetic",
    "behavior": "Responds with concise and accurate information"
}'
```

#### **List All Chatbots**
```bash
curl -X GET "http://127.0.0.1:8000/chatbot/" \
-H "Authorization: Bearer <your-token>"
```

#### **Get a Chatbot**
```bash
curl -X GET "http://127.0.0.1:8000/chatbot/<chatbot_id>" \
-H "Authorization: Bearer <your-token>"
```

#### **Update a Chatbot**
```bash
curl -X PATCH "http://127.0.0.1:8000/chatbot/<chatbot_id>" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
    "tone": "Friendly and casual",
    "behavior": "Provides detailed explanations"
}'
```

#### **Delete a Chatbot**
```bash
curl -X DELETE "http://127.0.0.1:8000/chatbot/<chatbot_id>" \
-H "Authorization: Bearer <your-token>"
```

---

### **3. Knowledge Base Management**

#### **Upload a Document**
```bash
curl -X POST "http://127.0.0.1:8000/chatbot/<chatbot_id>/upload" \
-H "Authorization: Bearer <your-token>" \
-F "file=@path/to/your/file.txt"
```

#### **Query Knowledge Base**
```bash
curl -X POST "http://127.0.0.1:8000/chatbot/<chatbot_id>/query" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
    "query": "What are the credentials required to set up this system?"
}'
```

#### **Get Knowledge Base Collection**
```bash
curl -X GET "http://127.0.0.1:8000/chatbot/<chatbot_id>/collection" \
-H "Authorization: Bearer <your-token>"
```

---

### **4. Health Check**
```bash
curl -X GET "http://127.0.0.1:8000/chatbot/health"
```

---

## Notes
- Replace `<your-token>` with the JWT token obtained from the **Login** endpoint.
- Replace `<chatbot_id>` with the actual chatbot ID created during the **Create a Chatbot** step.
