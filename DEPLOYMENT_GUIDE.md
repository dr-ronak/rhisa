# RHISA GraphRAG Deployment Guide

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI configured
3. Python 3.9 or higher
4. Docker (for Lambda deployment)
5. Terraform or CloudFormation knowledge (optional)

## Step 1: AWS Infrastructure Setup

### Option A: Using CloudFormation

```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name rhisa-graphrag-infrastructure \
  --template-body file://infrastructure/cloudformation_template.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=production \
  --capabilities CAPABILITY_IAM

# Wait for stack creation
aws cloudformation wait stack-create-complete \
  --stack-name rhisa-graphrag-infrastructure

# Get outputs
aws cloudformation describe-stacks \
  --stack-name rhisa-graphrag-infrastructure \
  --query 'Stacks[0].Outputs'
```

### Option B: Manual Setup

#### 1. Create Neptune Cluster

```bash
# Create Neptune cluster
aws neptune create-db-cluster \
  --db-cluster-identifier rhisa-neptune-cluster \
  --engine neptune \
  --engine-version 1.2.1.0 \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name your-subnet-group

# Create Neptune instance
aws neptune create-db-instance \
  --db-instance-identifier rhisa-neptune-instance \
  --db-instance-class db.r5.large \
  --engine neptune \
  --db-cluster-identifier rhisa-neptune-cluster
```

#### 2. Create OpenSearch Domain

```bash
aws opensearch create-domain \
  --domain-name rhisa-opensearch \
  --engine-version OpenSearch_2.11 \
  --cluster-config InstanceType=r6g.large.search,InstanceCount=2 \
  --ebs-options EBSEnabled=true,VolumeType=gp3,VolumeSize=100 \
  --access-policies file://opensearch-access-policy.json
```

#### 3. Create S3 Bucket

```bash
aws s3 mb s3://rhisa-healthcare-data
aws s3api put-bucket-encryption \
  --bucket rhisa-healthcare-data \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

#### 4. Enable Bedrock Access

```bash
# Request model access in AWS Console
# Navigate to: Bedrock > Model access
# Request access to:
# - Claude 3 Sonnet
# - Titan Embeddings v2
```

## Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your AWS resource endpoints
nano .env
```

Update the following values:
- `NEPTUNE_ENDPOINT`: From Neptune cluster endpoint
- `OPENSEARCH_ENDPOINT`: From OpenSearch domain endpoint
- `S3_BUCKET`: Your S3 bucket name
- AWS credentials (or use IAM roles)

## Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements_graphrag.txt
```

## Step 4: Initialize GraphRAG System

```bash
# Set environment variable to ingest initial data
export INGEST_DATA=true

# Run initialization script
python -c "
from graphrag.graphrag_engine import GraphRAGEngine
from graphrag.data_ingestion import DataIngestionPipeline

with GraphRAGEngine() as engine:
    pipeline = DataIngestionPipeline(engine)
    pipeline.ingest_healthcare_knowledge()
    print('GraphRAG system initialized successfully')
"
```

## Step 5: Local Testing

```bash
# Run Flask application locally
python app_graphrag.py

# Test health endpoint
curl http://localhost:5000/api/v1/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of cataract?",
    "region": "gujarat",
    "language": "en"
  }'
```

## Step 6: Lambda Deployment

### Create Lambda Deployment Package

```bash
# Create deployment directory
mkdir lambda_deployment
cd lambda_deployment

# Copy application files
cp -r ../graphrag .
cp -r ../config .
cp ../app_graphrag.py lambda_function.py

# Install dependencies
pip install -r ../requirements_graphrag.txt -t .

# Create deployment package
zip -r ../rhisa-graphrag-lambda.zip .
cd ..
```

### Deploy to Lambda

```bash
# Create Lambda function
aws lambda create-function \
  --function-name rhisa-graphrag-api \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://rhisa-graphrag-lambda.zip \
  --timeout 300 \
  --memory-size 1024 \
  --environment Variables="{
    NEPTUNE_ENDPOINT=your-endpoint,
    OPENSEARCH_ENDPOINT=your-endpoint,
    BEDROCK_REGION=us-east-1
  }"

# Update function code (for updates)
aws lambda update-function-code \
  --function-name rhisa-graphrag-api \
  --zip-file fileb://rhisa-graphrag-lambda.zip
```

## Step 7: API Gateway Setup

```bash
# Create API Gateway
aws apigatewayv2 create-api \
  --name rhisa-graphrag-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:REGION:ACCOUNT:function:rhisa-graphrag-api

# Get API endpoint
aws apigatewayv2 get-apis \
  --query 'Items[?Name==`rhisa-graphrag-api`].ApiEndpoint' \
  --output text
```

## Step 8: Monitoring Setup

### CloudWatch Dashboards

```bash
# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name rhisa-graphrag-monitoring \
  --dashboard-body file://infrastructure/cloudwatch-dashboard.json
```

### Set up Alarms

```bash
# Lambda error alarm
aws cloudwatch put-metric-alarm \
  --alarm-name rhisa-lambda-errors \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

## Step 9: Security Hardening

1. Enable VPC endpoints for AWS services
2. Configure WAF rules for API Gateway
3. Enable CloudTrail logging
4. Set up AWS Secrets Manager for credentials
5. Configure IAM least privilege policies

## Step 10: Performance Optimization

### Neptune Optimization

```bash
# Create Neptune read replicas
aws neptune create-db-instance \
  --db-instance-identifier rhisa-neptune-replica-1 \
  --db-instance-class db.r5.large \
  --engine neptune \
  --db-cluster-identifier rhisa-neptune-cluster
```

### OpenSearch Optimization

- Enable UltraWarm for cost optimization
- Configure index lifecycle policies
- Set up cross-cluster replication for DR

### Lambda Optimization

- Use Lambda layers for dependencies
- Enable Lambda provisioned concurrency
- Configure Lambda reserved concurrency

## Troubleshooting

### Neptune Connection Issues

```bash
# Test Neptune connectivity
aws neptune describe-db-clusters \
  --db-cluster-identifier rhisa-neptune-cluster

# Check security groups
aws ec2 describe-security-groups \
  --group-ids sg-xxxxx
```

### OpenSearch Issues

```bash
# Check domain status
aws opensearch describe-domain \
  --domain-name rhisa-opensearch

# View cluster health
curl -XGET https://your-opensearch-endpoint/_cluster/health
```

### Bedrock Access Issues

```bash
# List available models
aws bedrock list-foundation-models \
  --region us-east-1

# Test model invocation
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-sonnet-20240229-v1:0 \
  --body '{"prompt":"Hello","max_tokens":100}' \
  output.json
```

## Cost Estimation

### Monthly Costs (Approximate)

- Neptune (db.r5.large): $500-700
- OpenSearch (r6g.large x2): $400-600
- Bedrock (Claude 3): $50-200 (usage-based)
- Lambda: $20-50 (usage-based)
- S3: $10-30
- Data Transfer: $20-50

**Total: ~$1,000-1,630/month**

## Scaling Considerations

1. Neptune: Add read replicas for read-heavy workloads
2. OpenSearch: Increase instance count and enable UltraWarm
3. Lambda: Use provisioned concurrency for consistent performance
4. API Gateway: Enable caching to reduce backend calls
5. CloudFront: Add CDN for global distribution

## Backup and Disaster Recovery

```bash
# Enable automated Neptune backups
aws neptune modify-db-cluster \
  --db-cluster-identifier rhisa-neptune-cluster \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00"

# Create manual snapshot
aws neptune create-db-cluster-snapshot \
  --db-cluster-identifier rhisa-neptune-cluster \
  --db-cluster-snapshot-identifier rhisa-snapshot-$(date +%Y%m%d)

# Enable OpenSearch automated snapshots
aws opensearch update-domain-config \
  --domain-name rhisa-opensearch \
  --snapshot-options AutomatedSnapshotStartHour=3
```

## Next Steps

1. Set up CI/CD pipeline
2. Implement comprehensive testing
3. Configure multi-region deployment
4. Set up monitoring and alerting
5. Implement rate limiting and throttling
6. Add authentication and authorization
7. Create API documentation
8. Set up load testing
