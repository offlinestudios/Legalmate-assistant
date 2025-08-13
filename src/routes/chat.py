from flask import Blueprint, request, jsonify, stream_template
from flask_cors import cross_origin
import openai
import os
import json
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Legal AI Assistant system prompts for different analysis types
ANALYSIS_PROMPTS = {
    'plain_english': """You are a legal AI assistant specializing in translating complex legal language into clear, understandable terms. 
    Your role is to:
    - Break down complex legal jargon into plain English
    - Explain legal concepts in simple terms
    - Maintain accuracy while improving readability
    - Highlight key points and important clauses
    Always be helpful, accurate, and professional.""",
    
    'risk_analysis': """You are a legal AI assistant specializing in risk analysis and contract review.
    Your role is to:
    - Identify potential risks and unfavorable terms in legal documents
    - Highlight clauses that could be problematic
    - Suggest areas that need attention or negotiation
    - Explain the implications of specific terms
    - Provide risk assessment and mitigation strategies
    Always be thorough, analytical, and professional.""",
    
    'negotiation': """You are a legal AI assistant specializing in contract negotiation and strategy.
    Your role is to:
    - Suggest fairer terms and negotiation strategies
    - Identify leverage points in agreements
    - Recommend alternative language for problematic clauses
    - Provide negotiation tactics and approaches
    - Help balance interests between parties
    Always be strategic, practical, and professional.""",
    
    'deal_advisor': """You are a legal AI assistant specializing in deal advisory and strategic guidance.
    Your role is to:
    - Provide strategic advice on agreement terms
    - Suggest what terms to request in negotiations
    - Analyze deal structure and implications
    - Recommend protective clauses and provisions
    - Guide on industry-standard practices
    Always be strategic, insightful, and professional.""",
    
    'dispute_resolution': """You are a legal AI assistant specializing in dispute resolution and conflict management.
    Your role is to:
    - Provide guidance on resolving conflicts and disputes
    - Suggest mediation and resolution strategies
    - Help recover what parties are owed
    - Analyze dispute scenarios and options
    - Recommend next steps for resolution
    Always be solution-oriented, practical, and professional.""",
    
    'document_generator': """You are a legal AI assistant specializing in document creation and template generation.
    Your role is to:
    - Create professional legal documents and contracts
    - Generate templates for common legal needs
    - Provide structured document formats
    - Include necessary clauses and provisions
    - Ensure documents are comprehensive and professional
    Always be thorough, accurate, and professional.""",
    
    'general': """You are a helpful legal AI assistant. You can help with any legal issue - from analyzing contracts and identifying risks to providing guidance on negotiations and disputes. 
    You provide accurate, helpful legal information while being clear that you don't replace qualified legal professionals for specific legal matters.
    Always be helpful, accurate, and professional."""
}

@chat_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        analysis_type = data.get('analysis_type', 'general')
        conversation_history = data.get('conversation_history', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get the appropriate system prompt
        system_prompt = ANALYSIS_PROMPTS.get(analysis_type, ANALYSIS_PROMPTS['general'])
        
        # Build messages for OpenAI API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=2000,
            temperature=0.7,
            stream=False
        )
        
        ai_response = response.choices[0].message.content
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'analysis_type': analysis_type
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({'error': 'Failed to process chat request'}), 500

@chat_bp.route('/chat/stream', methods=['POST'])
@cross_origin()
def chat_stream():
    """Streaming chat endpoint for real-time responses"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        analysis_type = data.get('analysis_type', 'general')
        conversation_history = data.get('conversation_history', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get the appropriate system prompt
        system_prompt = ANALYSIS_PROMPTS.get(analysis_type, ANALYSIS_PROMPTS['general'])
        
        # Build messages for OpenAI API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        def generate():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=2000,
                    temperature=0.7,
                    stream=True
                )
                
                for chunk in response:
                    if chunk.choices[0].delta.get('content'):
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return app.response_class(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*'
            }
        )
        
    except Exception as e:
        print(f"Stream chat error: {str(e)}")
        return jsonify({'error': 'Failed to process streaming chat request'}), 500

@chat_bp.route('/analysis-types', methods=['GET'])
@cross_origin()
def get_analysis_types():
    """Get available analysis types"""
    analysis_types = [
        {
            'id': 'plain_english',
            'title': 'Plain English',
            'description': 'Translate complex legal language into clear, understandable terms',
            'icon': 'Languages'
        },
        {
            'id': 'risk_analysis',
            'title': 'Risk Analysis',
            'description': 'Identify potential risks and unfavorable terms in your documents',
            'icon': 'Shield'
        },
        {
            'id': 'negotiation',
            'title': 'Negotiation',
            'description': 'Get suggestions for fairer terms and negotiation strategies',
            'icon': 'Scale'
        },
        {
            'id': 'deal_advisor',
            'title': 'Deal Advisor',
            'description': 'Strategic advice on what terms to request in your agreements',
            'icon': 'Handshake'
        },
        {
            'id': 'dispute_resolution',
            'title': 'Dispute Resolution',
            'description': 'Guidance on resolving conflicts and recovering what you\'re owed',
            'icon': 'AlertTriangle'
        },
        {
            'id': 'document_generator',
            'title': 'Document Generator',
            'description': 'Create professional legal documents and contract templates',
            'icon': 'FileText'
        }
    ]
    
    return jsonify({'analysis_types': analysis_types})

