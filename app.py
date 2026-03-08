"""
RHISA Healthcare Chatbot - Main Application
Regional Health Insight & Support Agent for Gujarat and Maharashtra
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from datetime import datetime
import os
from agents.knowledge_agent import KnowledgeAgent
from agents.trend_analyzer import TrendAnalyzer
from agents.compliance_checker import ComplianceChecker
from data.synthetic_generator import SyntheticDataGenerator
from config.settings import Config
from utils.language_processor import LanguageProcessor
from utils.entity_extractor import EntityExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize components
knowledge_agent = KnowledgeAgent()
trend_analyzer = TrendAnalyzer()
compliance_checker = ComplianceChecker()
synthetic_generator = SyntheticDataGenerator()
language_processor = LanguageProcessor()
entity_extractor = EntityExtractor()

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('index.html')

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'service': 'RHISA Healthcare Chatbot'
    })

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        region = data.get('region', 'gujarat')
        language = data.get('language', 'en')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Extract entities from user message
        entities = entity_extractor.extract_entities(user_message)
        
        # Determine intent and route to appropriate agent
        intent = _classify_intent(user_message, entities)
        
        response = _process_request(intent, user_message, region, language, entities)
        
        return jsonify({
            'response': response,
            'intent': intent,
            'entities': entities,
            'region': region,
            'language': language,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/knowledge/search', methods=['GET'])
def search_knowledge():
    """Search knowledge base"""
    try:
        query = request.args.get('query', '')
        region = request.args.get('region', 'gujarat')
        language = request.args.get('language', 'en')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = knowledge_agent.search(query, region, language)
        
        return jsonify({
            'results': results,
            'query': query,
            'region': region,
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/v1/trends/<region>/<condition>', methods=['GET'])
def get_trends(region, condition):
    """Get health trends for specific region and condition"""
    try:
        trends = trend_analyzer.analyze_trends(region, condition)
        
        return jsonify({
            'trends': trends,
            'region': region,
            'condition': condition,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        return jsonify({'error': 'Trend analysis failed'}), 500

@app.route('/api/v1/compliance/check', methods=['POST'])
def check_compliance():
    """Check compliance with regional guidelines"""
    try:
        data = request.get_json()
        case_data = data.get('case_data', {})
        region = data.get('region', 'gujarat')
        
        compliance_result = compliance_checker.check_compliance(case_data, region)
        
        return jsonify({
            'compliance': compliance_result,
            'region': region,
            'checked_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error checking compliance: {str(e)}")
        return jsonify({'error': 'Compliance check failed'}), 500

@app.route('/api/v1/patient-education', methods=['POST'])
def generate_patient_education():
    """Generate patient education materials"""
    try:
        data = request.get_json()
        condition = data.get('condition', '')
        language = data.get('language', 'en')
        region = data.get('region', 'gujarat')
        
        education_content = knowledge_agent.generate_patient_education(
            condition, language, region
        )
        
        return jsonify({
            'content': education_content,
            'condition': condition,
            'language': language,
            'region': region
        })
        
    except Exception as e:
        logger.error(f"Error generating patient education: {str(e)}")
        return jsonify({'error': 'Education content generation failed'}), 500

def _classify_intent(message, entities):
    """Classify user intent based on message and entities"""
    message_lower = message.lower()
    
    # Intent classification logic
    if any(word in message_lower for word in ['trend', 'pattern', 'statistics', 'data']):
        return 'trend_analysis'
    elif any(word in message_lower for word in ['guideline', 'compliance', 'policy', 'rule']):
        return 'compliance_check'
    elif any(word in message_lower for word in ['education', 'explain', 'what is', 'how to']):
        return 'patient_education'
    elif any(word in message_lower for word in ['search', 'find', 'lookup', 'information']):
        return 'knowledge_search'
    else:
        return 'general_query'

def _process_request(intent, message, region, language, entities):
    """Process request based on intent"""
    try:
        if intent == 'trend_analysis':
            # Extract condition from entities or message
            condition = _extract_condition(entities, message)
            return trend_analyzer.analyze_and_explain(region, condition, language)
            
        elif intent == 'compliance_check':
            # Create case data from message
            case_data = _create_case_data(entities, message)
            return compliance_checker.check_and_explain(case_data, region, language)
            
        elif intent == 'patient_education':
            condition = _extract_condition(entities, message)
            return knowledge_agent.generate_patient_education(condition, language, region)
            
        elif intent == 'knowledge_search':
            return knowledge_agent.search_and_respond(message, region, language)
            
        else:
            return knowledge_agent.general_response(message, region, language)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return f"I apologize, but I encountered an error processing your request. Please try again."

def _extract_condition(entities, message):
    """Extract medical condition from entities or message"""
    # Look for medical conditions in entities
    for entity in entities:
        if entity.get('type') == 'CONDITION':
            return entity.get('text', '')
    
    # Fallback to keyword matching
    conditions = ['diabetes', 'hypertension', 'cataract', 'glaucoma', 'dermatitis', 'eczema']
    message_lower = message.lower()
    
    for condition in conditions:
        if condition in message_lower:
            return condition
    
    return 'general'

def _create_case_data(entities, message):
    """Create case data structure from entities and message"""
    case_data = {
        'conditions': [],
        'medications': [],
        'symptoms': [],
        'demographics': {}
    }
    
    for entity in entities:
        entity_type = entity.get('type', '')
        entity_text = entity.get('text', '')
        
        if entity_type == 'CONDITION':
            case_data['conditions'].append(entity_text)
        elif entity_type == 'MEDICATION':
            case_data['medications'].append(entity_text)
        elif entity_type == 'SYMPTOM':
            case_data['symptoms'].append(entity_text)
    
    return case_data

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)