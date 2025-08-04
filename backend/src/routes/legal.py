from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import openai
import os

legal_bp = Blueprint('legal', __name__)

# AI mode prompts for different legal analysis types
AI_MODE_PROMPTS = {
    'translator': """You are a legal translator. Explain the following legal document in plain English, making it easy for a non-lawyer to understand. Break down complex legal terms and clauses into simple language. Focus on what the document means in practical terms for the person involved.

Document to analyze:
{document}

Provide a clear, plain English explanation:""",
    
    'risk': """You are a legal risk analyst. Analyze the following document and identify any problematic, one-sided, or potentially harmful clauses. Look for terms that heavily favor one party, vague language that could be exploited, unreasonable obligations, or missing protections.

Document to analyze:
{document}

Identify the risks and problematic clauses:""",
    
    'negotiator': """You are a legal negotiation expert. Review the following document and suggest fairer, more balanced alternatives to problematic clauses. Provide specific counter-proposals that would better protect the interests of both parties.

Document to analyze:
{document}

Suggest negotiation points and fairer alternatives:""",
    
    'agent': """You are a deal strategy advisor. Based on the following document or deal description, suggest what terms, protections, and clauses should be requested to ensure a fair and beneficial agreement. Think like an experienced agent protecting their client's interests.

Document/Deal to analyze:
{document}

Suggest what terms and protections to ask for:""",
    
    'dispute': """You are a dispute resolution specialist. Based on the situation described, help draft a professional complaint, refund request, or dispute letter. Provide a template that is firm but professional, citing relevant issues and requesting appropriate remedies.

Situation to address:
{document}

Draft a professional dispute letter:""",
    
    'template': """You are a legal document generator. Based on the request, create a professional legal document template. Include all necessary clauses, terms, and protections typically found in this type of document.

Document type requested:
{document}

Generate the legal document template:"""
}

@legal_bp.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_document():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        document_text = data.get('document', '').strip()
        mode = data.get('mode', 'translator')
        
        if not document_text:
            return jsonify({'error': 'Document text is required'}), 400
        
        if mode not in AI_MODE_PROMPTS:
            return jsonify({'error': 'Invalid analysis mode'}), 400
        
        # Get the appropriate prompt for the selected mode
        prompt = AI_MODE_PROMPTS[mode].format(document=document_text)
        
        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are LegalMate, an AI legal assistant that helps people understand and navigate legal documents and situations. Provide helpful, accurate, and practical legal guidance while being clear that you're not providing formal legal advice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'mode': mode
        })
        
    except openai.APIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@legal_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat_with_legalmate():
    """Chat endpoint for conversational AI interaction"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_message = data.get('message', '').strip()
        context = data.get('context', [])
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Build conversation context
        messages = [
            {
                "role": "system", 
                "content": """You are LegalMate, a friendly and knowledgeable AI legal assistant. You help people with:

- Contract review and analysis
- Legal document explanation in plain English
- Risk identification in agreements
- Negotiation strategies and advice
- Legal rights and obligations
- Document templates and forms
- Dispute resolution guidance
- General legal questions

Guidelines:
- Be conversational, helpful, and professional
- Explain legal concepts in simple terms
- Always clarify that you provide information, not formal legal advice
- For complex matters, recommend consulting with a qualified attorney
- Be proactive in offering specific help and asking clarifying questions
- If someone shares a document, offer to analyze it in different modes (risk, translation, negotiation, etc.)
- Provide practical, actionable advice when possible
- Keep responses concise but comprehensive
- Use a warm, approachable tone while maintaining professionalism

You can help with contracts, leases, employment agreements, freelance contracts, NDAs, terms of service, and many other legal documents and situations."""
            }
        ]
        
        # Add recent conversation context (last 5 messages)
        for msg in context[-5:]:
            if msg.get('sender') == 'user':
                messages.append({"role": "user", "content": msg.get('message', '')})
            elif msg.get('sender') == 'bot' and not msg.get('isTyping'):
                messages.append({"role": "assistant", "content": msg.get('message', '')})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=800,
            temperature=0.8
        )
        
        bot_response = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
        
    except openai.APIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@legal_bp.route('/templates', methods=['GET'])
@cross_origin()
def get_templates():
    """Get available legal document templates"""
    templates = [
        {
            'id': 'freelance_contract',
            'name': 'Freelance Contract',
            'description': 'Standard freelance service agreement'
        },
        {
            'id': 'nda',
            'name': 'Non-Disclosure Agreement',
            'description': 'Confidentiality agreement template'
        },
        {
            'id': 'service_agreement',
            'name': 'Service Agreement',
            'description': 'General service provider agreement'
        },
        {
            'id': 'rental_letter',
            'name': 'Rental Notice Letter',
            'description': 'Template for rental-related correspondence'
        },
        {
            'id': 'dmca_notice',
            'name': 'DMCA Takedown Notice',
            'description': 'Copyright infringement takedown request'
        }
    ]
    
    return jsonify({
        'success': True,
        'templates': templates
    })

@legal_bp.route('/generate-template', methods=['POST'])
@cross_origin()
def generate_template():
    """Generate a specific legal document template"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        template_type = data.get('template_type', '').strip()
        custom_details = data.get('details', '').strip()
        
        if not template_type:
            return jsonify({'error': 'Template type is required'}), 400
        
        # Create prompt for template generation
        prompt = f"Generate a professional {template_type} template. "
        if custom_details:
            prompt += f"Include these specific details: {custom_details}. "
        prompt += "Make it comprehensive but easy to customize."
        
        # Use the template mode prompt
        full_prompt = AI_MODE_PROMPTS['template'].format(document=prompt)
        
        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are LegalMate, an AI legal assistant that generates professional legal document templates. Create comprehensive, well-structured templates that users can customize for their needs."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )
        
        template = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'template': template,
            'template_type': template_type
        })
        
    except openai.APIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@legal_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'LegalMate API is running',
        'version': '1.0.0'
    })

