# Legal AI Assistant - Full Stack Application

A complete full-stack legal AI assistant application with ChatGPT API integration, ready for Railway deployment.

## 🎯 Features

### Frontend (React + Vite)
- **ChatGPT-Style Interface**: Modern chat interface with sidebar and conversation history
- **6 AI Analysis Types**: Plain English, Risk Analysis, Negotiation, Deal Advisor, Dispute Resolution, Document Generator
- **File Upload Support**: PDF, Word documents, and text files with real-time processing
- **Mobile Responsive**: Perfect mobile experience with collapsible sidebar
- **Professional UI**: Clean, modern design with help center, pricing, and settings

### Backend (Flask + OpenAI)
- **ChatGPT API Integration**: Real AI responses using OpenAI's GPT-4 model
- **Document Processing**: Extract text from PDF, DOC, DOCX, and TXT files
- **Analysis Endpoints**: Specialized prompts for different legal analysis types
- **File Upload API**: Secure file handling with size limits and format validation
- **Health Monitoring**: Health check endpoints for deployment monitoring

### Deployment Ready
- **Railway Optimized**: Complete Railway deployment configuration
- **Environment Variables**: Secure API key management
- **CORS Enabled**: Frontend-backend communication configured
- **Production Build**: Optimized for production deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API Key
- Railway account (for deployment)

### Local Development

```bash
# Clone or extract the project
cd legal-ai-assistant-fullstack

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key_here"

# Run the application
python src/main.py
```

The application will be available at `http://localhost:5000`

### Railway Deployment

1. **Connect Repository**
   - Push code to GitHub repository
   - Connect repository to Railway

2. **Set Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PORT=5000
   FLASK_ENV=production
   ```

3. **Deploy**
   - Railway will automatically detect the Flask application
   - Build and deployment will happen automatically
   - Access your app at the provided Railway URL

## 📁 Project Structure

```
legal-ai-assistant-fullstack/
├── src/
│   ├── routes/
│   │   ├── chat.py          # ChatGPT API integration
│   │   ├── files.py         # File upload and processing
│   │   ├── health.py        # Health check endpoints
│   │   └── user.py          # User management (template)
│   ├── models/
│   │   └── user.py          # Database models
│   ├── static/              # Frontend build files
│   │   ├── index.html
│   │   └── assets/
│   ├── database/
│   │   └── app.db          # SQLite database
│   └── main.py             # Flask application entry point
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
├── railway.json           # Railway deployment config
├── Procfile              # Process configuration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message to AI assistant
- `POST /api/chat/stream` - Streaming chat responses
- `GET /api/analysis-types` - Get available analysis types

### File Endpoints
- `POST /api/upload` - Upload and process documents
- `POST /api/analyze-document` - Analyze uploaded documents
- `GET /api/supported-formats` - Get supported file formats

### Health Endpoints
- `GET /api/health` - Health check for Railway
- `GET /api/status` - Detailed application status

## 🎨 Analysis Types

1. **Plain English** (`plain_english`)
   - Translates complex legal language into clear terms
   - Explains legal concepts in simple language

2. **Risk Analysis** (`risk_analysis`)
   - Identifies potential risks and unfavorable terms
   - Provides risk assessment and mitigation strategies

3. **Negotiation** (`negotiation`)
   - Suggests fairer terms and negotiation strategies
   - Recommends alternative language for clauses

4. **Deal Advisor** (`deal_advisor`)
   - Strategic advice on agreement terms
   - Guidance on industry-standard practices

5. **Dispute Resolution** (`dispute_resolution`)
   - Guidance on resolving conflicts and disputes
   - Mediation and resolution strategies

6. **Document Generator** (`document_generator`)
   - Creates professional legal documents
   - Generates contract templates

## 🔒 Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key for ChatGPT integration

### Optional
- `PORT` - Port number (default: 5000)
- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Flask secret key for sessions
- `MAX_FILE_SIZE_MB` - Maximum file upload size (default: 16MB)

## 📱 File Upload Support

### Supported Formats
- **PDF** - Portable Document Format
- **DOC** - Microsoft Word Document (legacy)
- **DOCX** - Microsoft Word Document
- **TXT** - Plain Text File

### File Processing
- Automatic text extraction from uploaded documents
- Size limit: 16MB per file
- Secure file handling with cleanup after processing
- Error handling for unsupported formats

## 🌐 Deployment Options

### Railway (Recommended)
- Automatic builds and deployments
- Environment variable management
- Custom domain support
- Built-in monitoring and logs

### Manual Deployment
```bash
# Build for production
export FLASK_ENV=production
export OPENAI_API_KEY="your_key_here"

# Run application
python src/main.py
```

## 🔍 Monitoring

### Health Checks
- `/api/health` - Basic health status
- `/api/status` - Detailed application information
- Automatic Railway health monitoring

### Logging
- Request/response logging
- Error tracking and reporting
- OpenAI API usage monitoring

## 🚨 Troubleshooting

### Common Issues

**OpenAI API Errors:**
- Verify API key is set correctly
- Check API quota and billing
- Ensure network connectivity

**File Upload Issues:**
- Check file size (max 16MB)
- Verify supported file format
- Ensure proper file permissions

**Deployment Issues:**
- Verify all environment variables are set
- Check Railway logs for errors
- Ensure requirements.txt is up to date

### Support
- Check Railway deployment logs
- Verify environment variables
- Test API endpoints individually
- Monitor health check status

## 📄 License

This project is provided for educational and development purposes.

## 🤝 Contributing

The application is designed to be modular and extensible:
- Add new analysis types in `src/routes/chat.py`
- Extend file processing in `src/routes/files.py`
- Customize frontend in the static files
- Add new API endpoints as needed

---

**Built with Flask, React, OpenAI GPT-4, and Railway deployment ready! 🚀**

