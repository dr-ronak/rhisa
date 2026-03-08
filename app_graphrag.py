"""
RHISA Healthcare Chatbot with GraphRAG
Main application integrating agentic GraphRAG with AWS services
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from datetime import datetime
import os

from graphrag.graphrag_engine import GraphRAGEngine
from graphrag.data_ingestion import DataIngestionPipeline
from config.settings import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize GraphRAG Engine
graphrag_engine = None

def initialize_graphrag():
    """Initialize GraphRAG engine"""
    global graphrag_engine
    try:
        logger.info("Initializing GraphRAG Engine...")
        graphrag_engine = GraphRAGEngine()
        graphrag_engine.initialize()
        
        # Optionally ingest initial data
        if os.getenv('INGEST_DATA', 'false').lower() == 'true':
            logger.info("Ingesting initial healthcare data...")
            pipeline = DataIngestionPipeline(graphrag_engine)
            pipeline.ingest_healthcare_knowledge()
        
        logger.info("GraphRAG Engine ready")
    except Exception as e:
        logger.error(f"Failed to initialize GraphRAG: {str(e)}")
        raise

# Initialize GraphRAG on module load (optional - can be lazy loaded)
# Uncomment the line below to initialize immediately on startup
# initialize_graphrag()

# Lazy initialization on first request (Flask 3.0+ compatible)
@app.before_request
def ensure_graphrag_initialized():
    """Ensure GraphRAG is initialized before handling requests"""
    global graphrag_engine
    if graphrag_engine is None:
        initialize_graphrag()

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
        'version': '2.0.0',
        'service': 'RHISA Healthcare Chatbot with GraphRAG',
        'graphrag_initialized': graphrag_engine is not None
    })

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    """Main chat endpoint with GraphRAG"""
    try:
        if not graphrag_engine:
            return jsonify({'error': 'GraphRAG engine not initialized'}), 503
        
        data = request.get_json()
        user_message = data.get('message', '')
        region = data.get('region', 'gujarat')
        language = data.get('language', 'en')
        domain = data.get('domain', 'eye_health')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process query through GraphRAG
        result = graphrag_engine.query(
            query=user_message,
            region=region,
            language=language,
            domain=domain
        )
        
        if result.get('success'):
            return jsonify({
                'response': result.get('response', ''),
                'context': result.get('context', {}),
                'plan': result.get('plan', {}),
                'region': region,
                'language': language,
                'timestamp': datetime.utcnow().isoformat(),
                'graphrag_enabled': True
            })
        else:
            return jsonify({
                'error': result.get('error', 'Unknown error'),
                'response': result.get('response', 'I apologize, but I encountered an error.')
            }), 500
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/graphrag/query', methods=['POST'])
def graphrag_query():
    """Direct GraphRAG query endpoint"""
    try:
        if not graphrag_engine:
            return jsonify({'error': 'GraphRAG engine not initialized'}), 503
        
        data = request.get_json()
        query = data.get('query', '')
        region = data.get('region', 'gujarat')
        language = data.get('language', 'en')
        domain = data.get('domain', 'eye_health')
        
        result = graphrag_engine.query(query, region, language, domain)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in GraphRAG query: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/graphrag/index', methods=['POST'])
def index_document():
    """Index a new document in GraphRAG"""
    try:
        if not graphrag_engine:
            return jsonify({'error': 'GraphRAG engine not initialized'}), 503
        
        data = request.get_json()
        doc_id = data.get('doc_id')
        content = data.get('content')
        metadata = data.get('metadata', {})
        
        if not doc_id or not content:
            return jsonify({'error': 'doc_id and content are required'}), 400
        
        success = graphrag_engine.index_document(doc_id, content, metadata)
        
        return jsonify({
            'success': success,
            'doc_id': doc_id,
            'message': 'Document indexed successfully' if success else 'Failed to index document'
        })
        
    except Exception as e:
        logger.error(f"Error indexing document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/graphrag/entity', methods=['POST'])
def add_entity():
    """Add entity to knowledge graph"""
    try:
        if not graphrag_engine:
            return jsonify({'error': 'GraphRAG engine not initialized'}), 503
        
        data = request.get_json()
        entity_type = data.get('entity_type')
        entity_id = data.get('entity_id')
        properties = data.get('properties', {})
        
        if not entity_type or not entity_id:
            return jsonify({'error': 'entity_type and entity_id are required'}), 400
        
        success = graphrag_engine.add_graph_entity(entity_type, entity_id, properties)
        
        return jsonify({
            'success': success,
            'entity_id': entity_id,
            'message': 'Entity added successfully' if success else 'Failed to add entity'
        })
        
    except Exception as e:
        logger.error(f"Error adding entity: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/graphrag/relationship', methods=['POST'])
def add_relationship():
    """Add relationship to knowledge graph"""
    try:
        if not graphrag_engine:
            return jsonify({'error': 'GraphRAG engine not initialized'}), 503
        
        data = request.get_json()
        from_id = data.get('from_id')
        to_id = data.get('to_id')
        relationship_type = data.get('relationship_type')
        properties = data.get('properties', {})
        
        if not from_id or not to_id or not relationship_type:
            return jsonify({'error': 'from_id, to_id, and relationship_type are required'}), 400
        
        success = graphrag_engine.add_graph_relationship(
            from_id, to_id, relationship_type, properties
        )
        
        return jsonify({
            'success': success,
            'message': 'Relationship added successfully' if success else 'Failed to add relationship'
        })
        
    except Exception as e:
        logger.error(f"Error adding relationship: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def shutdown_graphrag(exception=None):
    """Shutdown GraphRAG engine"""
    global graphrag_engine
    if graphrag_engine:
        graphrag_engine.shutdown()

if __name__ == '__main__':
    # Initialize GraphRAG before starting server
    logger.info("Starting RHISA Healthcare Chatbot with GraphRAG...")
    
    # Optional: Initialize immediately instead of lazy loading
    if os.getenv('INIT_ON_STARTUP', 'true').lower() == 'true':
        initialize_graphrag()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
