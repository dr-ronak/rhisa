"""
Test script for GraphRAG system
"""

import os
import sys
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all modules can be imported"""
    logger.info("Testing imports...")
    try:
        from graphrag.config import aws_config, graphrag_config
        from graphrag.bedrock_client import BedrockClient
        from graphrag.graph_store import NeptuneGraphStore
        from graphrag.vector_store import OpenSearchVectorStore
        from graphrag.agents import OrchestratorAgent, GraphQueryAgent, VectorSearchAgent
        from graphrag.graphrag_engine import GraphRAGEngine
        from graphrag.data_ingestion import DataIngestionPipeline
        
        logger.info("✓ All imports successful")
        return True
    except Exception as e:
        logger.error(f"✗ Import failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading"""
    logger.info("Testing configuration...")
    try:
        from graphrag.config import aws_config, graphrag_config
        
        logger.info(f"AWS Region: {aws_config.region}")
        logger.info(f"Bedrock Model: {aws_config.bedrock_model_id}")
        logger.info(f"Max Graph Hops: {graphrag_config.max_graph_hops}")
        logger.info(f"Temperature: {graphrag_config.temperature}")
        
        logger.info("✓ Configuration loaded successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Configuration test failed: {str(e)}")
        return False

def test_bedrock_client():
    """Test Bedrock client (requires AWS credentials)"""
    logger.info("Testing Bedrock client...")
    try:
        from graphrag.bedrock_client import BedrockClient
        
        client = BedrockClient()
        
        # Test embedding generation
        logger.info("Testing embedding generation...")
        embedding = client.generate_embedding("Test healthcare query")
        
        if embedding and len(embedding) > 0:
            logger.info(f"✓ Generated embedding of dimension: {len(embedding)}")
        else:
            logger.warning("⚠ Embedding generation returned empty result")
        
        # Test response generation
        logger.info("Testing response generation...")
        response = client.generate_response(
            prompt="What is cataract?",
            temperature=0.7,
            max_tokens=100
        )
        
        if response:
            logger.info(f"✓ Generated response: {response[:100]}...")
        else:
            logger.warning("⚠ Response generation returned empty result")
        
        return True
    except Exception as e:
        logger.error(f"✗ Bedrock client test failed: {str(e)}")
        logger.info("Note: This test requires valid AWS credentials and Bedrock access")
        return False

def test_graph_store():
    """Test Neptune graph store (requires Neptune endpoint)"""
    logger.info("Testing Neptune graph store...")
    try:
        from graphrag.graph_store import NeptuneGraphStore
        
        store = NeptuneGraphStore()
        logger.info(f"Neptune endpoint: {store.endpoint}")
        
        # Note: Actual connection test requires valid Neptune endpoint
        logger.info("⚠ Skipping connection test (requires valid Neptune endpoint)")
        logger.info("✓ Graph store initialized")
        return True
    except Exception as e:
        logger.error(f"✗ Graph store test failed: {str(e)}")
        return False

def test_vector_store():
    """Test OpenSearch vector store (requires OpenSearch endpoint)"""
    logger.info("Testing OpenSearch vector store...")
    try:
        from graphrag.vector_store import OpenSearchVectorStore
        
        store = OpenSearchVectorStore()
        logger.info(f"OpenSearch endpoint: {store.endpoint}")
        logger.info(f"Index name: {store.index_name}")
        
        # Note: Actual connection test requires valid OpenSearch endpoint
        logger.info("⚠ Skipping connection test (requires valid OpenSearch endpoint)")
        logger.info("✓ Vector store initialized")
        return True
    except Exception as e:
        logger.error(f"✗ Vector store test failed: {str(e)}")
        return False

def test_agents():
    """Test agent initialization"""
    logger.info("Testing agents...")
    try:
        from graphrag.agents import BaseAgent, GraphQueryAgent, VectorSearchAgent
        from graphrag.graph_store import NeptuneGraphStore
        from graphrag.vector_store import OpenSearchVectorStore
        from graphrag.bedrock_client import BedrockClient
        
        # Test base agent
        class TestAgent(BaseAgent):
            def execute(self, task):
                return {'success': True, 'message': 'Test execution'}
        
        test_agent = TestAgent("TestAgent", "Test agent description")
        logger.info(f"✓ Base agent created: {test_agent.name}")
        
        # Test tool addition
        test_agent.add_tool({
            'name': 'test_tool',
            'description': 'Test tool',
            'input_schema': {'type': 'object'}
        })
        logger.info(f"✓ Tool added, total tools: {len(test_agent.tools)}")
        
        logger.info("✓ Agents tested successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Agent test failed: {str(e)}")
        return False

def test_graphrag_engine():
    """Test GraphRAG engine initialization"""
    logger.info("Testing GraphRAG engine...")
    try:
        from graphrag.graphrag_engine import GraphRAGEngine
        
        engine = GraphRAGEngine()
        logger.info("✓ GraphRAG engine created")
        
        # Note: Full initialization requires AWS resources
        logger.info("⚠ Skipping full initialization (requires AWS resources)")
        
        return True
    except Exception as e:
        logger.error(f"✗ GraphRAG engine test failed: {str(e)}")
        return False

def test_data_ingestion():
    """Test data ingestion pipeline"""
    logger.info("Testing data ingestion pipeline...")
    try:
        from graphrag.data_ingestion import DataIngestionPipeline
        from graphrag.graphrag_engine import GraphRAGEngine
        
        engine = GraphRAGEngine()
        pipeline = DataIngestionPipeline(engine)
        
        logger.info("✓ Data ingestion pipeline created")
        logger.info("⚠ Skipping actual ingestion (requires AWS resources)")
        
        return True
    except Exception as e:
        logger.error(f"✗ Data ingestion test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("RHISA GraphRAG System Tests")
    logger.info("=" * 60)
    logger.info(f"Start time: {datetime.now().isoformat()}")
    logger.info("")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Bedrock Client", test_bedrock_client),
        ("Graph Store", test_graph_store),
        ("Vector Store", test_vector_store),
        ("Agents", test_agents),
        ("GraphRAG Engine", test_graphrag_engine),
        ("Data Ingestion", test_data_ingestion)
    ]
    
    results = {}
    for test_name, test_func in tests:
        logger.info("")
        logger.info("-" * 60)
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Unexpected error in {test_name}: {str(e)}")
            results[test_name] = False
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("")
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info(f"End time: {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
