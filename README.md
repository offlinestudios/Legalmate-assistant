# LegalMate - Your AI Legal Assistant with Conversational Chatbot

LegalMate is a comprehensive AI-powered legal assistant that helps users review contracts, detect risks, generate negotiations, and create legal documents. **Now enhanced with interactive chatbot and voice capabilities!** Built for freelancers, tenants, creators, small business owners, and anyone dealing with legal documents without paying expensive lawyer fees.

## 🚀 New Enhanced Features

### 🤖 **Dual Interface Modes**
- **Document Analysis Mode** - Structured analysis with 6 specialized AI modes
- **Chat Mode** - Natural conversation with AI legal assistant

### 🗣️ **Voice Interaction**
- **Speech-to-Text** - Speak your legal questions using microphone
- **Text-to-Speech** - Hear LegalMate's responses read aloud
- **Voice Controls** - Easy toggle for voice features

### 💬 **Conversational AI**
- **Natural Language Processing** - Ask questions in plain English
- **Context Awareness** - Remembers conversation history for follow-ups
- **Smart Suggestions** - Pre-built prompts like "Review this contract for red flags"
- **Professional Guidance** - Like having a lawyer available 24/7

## Features

### AI Legal Assistant Modes

- **🧑‍🎓 Translator Mode**: Explains legal documents in plain English
- **🕵️ Risk Mode**: Identifies problematic clauses and one-sided terms
- **✍️ Negotiator Mode**: Generates fairer counter-proposals
- **💼 Agent Mode**: Suggests deal terms and protections
- **📢 Dispute Mode**: Creates professional complaint letters
- **📃 Template Mode**: Generates legal document templates

### Key Benefits

- 24/7 AI-powered legal assistance
- No $300/hour lawyer fees
- Instant legal guidance
- Contract review and risk detection
- Negotiation help and strategy
- Legal document templates

## Technology Stack

### Frontend
- **React** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/UI** - High-quality component library
- **Lucide Icons** - Beautiful icon set
- **Vite** - Fast build tool

### Backend
- **Flask** - Lightweight Python web framework
- **OpenAI API** - AI-powered legal analysis
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database for user data

## Project Structure

```
legalmate/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── assets/          # Static assets
│   │   ├── App.jsx          # Main application component
│   │   └── main.jsx         # Entry point
│   ├── public/              # Public assets
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
├── backend/                 # Flask API
│   ├── src/
│   │   ├── routes/          # API route handlers
│   │   │   ├── legal.py     # Legal analysis endpoints
│   │   │   └── user.py      # User management
│   │   ├── models/          # Database models
│   │   ├── static/          # Static files for deployment
│   │   └── main.py          # Flask application entry point
│   ├── venv/                # Python virtual environment
│   └── requirements.txt     # Python dependencies
├── README.md                # Project documentation
└── .gitignore              # Git ignore rules
```

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- Python 3.11+
- OpenAI API key

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm run dev --host
   ```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

5. Start the Flask server:
   ```bash
   python src/main.py
   ```

The backend API will be available at `http://localhost:5000`

## API Endpoints

### Legal Analysis
- `POST /api/analyze` - Analyze legal documents
- `GET /api/templates` - Get available templates
- `POST /api/generate-template` - Generate legal document templates
- `GET /api/health` - Health check endpoint

### Request Format

```json
{
  "document": "Your legal document text here...",
  "mode": "risk|translator|negotiator|agent|dispute|template"
}
```

### Response Format

```json
{
  "success": true,
  "analysis": "AI-generated legal analysis...",
  "mode": "risk"
}
```

## Deployment

### Frontend Deployment

The frontend can be deployed to any static hosting service:

1. Build the production version:
   ```bash
   cd frontend
   pnpm run build
   ```

2. Deploy the `dist/` folder to:
   - GitHub Pages
   - Netlify
   - Vercel
   - AWS S3
   - Any static hosting service

### Backend Deployment

The backend can be deployed to cloud platforms:

1. **Heroku**:
   - Add `Procfile`: `web: python src/main.py`
   - Set environment variables in Heroku dashboard

2. **Railway**:
   - Connect GitHub repository
   - Set environment variables

3. **AWS/GCP/Azure**:
   - Use container deployment with Docker
   - Set up environment variables

### Full-Stack Deployment

For integrated deployment, build the frontend and place it in the backend's static directory:

```bash
# Build frontend
cd frontend
pnpm run build

# Copy to backend static directory
cp -r dist/* ../backend/src/static/

# Deploy backend with integrated frontend
cd ../backend
# Deploy to your preferred platform
```

## Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key for AI analysis

### Optional
- `FLASK_ENV` - Set to `production` for production deployment
- `SECRET_KEY` - Flask secret key (auto-generated if not set)

## Development

### Adding New AI Modes

1. Add the mode to `AI_MODE_PROMPTS` in `backend/src/routes/legal.py`
2. Add the mode option to the frontend in `frontend/src/App.jsx`
3. Update the UI with appropriate icons and descriptions

### Customizing the UI

The frontend uses Tailwind CSS for styling. Modify components in `frontend/src/App.jsx` or create new components in `frontend/src/components/`.

### API Extensions

Add new endpoints in `backend/src/routes/` and register them in `backend/src/main.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Pricing Tiers

### Free Tier
- 3 document uploads/month
- Basic contract summaries
- Limited AI modes

### Pro Tier ($12.99/month)
- Unlimited document reviews
- All AI modes
- Negotiation tools
- Letter generation

### Agent+ Tier ($29.99/month)
- Everything in Pro
- Legal strategy prompts
- Deal agent mode
- Access to paralegals

---

**Disclaimer**: LegalMate provides AI-powered legal assistance for informational purposes only. It does not constitute formal legal advice. For complex legal matters, consult with a qualified attorney.

