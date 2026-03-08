"""
Configuration for GraphRAG AWS services
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AWSConfig:
    """AWS service configuration"""
    region: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # Neptune Configuration
    neptune_endpoint: str = os.getenv('NEPTUNE_ENDPOINT', '')
    neptune_port: int = int(os.getenv('NEPTUNE_PORT', '8182'))
    
    # OpenSearch Configuration
    opensearch_endpoint: str = os.getenv('OPENSEARCH_ENDPOINT', '')
    opensearch_index: str = os.getenv('OPENSEARCH_INDEX', 'healthcare-knowledge')
    
    # Bedrock Configuration
    bedrock_region: str = os.getenv('BEDROCK_REGION', 'us-east-1')
    bedrock_model_id: str = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    bedrock_embedding_model: str = os.getenv('BEDROCK_EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
    
    # S3 Configuration
    s3_bucket: str = os.getenv('S3_BUCKET', 'rhisa-healthcare-data')
    s3_prefix: str = os.getenv('S3_PREFIX', 'knowledge-base/')
    
    # Lambda Configuration
    lambda_timeout: int = int(os.getenv('LAMBDA_TIMEOUT', '300'))
    lambda_memory: int = int(os.getenv('LAMBDA_MEMORY', '1024'))
    
    # API Gateway Configuration
    api_gateway_stage: str = os.getenv('API_GATEWAY_STAGE', 'prod')
    
    # CloudWatch Configuration
    log_group: str = os.getenv('LOG_GROUP', '/aws/lambda/rhisa-graphrag')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')

@dataclass
class GraphRAGConfig:
    """GraphRAG specific configuration"""
    
    # Retrieval settings
    max_graph_hops: int = 3
    max_vector_results: int = 10
    similarity_threshold: float = 0.7
    rerank_top_k: int = 5
    
    # Agent settings
    max_agent_iterations: int = 5
    agent_timeout: int = 60
    enable_reflection: bool = True
    
    # Graph settings
    graph_traversal_depth: int = 2
    max_graph_nodes: int = 50
    
    # Generation settings
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.9
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    # Regional settings
    supported_regions: list = None
    supported_languages: list = None
    
    def __post_init__(self):
        if self.supported_regions is None:
            self.supported_regions = ['gujarat', 'maharashtra']
        if self.supported_languages is None:
            self.supported_languages = ['en', 'gu', 'mr']

# Global configuration instances
aws_config = AWSConfig()
graphrag_config = GraphRAGConfig()
