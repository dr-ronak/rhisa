"""
RHISA Healthcare Chatbot - Demo Version
Runs without AWS resources for testing and development
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Mock GraphRAG responses for demo
class MockGraphRAGEngine:
    """Mock GraphRAG engine for demo purposes"""
    
    def __init__(self):
        self.initialized = True
        logger.info("Mock GraphRAG Engine initialized")
    
    def query(self, query, region='gujarat', language='en', domain='eye_health'):
        """Mock query processing"""
        
        # Simple keyword-based responses
        query_lower = query.lower()
        
        if 'cataract' in query_lower:
            response = self._get_cataract_response(region, language)
        elif 'glaucoma' in query_lower:
            response = self._get_glaucoma_response(region, language)
        elif 'symptom' in query_lower or 'blurred' in query_lower:
            response = self._get_symptom_response(region, language)
        elif 'treatment' in query_lower:
            response = self._get_treatment_response(region, language)
        else:
            response = self._get_general_response(region, language)
        
        return {
            'success': True,
            'response': response,
            'context': {
                'graph_results': ['Mock graph data'],
                'vector_results': ['Mock vector search results']
            },
            'plan': {
                'agents': ['vector_search', 'graph_query'],
                'reasoning': 'Demo mode - using mock responses'
            }
        }
    
    def _get_cataract_response(self, region, language):
        responses = {
            'en': f"""**Understanding Cataract**

Cataract is a common eye condition where the lens becomes cloudy, affecting vision. In {region.title()}, it's one of the leading causes of vision impairment.

**Common Symptoms:**
- Blurred or cloudy vision
- Difficulty seeing at night
- Sensitivity to light and glare
- Seeing halos around lights
- Fading or yellowing of colors

**Treatment Options:**
- Early stages: Updated eyeglass prescription
- Advanced stages: Cataract surgery (highly successful with 95%+ success rate)

**Regional Resources in {region.title()}:**
- Free eye screening at Primary Health Centers
- Government-supported cataract surgery programs
- Emergency services: 108

*Note: This is a demo response. Please consult with a qualified healthcare professional for medical advice.*
""",
            'gu': f"""**મોતિયા વિશે સમજો**

મોતિયા એ એક સામાન્ય આંખની સ્થિતિ છે જ્યાં લેન્સ વાદળછાયું બને છે. {region.title()}માં, આ દ્રષ્ટિ ક્ષતિનું મુખ્ય કારણ છે.

**સામાન્ય લક્ષણો:**
- અસ્પષ્ટ અથવા વાદળછાયું દ્રષ્ટિ
- રાત્રે જોવામાં મુશ્કેલી
- પ્રકાશ પ્રત્યે સંવેદનશીલતા

**સારવાર:**
- પ્રારંભિક તબક્કા: ચશ્માં બદલવા
- અદ્યતન તબક્કા: મોતિયાની શસ્ત્રક્રિયા

*નોંધ: આ ડેમો પ્રતિસાદ છે. તબીબી સલાહ માટે કૃપા કરીને લાયક આરોગ્ય વ્યાવસાયિકની સલાહ લો.*
""",
            'mr': f"""**मोतीबिंदू समजून घ्या**

मोतीबिंदू ही एक सामान्य डोळ्यांची स्थिती आहे जिथे लेन्स ढगाळ होते. {region.title()}मध्ये, हे दृष्टी कमजोरीचे प्रमुख कारण आहे.

**सामान्य लक्षणे:**
- अस्पष्ट किंवा ढगाळ दृष्टी
- रात्री पाहण्यात अडचण
- प्रकाशाची संवेदनशीलता

**उपचार:**
- सुरुवातीच्या टप्प्यात: चष्मा बदलणे
- प्रगत टप्प्यात: मोतीबिंदू शस्त्रक्रिया

*टीप: हा डेमो प्रतिसाद आहे. वैद्यकीय सल्ल्यासाठी कृपया पात्र आरोग्य व्यावसायिकांचा सल्ला घ्या.*
"""
        }
        return responses.get(language, responses['en'])
    
    def _get_glaucoma_response(self, region, language):
        return f"""**Glaucoma Information**

Glaucoma is a group of eye conditions that damage the optic nerve, often due to high eye pressure.

**Risk Factors:**
- Age over 60
- Family history
- Diabetes
- High blood pressure

**Prevention & Management:**
- Regular eye exams (annual for high-risk individuals)
- Early detection is crucial
- Treatment includes eye drops, laser therapy, or surgery

**{region.title()} Resources:**
- Free glaucoma screening at government health centers
- Specialized eye care facilities available

*Demo response - consult healthcare professionals for actual medical advice.*
"""
    
    def _get_symptom_response(self, region, language):
        return f"""**Common Eye Symptoms**

If you're experiencing eye symptoms, here's what you should know:

**Blurred Vision:**
- Can indicate refractive errors, cataracts, or other conditions
- Requires eye examination

**Eye Pain:**
- May indicate infection, glaucoma, or injury
- Seek immediate medical attention if severe

**Light Sensitivity:**
- Common with various eye conditions
- Protect eyes with sunglasses

**When to Seek Help:**
- Sudden vision changes
- Severe eye pain
- Injury to the eye
- Persistent symptoms

**Emergency Contact:** 108

*Demo response - this is not a substitute for professional medical diagnosis.*
"""
    
    def _get_treatment_response(self, region, language):
        return f"""**Treatment Options in {region.title()}**

Healthcare facilities in {region.title()} offer various treatment options:

**Primary Health Centers:**
- Basic eye examinations
- Prescription services
- Referrals to specialists

**District Hospitals:**
- Advanced diagnostics
- Surgical facilities
- Specialist consultations

**Government Programs:**
- Free cataract surgery
- Diabetic retinopathy screening
- Vision screening camps

**Private Healthcare:**
- Specialized eye hospitals
- Advanced treatment options

*Demo response - contact local health department for specific information.*
"""
    
    def _get_general_response(self, region, language):
        return f"""**RHISA Healthcare Assistant**

Hello! I'm RHISA, your Regional Health Insight & Support Agent for {region.title()}.

I can help you with:
- Eye health information (cataracts, glaucoma, diabetic retinopathy)
- Skin health guidance
- Treatment options and guidelines
- Regional healthcare resources
- Patient education

**Note:** This is a demo version running without AWS resources. For full functionality with GraphRAG, please configure AWS services (Neptune, OpenSearch, Bedrock).

How can I assist you with your healthcare questions today?

*Demo mode - responses are simplified examples.*
"""
    
    def shutdown(self):
        """Mock shutdown"""
        logger.info("Mock GraphRAG Engine shutdown")

# Initialize mock engine
graphrag_engine = MockGraphRAGEngine()

@app.route('/')
def index():
    """Main chatbot interface"""
    return """
    <html>
    <head>
        <title>RHISA Healthcare Chatbot - Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2196F3; }
            .demo-notice { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 3px; }
            code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🏥 RHISA Healthcare Chatbot - Demo Mode</h1>
        
        <div class="demo-notice">
            <strong>⚠️ Demo Mode:</strong> This version runs without AWS resources for testing.
            Responses are mock examples. For full GraphRAG functionality, configure AWS services.
        </div>
        
        <h2>API Endpoints</h2>
        
        <div class="endpoint">
            <strong>Health Check:</strong><br>
            <code>GET /api/v1/health</code>
        </div>
        
        <div class="endpoint">
            <strong>Chat:</strong><br>
            <code>POST /api/v1/chat</code><br>
            Body: <code>{"message": "What are symptoms of cataract?", "region": "gujarat", "language": "en"}</code>
        </div>
        
        <h2>Example cURL Commands</h2>
        
        <div class="endpoint">
            <pre>curl http://localhost:5000/api/v1/health</pre>
        </div>
        
        <div class="endpoint">
            <pre>curl -X POST http://localhost:5000/api/v1/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What are symptoms of cataract?", "region": "gujarat", "language": "en"}'</pre>
        </div>
        
        <p><strong>Supported Regions:</strong> gujarat, maharashtra</p>
        <p><strong>Supported Languages:</strong> en (English), gu (Gujarati), mr (Marathi)</p>
    </body>
    </html>
    """

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0-demo',
        'service': 'RHISA Healthcare Chatbot (Demo Mode)',
        'graphrag_initialized': True,
        'mode': 'demo',
        'note': 'Running with mock responses - configure AWS for full functionality'
    })

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        region = data.get('region', 'gujarat')
        language = data.get('language', 'en')
        domain = data.get('domain', 'eye_health')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process query through mock GraphRAG
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
                'mode': 'demo',
                'graphrag_enabled': True
            })
        else:
            return jsonify({
                'error': result.get('error', 'Unknown error'),
                'response': 'I apologize, but I encountered an error.'
            }), 500
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.teardown_appcontext
def shutdown_graphrag(exception=None):
    """Shutdown GraphRAG engine"""
    if graphrag_engine:
        graphrag_engine.shutdown()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    logger.info("=" * 60)
    logger.info("RHISA Healthcare Chatbot - Demo Mode")
    logger.info("=" * 60)
    logger.info("Running without AWS resources")
    logger.info("For full GraphRAG functionality, use app_graphrag.py")
    logger.info(f"Server starting on http://localhost:{port}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
