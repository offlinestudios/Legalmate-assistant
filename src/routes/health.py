from flask import Blueprint, jsonify
from flask_cors import cross_origin
import os
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint for Railway deployment"""
    try:
        # Check if OpenAI API key is configured
        openai_configured = bool(os.getenv('OPENAI_API_KEY'))
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Legal AI Assistant Backend',
            'version': '1.0.0',
            'openai_configured': openai_configured,
            'endpoints': {
                'chat': '/api/chat',
                'chat_stream': '/api/chat/stream',
                'file_upload': '/api/upload',
                'document_analysis': '/api/analyze-document',
                'analysis_types': '/api/analysis-types',
                'supported_formats': '/api/supported-formats'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@health_bp.route('/status', methods=['GET'])
@cross_origin()
def status():
    """Detailed status endpoint"""
    try:
        return jsonify({
            'service': 'Legal AI Assistant Backend',
            'status': 'running',
            'version': '1.0.0',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'python_version': '3.11',
            'features': {
                'chat': True,
                'file_upload': True,
                'document_analysis': True,
                'streaming_chat': True,
                'multiple_analysis_types': True
            },
            'supported_file_types': ['pdf', 'doc', 'docx', 'txt'],
            'max_file_size_mb': 16,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

