# RHISA GraphRAG Quick Start Guide

## 5-Minute Setup (Local Development)

### Step 1: Install Dependencies

```bash
# Clone and navigate to project
cd rhisa-healthcare-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements_graphrag.txt
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your AWS credentials
# Minimum required:
# - AWS_REGION
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - BEDROCK_REGION
```

### Step 3: Test Installation

```bash
# Run test script
python test_graphrag.py
```

Expected output:
```
✓ All imports successful
✓ Configuration loaded successfully
✓ Bedrock client initialized
...
Results: X/8 tests passed
```

### Step 4: Run Application

#### Option A: Demo Mode (No AWS Required)

```bash
# Start demo server with mock responses
python app_demo.py
```

This runs a demo version with mock responses - perfect for testing the API structure without AWS resources.

#### Option B: Full GraphRAG Mode (Requires AWS)

```bash
# Start full GraphRAG server
python app_graphrag.py
```

This requires AWS services (Neptune, OpenSearch, Bedrock) to be configured.

Visit: `http://localhost:5000`

## Testing the API

### Health Check

```bash
curl http://localhost:5000/api/v1/health
```

### Chat Query

```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of cataract?",
    "region": "gujarat",
    "language": "en"
  }'
```

## AWS Setup (Production)

### Prerequisites

1. AWS Account with admin access
2. AWS CLI installed and configured
3. Bedrock model access enabled

### Quick Deploy

```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name rhisa-graphrag \
  --template-body file://infrastructure/cloudformation_template.yaml \
  --capabilities CAPABILITY_IAM

# Wait for completion (10-15 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name rhisa-graphrag

# Get endpoints
aws cloudformation describe-stacks \
  --stack-name rhisa-graphrag \
  --query 'Stacks[0].Outputs'
```

### Update Environment

Update `.env` with the CloudFormation outputs:
- `NEPTUNE_ENDPOINT`
- `OPENSEARCH_ENDPOINT`
- `S3_BUCKET`

### Initialize Data

```bash
# Set flag to ingest initial data
export INGEST_DATA=true

# Run application (will ingest data on startup)
python app_graphrag.py
```

## Example Queries

### 1. Medical Condition Query

```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about glaucoma treatment in Gujarat",
    "region": "gujarat",
    "language": "en",
    "domain": "eye_health"
  }'
```

### 2. Symptom Query

```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have blurred vision and eye pain",
    "region": "gujarat",
    "language": "en"
  }'
```

### 3. Regional Guidelines

```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the eye screening guidelines in Maharashtra?",
    "region": "maharashtra",
    "language": "en"
  }'
```

### 4. Multilingual Query

```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "મોતિયાના લક્ષણો શું છે?",
    "region": "gujarat",
    "language": "gu"
  }'
```

## Adding Custom Data

### Add Medical Entity

```bash
curl -X POST http://localhost:5000/api/v1/graphrag/entity \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "condition",
    "entity_id": "cond_custom_001",
    "properties": {
      "name": "myopia",
      "display_name": "Myopia",
      "region": "gujarat",
      "domain": "eye_health",
      "description": "Nearsightedness"
    }
  }'
```

### Add Relationship

```bash
curl -X POST http://localhost:5000/api/v1/graphrag/relationship \
  -H "Content-Type: application/json" \
  -d '{
    "from_id": "cond_custom_001",
    "to_id": "symp_blurred_vision",
    "relationship_type": "has_symptom",
    "properties": {
      "frequency": "common"
    }
  }'
```

### Index Document

```bash
curl -X POST http://localhost:5000/api/v1/graphrag/index \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "doc_custom_001",
    "content": "Myopia is a common refractive error where distant objects appear blurry...",
    "metadata": {
      "region": "gujarat",
      "domain": "eye_health",
      "title": "Understanding Myopia",
      "language": "en"
    }
  }'
```

## Troubleshooting

### Issue: Import Errors

```bash
# Reinstall dependencies
pip install -r requirements_graphrag.txt --force-reinstall
```

### Issue: AWS Connection Errors

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

### Issue: Neptune Connection Timeout

- Ensure Lambda/EC2 is in same VPC as Neptune
- Check security group rules
- Verify Neptune endpoint is correct

### Issue: OpenSearch Access Denied

- Check IAM policies
- Verify access policies on OpenSearch domain
- Ensure correct authentication method

## Next Steps

1. Read `README_GRAPHRAG.md` for detailed documentation
2. See `DEPLOYMENT_GUIDE.md` for production deployment
3. Review `GRAPHRAG_ARCHITECTURE.md` for system design
4. Explore `graphrag/` module for customization

## Support

- GitHub Issues: Report bugs
- Documentation: See `/docs` folder
- AWS Support: For infrastructure issues

## Quick Reference

### Environment Variables

```bash
# Required
AWS_REGION=us-east-1
BEDROCK_REGION=us-east-1

# For full functionality
NEPTUNE_ENDPOINT=your-neptune-endpoint
OPENSEARCH_ENDPOINT=your-opensearch-endpoint
S3_BUCKET=your-s3-bucket
```

### API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/chat` - Chat interface
- `POST /api/v1/graphrag/query` - Direct GraphRAG query
- `POST /api/v1/graphrag/index` - Index document
- `POST /api/v1/graphrag/entity` - Add entity
- `POST /api/v1/graphrag/relationship` - Add relationship

### Supported Regions

- `gujarat` - Gujarat, India
- `maharashtra` - Maharashtra, India

### Supported Languages

- `en` - English
- `gu` - Gujarati (ગુજરાતી)
- `mr` - Marathi (मराठी)

### Healthcare Domains

- `eye_health` - Eye health and vision
- `skin_health` - Skin conditions and dermatology
