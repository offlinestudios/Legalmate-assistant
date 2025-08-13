# Legal AI Assistant - Deployment Guide

Complete guide for deploying the Legal AI Assistant to Railway and other platforms.

## 🚀 Railway Deployment (Recommended)

Railway provides the easiest deployment experience with automatic builds, environment management, and monitoring.

### Step 1: Prepare Your Repository

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Legal AI Assistant"
   git branch -M main
   git remote add origin https://github.com/yourusername/legal-ai-assistant.git
   git push -u origin main
   ```

2. **Verify Project Structure**
   ```
   legal-ai-assistant-fullstack/
   ├── src/main.py              # Entry point
   ├── requirements.txt         # Dependencies
   ├── railway.json            # Railway config
   ├── Procfile               # Process config
   └── .env.example           # Environment template
   ```

### Step 2: Railway Setup

1. **Create Railway Account**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   PORT=5000
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

### Step 3: Deploy

1. **Automatic Deployment**
   - Railway automatically detects Flask application
   - Builds using requirements.txt
   - Starts with `python src/main.py`

2. **Monitor Deployment**
   - Check deployment logs in Railway dashboard
   - Verify health check at `/api/health`
   - Test application functionality

### Step 4: Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to Settings > Domains
   - Add your custom domain
   - Configure DNS records as shown

## 🔧 Environment Variables Setup

### Required Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Flask Configuration
PORT=5000
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
```

### Optional Variables

```bash
# File Upload Configuration
MAX_FILE_SIZE_MB=16
UPLOAD_FOLDER=uploads

# Database Configuration (if using external DB)
DATABASE_URL=postgresql://user:password@host:port/database

# CORS Configuration
ALLOWED_ORIGINS=https://your-domain.com
```

### Getting OpenAI API Key

1. **Create OpenAI Account**
   - Visit [platform.openai.com](https://platform.openai.com)
   - Sign up or log in

2. **Generate API Key**
   - Go to API Keys section
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

3. **Set Usage Limits**
   - Configure usage limits in OpenAI dashboard
   - Monitor usage and billing

## 🌐 Alternative Deployment Options

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your-key-here
   heroku config:set FLASK_ENV=production
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Configure vercel.json**
   ```json
   {
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

### DigitalOcean App Platform

1. **Create App**
   - Connect GitHub repository
   - Select Python runtime

2. **Configure Build**
   ```yaml
   name: legal-ai-assistant
   services:
   - name: web
     source_dir: /
     github:
       repo: yourusername/legal-ai-assistant
       branch: main
     run_command: python src/main.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: OPENAI_API_KEY
       value: your-key-here
     - key: FLASK_ENV
       value: production
   ```

## 🔍 Testing Deployment

### Health Check Endpoints

```bash
# Basic health check
curl https://your-app.railway.app/api/health

# Detailed status
curl https://your-app.railway.app/api/status

# Test chat endpoint
curl -X POST https://your-app.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "analysis_type": "general"}'
```

### Frontend Testing

1. **Access Application**
   - Visit your Railway URL
   - Verify chat interface loads
   - Test file upload functionality

2. **Test Analysis Types**
   - Click + icon to open analysis menu
   - Select different analysis types
   - Verify AI responses

3. **Mobile Testing**
   - Test on mobile devices
   - Verify responsive design
   - Check sidebar functionality

## 🚨 Troubleshooting

### Common Deployment Issues

**Build Failures:**
```bash
# Check requirements.txt
pip freeze > requirements.txt

# Verify Python version
python --version

# Test locally first
python src/main.py
```

**OpenAI API Issues:**
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check quota
# Visit platform.openai.com/usage
```

**CORS Issues:**
```python
# Verify CORS configuration in main.py
CORS(app, origins="*")
```

### Monitoring and Logs

**Railway Logs:**
- View real-time logs in Railway dashboard
- Monitor deployment status
- Check error messages

**Application Monitoring:**
```python
# Add logging to your application
import logging
logging.basicConfig(level=logging.INFO)
```

### Performance Optimization

**File Upload Optimization:**
```python
# Increase upload limits if needed
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

**Response Caching:**
```python
# Add response caching for better performance
from flask_caching import Cache
cache = Cache(app)
```

## 📊 Monitoring and Analytics

### Railway Monitoring

1. **Built-in Metrics**
   - CPU and memory usage
   - Request/response times
   - Error rates

2. **Custom Monitoring**
   ```python
   # Add custom metrics
   @app.route('/api/metrics')
   def metrics():
       return {
           'requests_total': request_count,
           'errors_total': error_count,
           'response_time_avg': avg_response_time
       }
   ```

### External Monitoring

**Uptime Monitoring:**
- Use services like UptimeRobot
- Monitor `/api/health` endpoint
- Set up alerts for downtime

**Error Tracking:**
```python
# Add error tracking (e.g., Sentry)
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

## 🔒 Security Considerations

### API Key Security

1. **Never Commit API Keys**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   echo "*.key" >> .gitignore
   ```

2. **Use Environment Variables**
   ```python
   import os
   api_key = os.getenv('OPENAI_API_KEY')
   ```

3. **Rotate Keys Regularly**
   - Generate new API keys periodically
   - Update in deployment environment

### File Upload Security

```python
# Validate file types
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

# Limit file sizes
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Sanitize filenames
from werkzeug.utils import secure_filename
filename = secure_filename(file.filename)
```

## 📈 Scaling Considerations

### Horizontal Scaling

**Railway Auto-scaling:**
- Configure auto-scaling in Railway dashboard
- Set CPU and memory thresholds
- Monitor scaling events

**Load Balancing:**
```python
# Ensure stateless application design
# Use external session storage if needed
app.config['SESSION_TYPE'] = 'redis'
```

### Database Scaling

**External Database:**
```python
# Use PostgreSQL for production
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

### CDN Integration

**Static File Delivery:**
- Use Railway's built-in CDN
- Or integrate with Cloudflare
- Optimize asset delivery

---

**Ready to deploy your Legal AI Assistant! 🚀**

For additional support, check the Railway documentation or create an issue in your repository.

