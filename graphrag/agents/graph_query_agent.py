"""
Graph Query Agent for Neptune graph traversal
"""

import logging
from typing import Dict, Any, List, Optional

from .base_agent import BaseAgent
from ..graph_store import NeptuneGraphStore
from ..config import graphrag_config

logger = logging.getLogger(__name__)

class GraphQueryAgent(BaseAgent):
    """Agent specialized in querying the Neptune knowledge graph"""
    
    def __init__(self, graph_store: NeptuneGraphStore):
        super().__init__(
            name="GraphQueryAgent",
            description="Queries Neptune knowledge graph for medical entities and relationships"
        )
        self.graph_store = graph_store
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup graph query tools"""
        self.add_tool({
            'name': 'query_neighbors',
            'description': 'Query neighboring entities in the graph',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'entity_id': {'type': 'string', 'description': 'Entity ID to query'},
                    'max_hops': {'type': 'integer', 'description': 'Maximum hops in graph'}
                },
                'required': ['entity_id']
            }
        })
        
        self.add_tool({
            'name': 'find_treatment_path',
            'description': 'Find treatment pathway for a medical condition',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'condition': {'type': 'string', 'description': 'Medical condition name'},
                    'region': {'type': 'string', 'description': 'Region (gujarat/maharashtra)'}
                },
                'required': ['condition', 'region']
            }
        })
        
        self.add_tool({
            'name': 'get_regional_guidelines',
            'description': 'Get regional healthcare guidelines',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'region': {'type': 'string', 'description': 'Region name'},
                    'domain': {'type': 'string', 'description': 'Healthcare domain'}
                },
                'required': ['region', 'domain']
            }
        })
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute graph query task"""
        try:
            query_type = task.get('query_type', 'neighbors')
            params = task.get('parameters', {})
            
            if query_type == 'neighbors':
                result = self._query_neighbors(params)
            elif query_type == 'treatment_path':
                result = self._find_treatment_path(params)
            elif query_type == 'regional_guidelines':
                result = self._get_regional_guidelines(params)
            elif query_type == 'find_path':
                result = self._find_path(params)
            else:
                result = {'success': False, 'error': f'Unknown query type: {query_type}'}
            
            self.log_execution(task, result)
            return result
            
        except Exception as e:
            logger.error(f"Error in GraphQueryAgent execution: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _query_neighbors(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Query neighboring entities"""
        try:
            entity_id = params.get('entity_id')
            max_hops = params.get('max_hops', graphrag_config.graph_traversal_depth)
            
            neighbors = self.graph_store.query_neighbors(entity_id, max_hops)
            
            return {
                'success': True,
                'data': neighbors,
                'count': len(neighbors)
            }
        except Exception as e:
            logger.error(f"Error querying neighbors: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _find_treatment_path(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find treatment pathway"""
        try:
            condition = params.get('condition')
            region = params.get('region')
            
            pathway = self.graph_store.get_treatment_path(condition, region)
            
            return {
                'success': True,
                'data': pathway,
                'has_data': bool(pathway)
            }
        except Exception as e:
            logger.error(f"Error finding treatment path: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _get_regional_guidelines(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get regional guidelines"""
        try:
            region = params.get('region')
            domain = params.get('domain')
            
            guidelines = self.graph_store.get_regional_guidelines(region, domain)
            
            return {
                'success': True,
                'data': guidelines,
                'count': len(guidelines)
            }
        except Exception as e:
            logger.error(f"Error getting regional guidelines: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _find_path(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find path between entities"""
        try:
            start_id = params.get('start_id')
            end_id = params.get('end_id')
            max_hops = params.get('max_hops', 5)
            
            path = self.graph_store.find_path(start_id, end_id, max_hops)
            
            return {
                'success': True,
                'data': path,
                'path_length': len(path)
            }
        except Exception as e:
            logger.error(f"Error finding path: {str(e)}")
            return {'success': False, 'error': str(e)}
