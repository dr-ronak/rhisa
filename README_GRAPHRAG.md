# RHISA Healthcare Chatbot with Agentic GraphRAG

## Overview

RHISA (Regional Health Insight & Support Agent) is an advanced healthcare chatbot powered by Agentic GraphRAG (Graph Retrieval-Augmented Generation) using AWS technology stack. The system combines knowledge graphs, vector search, and multi-agent AI to provide accurate, contextual healthcare information for Gujarat and Maharashtra regions in India.

## Architecture

### Core Components

1. **Amazon Neptune** - Graph database storing medical knowledge graph
   - Medical entities (conditions, symptoms, treatments, medications)
   - Relationships and treatment pathways
   - Regional healthcare guidelines

2. **Amazon OpenSearch** - Vector store for semantic search
   - Document embeddings using Titan
   - Hybrid search (keyword + semantic)
   - Multi-language support

3. **Amazon Bedrock** - Foundation models
   - Claude 3 Sonnet for conversational AI
   - Titan Embeddings v2 for vector generation
   - Tool calling and agent orchestration

4. **Multi-Agent System**
   - **Orchestrator Agent**: Coordinates all agents and plans execution
   - **Graph Query Agent**: Queries Neptune knowledge graph
   - **Vector Search Agent**: Performs semantic search in OpenSearch
   - **Knowledge Agent**: Provides patient education
   - **Trend Analyzer**: Analyzes regional health patterns
   - **Compliance Checker**: Validates against guidelines

### GraphRAG Workflow

```
User Query
    ↓
Orchestrator Agent (Plans execution)
    ↓
    ├─→ Graph Query Agent → Neptune (Relationships, pathways)
    ├─→ Vector Search Agent → OpenSearch (Semantic search)
    └─→ Context Aggregation
         ↓
    Bedrock Claude 3 (Response generation)
         ↓
    Specialized Agents (Compliance, Trends)
         ↓
    Final Response
```

## Features

### Agentic Capabilities

- **Autonomous Planning**: LLM-based query analysis and execution planning
- **Multi-Hop Reasoning**: Graph traversal for complex medical queries
- **Tool Selection**: Dynamic agent and tool selection
- **Self-Reflection**: Error detection and retry mechanisms
- **Context Aggregation**: Combines graph and vector search results

### Healthcare Features

- **Multilingual Support**: English, Gujarati, Marathi
- **Regional Intelligence**: Gujarat and Maharashtra specific data
- **Medical Domains**: Eye health and skin conditions
- **Treatment Pathways**: Graph-based treatment recommendations
- **Compliance Checking**: Regional guideline validation
- **Trend Analysis**: Health pattern analysis

## Installation

### Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- AWS CLI configured
- Docker (for Lambda deployment)

### Local Setup

```bash
# Clone repository
git clone <repository-url>
cd rhisa-healthcare-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_graphrag.txt

# Configure environment
cp .env.example .env
# Edit .env with your AWS credentials and endpoints

# Initialize GraphRAG system
export INGEST_DATA=true
python app_graphrag.py
```

## Usage

### API Endpoints

#### 1. Health Check
```bash
GET /api/v1/health
```

#### 2. Chat with GraphRAG
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "message": "What are the symptoms of cataract?",
  "region": "gujarat",
  "language": "en",
  "domain": "eye_health"
}
```

#### 3. Direct GraphRAG Query
```bash
POST /api/v1/graphrag/query
Content-Type: application/json

{
  "query": "Treatment pathway for glaucoma",
  "region": "gujarat",
  "language": "en",
  "domain": "eye_health"
}
```

#### 4. Index Document
```bash
POST /api/v1/graphrag/index
Content-Type: application/json

{
  "doc_id": "doc_001",
  "content": "Healthcare document content...",
  "metadata": {
    "region": "gujarat",
    "domain": "eye_health",
    "title": "Document Title"
  }
}
```

#### 5. Add Graph Entity
```bash
POST /api/v1/graphrag/entity
Content-Type: application/json

{
  "entity_type": "condition",
  "entity_id": "cond_001",
  "properties": {
    "name": "cataract",
    "region": "gujarat",
    "domain": "eye_health"
  }
}
```

#### 6. Add Graph Relationship
```bash
POST /api/v1/graphrag/relationship
Content-Type: application/json

{
  "from_id": "cond_001",
  "to_id": "symp_001",
  "relationship_type": "has_symptom",
  "properties": {
    "frequency": "common"
  }
}
```

### Python SDK Usage

```python
from graphrag.graphrag_engine import GraphRAGEngine

# Initialize engine
with GraphRAGEngine() as engine:
    # Query the system
    result = engine.query(
        query="What are the symptoms of cataract?",
        region="gujarat",
        language="en",
        domain="eye_health"
    )
    
    print(result['response'])
    
    # Add new entity
    engine.add_graph_entity(
        entity_type="condition",
        entity_id="cond_new",
        properties={"name": "glaucoma", "region": "gujarat"}
    )
    
    # Index document
    engine.index_document(
        doc_id="doc_new",
        content="Healthcare information...",
        metadata={"region": "gujarat", "domain": "eye_health"}
    )
```

## Configuration

### Environment Variables

See `.env.example` for all configuration options.

Key configurations:
- `NEPTUNE_ENDPOINT`: Neptune cluster endpoint
- `OPENSEARCH_ENDPOINT`: OpenSearch domain endpoint
- `BEDROCK_MODEL_ID`: Claude 3 model ID
- `BEDROCK_EMBEDDING_MODEL`: Titan embeddings model ID

### GraphRAG Configuration

Edit `graphrag/config.py`:

```python
@dataclass
class GraphRAGConfig:
    max_graph_hops: int = 3
    max_vector_results: int = 10
    similarity_threshold: float = 0.7
    rerank_top_k: int = 5
    max_agent_iterations: int = 5
    temperature: float = 0.7
    max_tokens: int = 2000
```

## Deployment

### AWS Lambda Deployment

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

Quick deployment:

```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name rhisa-graphrag \
  --template-body file://infrastructure/cloudformation_template.yaml \
  --capabilities CAPABILITY_IAM

# Package and deploy Lambda
./scripts/deploy_lambda.sh
```

### Docker Deployment

```bash
# Build Docker image
docker build -t rhisa-graphrag .

# Run container
docker run -p 5000:5000 \
  -e NEPTUNE_ENDPOINT=your-endpoint \
  -e OPENSEARCH_ENDPOINT=your-endpoint \
  rhisa-graphrag
```

## Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=graphrag tests/
```

## Project Structure

```
rhisa-healthcare-chatbot/
├── graphrag/                    # GraphRAG core module
│   ├── agents/                  # Multi-agent system
│   │   ├── base_agent.py
│   │   ├── orchestrator_agent.py
│   │   ├── graph_query_agent.py
│   │   └── vector_search_agent.py
│   ├── bedrock_client.py        # Bedrock LLM client
│   ├── graph_store.py           # Neptune interface
│   ├── vector_store.py          # OpenSearch interface
│   ├── graphrag_engine.py       # Main engine
│   ├── data_ingestion.py        # Data pipeline
│   └── config.py                # Configuration
├── infrastructure/              # AWS infrastructure
│   └── cloudformation_template.yaml
├── app_graphrag.py             # Flask application
├── requirements_graphrag.txt   # Dependencies
├── .env.example                # Environment template
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
└── README_GRAPHRAG.md          # This file
```

## Performance

### Benchmarks

- Query latency: 2-5 seconds (including LLM generation)
- Graph traversal: <500ms for 3-hop queries
- Vector search: <200ms for top-10 results
- Concurrent requests: 100+ req/s with Lambda

### Optimization Tips

1. **Caching**: Enable Redis for frequently accessed data
2. **Neptune**: Use read replicas for read-heavy workloads
3. **OpenSearch**: Configure index lifecycle policies
4. **Lambda**: Use provisioned concurrency for consistent performance
5. **Bedrock**: Batch embedding generation when possible

## Cost Estimation

Monthly costs (approximate):
- Neptune (db.r5.large): $500-700
- OpenSearch (r6g.large x2): $400-600
- Bedrock (usage-based): $50-200
- Lambda: $20-50
- S3 + Data Transfer: $30-80

**Total: ~$1,000-1,630/month**

## Security

- VPC isolation for Neptune and OpenSearch
- IAM roles for service authentication
- Encryption at rest and in transit
- AWS WAF for API protection
- CloudTrail for audit logging
- Secrets Manager for credential management

## Monitoring

- CloudWatch metrics and logs
- Custom dashboards for GraphRAG metrics
- Alarms for errors and latency
- X-Ray tracing for request flow
- Neptune and OpenSearch monitoring

## Troubleshooting

### Common Issues

1. **Neptune Connection Timeout**
   - Check security groups
   - Verify VPC configuration
   - Ensure Lambda is in same VPC

2. **OpenSearch Access Denied**
   - Verify IAM policies
   - Check access policies on domain
   - Ensure correct authentication

3. **Bedrock Model Access**
   - Request model access in console
   - Verify region availability
   - Check IAM permissions

4. **High Latency**
   - Enable caching
   - Optimize graph queries
   - Use provisioned concurrency
   - Add read replicas

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: Report bugs and feature requests
- Documentation: See `/docs` folder
- AWS Support: For infrastructure issues

## Acknowledgments

- Built with AWS Bedrock, Neptune, and OpenSearch
- Powered by Claude 3 and Titan models
- Designed for Gujarat and Maharashtra healthcare systems
- Privacy-first with synthetic data

## Roadmap

- [ ] Multi-region deployment
- [ ] Real-time streaming responses
- [ ] Voice interface integration
- [ ] Mobile app support
- [ ] Advanced analytics dashboard
- [ ] Integration with EHR systems
- [ ] Telemedicine features
- [ ] Prescription management
