# Legal AI Assistant - Railway Ready

A complete legal AI assistant with ChatGPT integration, ready for Railway deployment.

## 🚀 Quick Railway Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Legal AI Assistant"
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway
1. Go to [Railway](https://railway.app)
2. Create new project from GitHub repo
3. Set environment variable: `OPENAI_API_KEY=your_openai_api_key_here`
4. Deploy automatically!

## 📁 Project Structure

```
legal-ai-assistant/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/
│   │   ├── chat.py         # ChatGPT API integration
│   │   ├── files.py        # File upload and processing
│   │   ├── health.py       # Health check endpoints
│   │   └── user.py         # User management
│   ├── models/
│   │   └── user.py         # Database models
│   ├── static/             # Frontend (React app built)
│   │   ├── index.html
│   │   └── assets/
│   └── database/
│       └── app.db          # SQLite database
├── requirements.txt        # Python dependencies
├── Procfile               # Railway start command
├── runtime.txt            # Python version
├── railway.json           # Railway configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## ⚙️ Environment Variables

Set in Railway dashboard:

### Required
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Optional
```
PORT=5000                  # Railway sets this automatically
FLASK_ENV=production
SECRET_KEY=your-secret-key
MAX_FILE_SIZE_MB=16
```

## 🎯 Features

### AI Integration
- Real ChatGPT API integration
- 6 specialized legal analysis types
- Streaming responses
- Context-aware conversations

### File Processing
- PDF document analysis
- Word document processing (.doc/.docx)
- Text file support
- 16MB file size limit

### User Interface
- ChatGPT-style interface
- Mobile-responsive design
- Sidebar with conversation history
- File upload with drag & drop
- Professional help center and pricing

### Legal Analysis Types
1. **Plain English** - Translate complex legal language
2. **Risk Analysis** - Identify potential risks and unfavorable terms
3. **Negotiation** - Suggest fairer terms and strategies
4. **Deal Advisor** - Strategic advice on agreement terms
5. **Dispute Resolution** - Guidance on resolving conflicts
6. **Document Generator** - Create professional legal documents

## 🔧 Local Development

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY="your_openai_api_key_here"

# Run the application
python src/main.py
```

### Access
- Open http://localhost:5000
- The React frontend is served from `/`
- API endpoints are available at `/api/*`

## 🌐 API Endpoints

### Chat & AI
- `POST /api/chat` - Send messages to ChatGPT
- `POST /api/chat/stream` - Streaming responses
- `GET /api/analysis-types` - Available analysis types

### File Processing
- `POST /api/upload` - Upload documents
- `POST /api/analyze-document` - Analyze uploaded files
- `GET /api/supported-formats` - Supported file types

### Health & Monitoring
- `GET /api/health` - Health check for Railway
- `GET /api/status` - Detailed application status

## 🚨 Troubleshooting

### Railway Deployment Issues

**Build Fails:**
- Check that `requirements.txt` is at repository root
- Verify `Procfile` exists with correct start command
- Ensure `OPENAI_API_KEY` is set in Railway environment variables

**App Won't Start:**
- Check Railway deployment logs
- Verify Python version in `runtime.txt`
- Ensure Flask app binds to correct port (`0.0.0.0:$PORT`)

**API Errors:**
- Verify OpenAI API key is valid and has credits
- Check API key format (should start with `sk-`)
- Monitor OpenAI usage limits

### Common Solutions

**Port Issues:**
```python
# In src/main.py, ensure this line exists:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

**CORS Issues:**
```python
# CORS is already configured in src/main.py
from flask_cors import CORS
CORS(app, origins="*")
```

**File Upload Issues:**
- Check file size limits (16MB default)
- Verify supported file types (PDF, DOC, DOCX, TXT)
- Ensure proper error handling

## 📊 Monitoring

### Railway Dashboard
- View deployment logs
- Monitor resource usage
- Check health status
- Manage environment variables

### Application Health
- Health check: `GET /api/health`
- Status endpoint: `GET /api/status`
- Error logging in Railway logs

## 🔒 Security

### Best Practices
- API keys stored as environment variables
- File upload validation and size limits
- Input sanitization for all user inputs
- CORS properly configured
- Error messages don't expose sensitive information

### File Security
- Uploaded files are processed and not permanently stored
- File type validation prevents malicious uploads
- Size limits prevent resource exhaustion

## 📈 Scaling

### Railway Auto-scaling
- Railway automatically scales based on traffic
- Configure scaling limits in Railway dashboard
- Monitor resource usage and costs

### Performance Optimization
- Static files served efficiently
- Database queries optimized
- Response caching ready for implementation
- CDN integration possible

## 🛠️ Customization

### Adding New Analysis Types
Edit `src/routes/chat.py` to add new analysis prompts:

```python
ANALYSIS_PROMPTS = {
    "new_type": {
        "name": "New Analysis Type",
        "prompt": "Your custom prompt here..."
    }
}
```

### Extending File Support
Modify `src/routes/files.py` to support additional file formats.

### UI Customization
The React frontend is pre-built in `src/static/`. To modify:
1. Get the original React source code
2. Make your changes
3. Build with `npm run build`
4. Copy build files to `src/static/`

### Database Upgrade
Replace SQLite with PostgreSQL:
1. Add PostgreSQL dependency to `requirements.txt`
2. Set `DATABASE_URL` environment variable in Railway
3. Update database configuration in `src/main.py`

## 📞 Support

### Resources
- [Railway Documentation](https://docs.railway.app/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Common Issues
- Check Railway deployment logs for specific errors
- Verify environment variables are set correctly
- Ensure OpenAI API key has sufficient credits
- Monitor file upload sizes and formats

---

## 🎯 Ready to Deploy!

This application is production-ready with:
- ✅ Real ChatGPT integration
- ✅ Professional UI/UX
- ✅ File processing capabilities
- ✅ Railway deployment configuration
- ✅ Health monitoring
- ✅ Error handling
- ✅ Security best practices

**Deploy to Railway in under 5 minutes!** 🚀

