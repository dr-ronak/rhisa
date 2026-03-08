"""
Main GraphRAG Engine integrating all components
"""

import logging
from typing import Dict, Any, Optional

from .bedrock_client import BedrockClient
from .graph_store import NeptuneGraphStore
from .vector_store import OpenSearchVectorStore
from .agents import OrchestratorAgent, GraphQueryAgent, VectorSearchAgent
from .config import aws_config, graphrag_config

logger = logging.getLogger(__name__)

class GraphRAGEngine:
    """Main GraphRAG engine for RHISA Healthcare Chatbot"""
    
    def __init__(self):
        self.bedrock_client = None
        self.graph_store = None
        self.vector_store = None
        self.orchestrator = None
        self._initialized = False
    
    def initialize(self):
        """Initialize all components"""
        try:
            logger.info("Initializing GraphRAG Engine...")
            
            # Initialize Bedrock client
            self.bedrock_client = BedrockClient()
            logger.info("✓ Bedrock client initialized")
            
            # Initialize Neptune graph store
            self.graph_store = NeptuneGraphStore()
            self.graph_store.connect()
            logger.info("✓ Neptune graph store connected")
            
            # Initialize OpenSearch vector store
            self.vector_store = OpenSearchVectorStore()
            logger.info("✓ OpenSearch vector store initialized")
            
            # Initialize agents
            graph_agent = GraphQueryAgent(self.graph_store)
            vector_agent = VectorSearchAgent(self.vector_store, self.bedrock_client)
            self.orchestrator = OrchestratorAgent(
                graph_agent, vector_agent, self.bedrock_client
            )
            logger.info("✓ Agents initialized")
            
            self._initialized = True
            logger.info("GraphRAG Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize GraphRAG Engine: {str(e)}")
            raise
    
    def query(self, query: str, region: str = 'gujarat', 
             language: str = 'en', domain: str = 'eye_health') -> Dict[str, Any]:
        """Execute a query through the GraphRAG system"""
        if not self._initialized:
            raise RuntimeError("GraphRAG Engine not initialized. Call initialize() first.")
        
        try:
            task = {
                'query': query,
                'region': region,
                'language': language,
                'domain': domain
            }
            
            logger.info(f"Processing query: {query}")
            result = self.orchestrator.execute(task)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': 'I apologize, but I encountered an error processing your query.'
            }
    
    def index_document(self, doc_id: str, content: str, 
                      metadata: Dict[str, Any]) -> bool:
        """Index a document in the vector store"""
        if not self._initialized:
            raise RuntimeError("GraphRAG Engine not initialized")
        
        try:
            # Generate embedding
            embedding = self.bedrock_client.generate_embedding(content)
            
            if not embedding:
                logger.error(f"Failed to generate embedding for document: {doc_id}")
                return False
            
            # Index in OpenSearch
            success = self.vector_store.index_document(
                doc_id, content, embedding, metadata
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return False
    
    def add_graph_entity(self, entity_type: str, entity_id: str, 
                        properties: Dict[str, Any]) -> bool:
        """Add an entity to the knowledge graph"""
        if not self._initialized:
            raise RuntimeError("GraphRAG Engine not initialized")
        
        try:
            return self.graph_store.add_medical_entity(
                entity_type, entity_id, properties
            )
        except Exception as e:
            logger.error(f"Error adding graph entity: {str(e)}")
            return False
    
    def add_graph_relationship(self, from_id: str, to_id: str, 
                              relationship_type: str,
                              properties: Optional[Dict[str, Any]] = None) -> bool:
        """Add a relationship to the knowledge graph"""
        if not self._initialized:
            raise RuntimeError("GraphRAG Engine not initialized")
        
        try:
            return self.graph_store.add_relationship(
                from_id, to_id, relationship_type, properties
            )
        except Exception as e:
            logger.error(f"Error adding graph relationship: {str(e)}")
            return False
    
    def shutdown(self):
        """Shutdown the GraphRAG engine"""
        try:
            if self.graph_store:
                self.graph_store.close()
            
            self._initialized = False
            logger.info("GraphRAG Engine shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
