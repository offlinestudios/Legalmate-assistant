from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import os
import uuid
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from datetime import datetime
import openai

files_bp = Blueprint('files', __name__)

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return None

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting DOCX text: {str(e)}")
        return None

def extract_text_from_doc(file_path):
    """Extract text from DOC file (basic support)"""
    try:
        # For .doc files, we'll try to read as text (limited support)
        with open(file_path, 'rb') as file:
            content = file.read()
            # This is a basic approach - for production, consider using python-docx2txt or antiword
            text = content.decode('utf-8', errors='ignore')
            return text
    except Exception as e:
        print(f"Error extracting DOC text: {str(e)}")
        return None

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting TXT text: {str(e)}")
        return None

@files_bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    """Upload and process a file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        analysis_type = request.form.get('analysis_type', 'general')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload PDF, DOC, DOCX, or TXT files.'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Extract text based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        extracted_text = None
        
        if file_extension == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            extracted_text = extract_text_from_docx(file_path)
        elif file_extension == 'doc':
            extracted_text = extract_text_from_doc(file_path)
        elif file_extension == 'txt':
            extracted_text = extract_text_from_txt(file_path)
        
        # Clean up - remove uploaded file after processing
        try:
            os.remove(file_path)
        except:
            pass
        
        if extracted_text is None:
            return jsonify({'error': 'Failed to extract text from file'}), 500
        
        # Truncate text if too long (keep first 10000 characters)
        if len(extracted_text) > 10000:
            extracted_text = extracted_text[:10000] + "\n\n[Document truncated for processing...]"
        
        return jsonify({
            'success': True,
            'filename': filename,
            'text': extracted_text,
            'file_size': file_size,
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"File upload error: {str(e)}")
        return jsonify({'error': 'Failed to process file'}), 500

@files_bp.route('/analyze-document', methods=['POST'])
@cross_origin()
def analyze_document():
    """Analyze uploaded document with AI"""
    try:
        data = request.get_json()
        document_text = data.get('text', '')
        analysis_type = data.get('analysis_type', 'general')
        filename = data.get('filename', 'document')
        
        if not document_text:
            return jsonify({'error': 'Document text is required'}), 400
        
        # Analysis prompts for different types
        analysis_prompts = {
            'plain_english': f"Please analyze this legal document and translate any complex legal language into clear, understandable terms. Explain key concepts and highlight important clauses:\n\n{document_text}",
            'risk_analysis': f"Please perform a risk analysis on this legal document. Identify potential risks, unfavorable terms, and areas of concern:\n\n{document_text}",
            'negotiation': f"Please review this legal document and suggest negotiation strategies, fairer terms, and areas for improvement:\n\n{document_text}",
            'deal_advisor': f"Please provide strategic advice on this agreement. What terms should be requested, what should be avoided, and what are the key considerations:\n\n{document_text}",
            'dispute_resolution': f"Please analyze this document for potential dispute resolution strategies and conflict management approaches:\n\n{document_text}",
            'document_generator': f"Please review this document and suggest improvements, missing clauses, or template enhancements:\n\n{document_text}",
            'general': f"Please analyze this legal document and provide helpful insights, explanations, and recommendations:\n\n{document_text}"
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts['general'])
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful legal AI assistant. Provide thorough, accurate analysis while being clear that you don't replace qualified legal professionals for specific legal matters."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        analysis_result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'filename': filename,
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Document analysis error: {str(e)}")
        return jsonify({'error': 'Failed to analyze document'}), 500

@files_bp.route('/supported-formats', methods=['GET'])
@cross_origin()
def get_supported_formats():
    """Get list of supported file formats"""
    return jsonify({
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024),
        'description': {
            'pdf': 'Portable Document Format',
            'doc': 'Microsoft Word Document (legacy)',
            'docx': 'Microsoft Word Document',
            'txt': 'Plain Text File'
        }
    })

