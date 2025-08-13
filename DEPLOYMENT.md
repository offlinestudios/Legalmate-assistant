# Railway Deployment Guide

## 🚀 Step-by-Step Railway Deployment

### Prerequisites
- GitHub account
- Railway account (free tier available)
- OpenAI API key

### Step 1: Prepare Repository

1. **Extract the package**
   ```bash
   unzip legal-ai-railway-ready.zip
   cd legal-ai-railway-ready
   ```

2. **Initialize Git repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Legal AI Assistant for Railway"
   ```

3. **Create GitHub repository**
   - Go to GitHub and create a new repository
   - Don't initialize with README (we already have one)

4. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Railway Auto-Detection**
   Railway will automatically:
   - Detect Python application from `requirements.txt`
   - Use `Procfile` for start command
   - Apply `railway.json` configuration
   - Set up health checks

### Step 3: Configure Environment

1. **Set Environment Variables**
   - Go to your project in Railway
   - Click "Variables" tab
   - Add: `OPENAI_API_KEY` = `your_openai_api_key_here`

2. **Optional Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key
   MAX_FILE_SIZE_MB=16
   ```

### Step 4: Monitor Deployment

1. **Watch Build Process**
   - Go to "Deployments" tab
   - Click on the active deployment
   - Monitor build logs

2. **Expected Build Steps**
   ```
   ✅ Detecting Python application
   ✅ Installing dependencies from requirements.txt
   ✅ Setting up Flask application
   ✅ Starting with: python src/main.py
   ✅ Health check: /api/health responding
   ```

3. **Get Your URL**
   - Railway provides a URL like: `https://your-app-name.railway.app`
   - Visit the URL to see your application

### Step 5: Verify Deployment

1. **Test Frontend**
   - Visit your Railway URL
   - Verify chat interface loads
   - Test responsive design on mobile

2. **Test Backend**
   - Try sending a chat message
   - Upload a document
   - Test different analysis types

3. **Check Health Endpoint**
   ```bash
   curl https://your-app-name.railway.app/api/health
   ```

## 🔧 Configuration Files Explained

### `Procfile`
```
web: python src/main.py
```
Tells Railway how to start your application.

### `runtime.txt`
```
python-3.11.0
```
Specifies Python version for Railway.

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/main.py",
    "healthcheckPath": "/api/health"
  }
}
```
Railway-specific configuration for build and deployment.

### `requirements.txt`
Lists all Python dependencies that Railway will install.

## 🚨 Troubleshooting

### Build Failures

**"No Python application detected"**
- Ensure `requirements.txt` is at repository root
- Check that file is not empty
- Verify proper Python package names

**"Start command failed"**
- Check `Procfile` syntax
- Verify `src/main.py` exists
- Ensure Flask app runs locally first

**"Port binding failed"**
- Verify app uses `os.environ.get('PORT', 5000)`
- Ensure app binds to `0.0.0.0`, not `localhost`

### Runtime Errors

**"OpenAI API Error"**
- Check `OPENAI_API_KEY` is set in Railway variables
- Verify API key is valid and has credits
- Test API key locally first

**"File upload not working"**
- Check file size limits (16MB default)
- Verify supported file types
- Monitor Railway logs for specific errors

**"Frontend not loading"**
- Ensure `src/static/` contains built React files
- Check Flask static file serving configuration
- Verify `index.html` exists in `src/static/`

### Performance Issues

**Slow responses**
- Monitor Railway resource usage
- Check OpenAI API response times
- Consider upgrading Railway plan

**Memory issues**
- Monitor memory usage in Railway dashboard
- Optimize file processing for large documents
- Consider external file storage for production

## 📊 Monitoring & Maintenance

### Railway Dashboard
- **Deployments**: View build and deployment history
- **Metrics**: Monitor CPU, memory, and network usage
- **Logs**: Real-time application logs
- **Variables**: Manage environment variables

### Health Monitoring
- Health check endpoint: `/api/health`
- Status endpoint: `/api/status`
- Set up external monitoring (UptimeRobot, etc.)

### Log Monitoring
```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs --follow
```

## 🔄 Updates & Redeployment

### Code Updates
```bash
# Make your changes
git add .
git commit -m "Update: description of changes"
git push origin main
```
Railway automatically redeploys on push to main branch.

### Environment Variable Updates
- Update in Railway dashboard
- No redeployment needed for most variables
- Some changes may require restart

### Rollback
- Go to Railway → Deployments
- Click on previous successful deployment
- Click "Redeploy"

## 🎯 Production Considerations

### Custom Domain
1. Railway → Settings → Domains
2. Add your custom domain
3. Configure DNS records as shown
4. SSL certificate automatically provided

### Database Upgrade
For production, consider PostgreSQL:
1. Add PostgreSQL service in Railway
2. Update `DATABASE_URL` environment variable
3. Modify database configuration in code

### Scaling
- Railway automatically scales based on traffic
- Monitor usage and upgrade plan as needed
- Consider CDN for static assets

### Security
- Rotate API keys regularly
- Monitor usage and costs
- Set up alerts for unusual activity
- Keep dependencies updated

## 💰 Cost Management

### Railway Pricing
- Free tier: Limited hours and resources
- Pro plan: $5/month for more resources
- Monitor usage in dashboard

### OpenAI Costs
- Set usage limits in OpenAI dashboard
- Monitor token usage
- Consider caching responses for common queries

---

## ✅ Success Checklist

Before going live:
- [ ] Application builds successfully
- [ ] Health check responds at `/api/health`
- [ ] Chat functionality works with OpenAI
- [ ] File upload and processing works
- [ ] Mobile interface is responsive
- [ ] Environment variables are set
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Usage limits configured

**Your Legal AI Assistant is now live on Railway! 🎉**

