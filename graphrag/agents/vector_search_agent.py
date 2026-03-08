"""
Vector Search Agent for OpenSearch semantic search
"""

import logging
from typing import Dict, Any, List, Optional

from .base_agent import BaseAgent
from ..vector_store import OpenSearchVectorStore
from ..bedrock_client import BedrockClient
from ..config import graphrag_config

logger = logging.getLogger(__name__)

class VectorSearchAgent(BaseAgent):
    """Agent specialized in semantic search using OpenSearch"""
    
    def __init__(self, vector_store: OpenSearchVectorStore, bedrock_client: BedrockClient):
        super().__init__(
            name="VectorSearchAgent",
            description="Performs semantic search using vector embeddings"
        )
        self.vector_store = vector_store
        self.bedrock_client = bedrock_client
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup vector search tools"""
        self.add_tool({
            'name': 'semantic_search',
            'description': 'Perform semantic search using vector embeddings',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Search query'},
                    'filters': {'type': 'object', 'description': 'Search filters'},
                    'k': {'type': 'integer', 'description': 'Number of results'}
                },
                'required': ['query']
            }
        })
        
        self.add_tool({
            'name': 'hybrid_search',
            'description': 'Perform hybrid search (keyword + semantic)',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Search query'},
                    'filters': {'type': 'object', 'description': 'Search filters'},
                    'k': {'type': 'integer', 'description': 'Number of results'}
                },
                'required': ['query']
            }
        })
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute vector search task"""
        try:
            search_type = task.get('search_type', 'semantic')
            params = task.get('parameters', {})
            
            if search_type == 'semantic':
                result = self._semantic_search(params)
            elif search_type == 'hybrid':
                result = self._hybrid_search(params)
            else:
                result = {'success': False, 'error': f'Unknown search type: {search_type}'}
            
            self.log_execution(task, result)
            return result
            
        except Exception as e:
            logger.error(f"Error in VectorSearchAgent execution: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _semantic_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform semantic search"""
        try:
            query = params.get('query')
            filters = params.get('filters', {})
            k = params.get('k', graphrag_config.max_vector_results)
            
            # Generate query embedding
            query_embedding = self.bedrock_client.generate_embedding(query)
            
            if not query_embedding:
                return {'success': False, 'error': 'Failed to generate query embedding'}
            
            # Perform vector search
            results = self.vector_store.vector_search(query_embedding, filters, k)
            
            # Filter by similarity threshold
            filtered_results = [
                r for r in results 
                if r['score'] >= graphrag_config.similarity_threshold
            ]
            
            return {
                'success': True,
                'data': filtered_results,
                'count': len(filtered_results),
                'total_found': len(results)
            }
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _hybrid_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform hybrid search"""
        try:
            query = params.get('query')
            filters = params.get('filters', {})
            k = params.get('k', graphrag_config.max_vector_results)
            
            # Generate query embedding
            query_embedding = self.bedrock_client.generate_embedding(query)
            
            if not query_embedding:
                return {'success': False, 'error': 'Failed to generate query embedding'}
            
            # Perform hybrid search
            results = self.vector_store.hybrid_search(query, query_embedding, filters, k)
            
            # Filter by similarity threshold
            filtered_results = [
                r for r in results 
                if r['score'] >= graphrag_config.similarity_threshold
            ]
            
            return {
                'success': True,
                'data': filtered_results,
                'count': len(filtered_results),
                'total_found': len(results)
            }
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            return {'success': False, 'error': str(e)}
