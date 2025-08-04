# LegalMate Deployment Guide

## Quick Start

Your LegalMate AI Legal Assistant is ready for deployment! This guide covers different deployment options.

## Architecture Overview

- **Frontend**: React application (can be deployed as static files)
- **Backend**: Flask API (requires server deployment)
- **Database**: SQLite (included)
- **AI Integration**: OpenAI API (requires API key)

## Deployment Options

### Option 1: Separate Frontend/Backend Deployment (Recommended)

#### Frontend Deployment (Static Hosting)
Deploy to GitHub Pages, Netlify, or Vercel:

1. **GitHub Pages**:
   ```bash
   # Build the frontend
   cd frontend
   pnpm run build
   
   # Create gh-pages branch and deploy
   npm install -g gh-pages
   gh-pages -d dist
   ```

2. **Netlify**:
   - Connect your GitHub repository
   - Set build command: `cd frontend && pnpm run build`
   - Set publish directory: `frontend/dist`

3. **Vercel**:
   - Connect your GitHub repository
   - Framework preset: Vite
   - Root directory: `frontend`

#### Backend Deployment (Server Required)

1. **Heroku**:
   ```bash
   # Create Procfile in backend directory
   echo "web: python src/main.py" > backend/Procfile
   
   # Deploy to Heroku
   cd backend
   heroku create your-legalmate-api
   heroku config:set OPENAI_API_KEY=your_api_key
   git subtree push --prefix backend heroku master
   ```

2. **Railway**:
   - Connect GitHub repository
   - Set root directory to `backend`
   - Add environment variable: `OPENAI_API_KEY`

3. **DigitalOcean App Platform**:
   - Connect GitHub repository
   - Configure as Python app
   - Set environment variables

### Option 2: Integrated Deployment (Full-Stack)

Deploy both frontend and backend together:

```bash
# Build frontend
cd frontend
pnpm run build

# Copy to backend static directory
cp -r dist/* ../backend/src/static/

# Deploy backend (which now serves the frontend)
cd ../backend
# Deploy to your preferred platform
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional
- `FLASK_ENV`: Set to `production` for production
- `PORT`: Port number (default: 5000)

## Domain Configuration

### Frontend URL Update
If deploying separately, update the API URL in `frontend/src/App.jsx`:

```javascript
// Change from localhost to your backend URL
const response = await fetch('https://your-backend-url.com/api/analyze', {
```

### CORS Configuration
The backend is configured to allow all origins. For production, update CORS settings in `backend/src/main.py`:

```python
CORS(app, origins=['https://your-frontend-domain.com'])
```

## SSL/HTTPS

Most hosting platforms provide SSL certificates automatically. Ensure both frontend and backend use HTTPS in production.

## Monitoring and Logs

- Check application logs in your hosting platform dashboard
- Monitor API usage in OpenAI dashboard
- Set up error tracking (Sentry, etc.) if needed

## Scaling Considerations

- **Frontend**: Automatically scales with CDN
- **Backend**: Consider load balancing for high traffic
- **Database**: Upgrade to PostgreSQL for production scale
- **AI API**: Monitor OpenAI usage and rate limits

## Security Checklist

- [ ] Environment variables properly set
- [ ] CORS configured for production domains
- [ ] HTTPS enabled
- [ ] API keys secured
- [ ] Database access restricted
- [ ] Error messages don't expose sensitive data

## Cost Estimation

### Hosting Costs (Monthly)
- **Frontend**: $0 (GitHub Pages, Netlify free tier)
- **Backend**: $5-25 (Heroku, Railway, DigitalOcean)
- **OpenAI API**: Variable based on usage

### Usage-Based Costs
- OpenAI API: ~$0.002 per 1K tokens
- Estimated cost per analysis: $0.01-0.05
- 1000 analyses/month: ~$10-50

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Check backend CORS configuration
   - Verify frontend API URLs

2. **OpenAI API Errors**:
   - Verify API key is set correctly
   - Check API usage limits
   - Ensure model name is correct

3. **Build Failures**:
   - Check Node.js version compatibility
   - Verify all dependencies are installed

4. **Database Issues**:
   - Ensure SQLite file permissions
   - Check database initialization

## Support

For deployment issues:
1. Check the logs in your hosting platform
2. Verify environment variables
3. Test API endpoints directly
4. Review the README.md for setup instructions

## Next Steps

After deployment:
1. Test all AI modes with real documents
2. Monitor performance and usage
3. Set up analytics and user feedback
4. Consider adding user authentication
5. Implement usage tracking and billing

---

Your LegalMate AI Legal Assistant is now ready for the world! 🚀

