"""
Neptune Graph Store for healthcare knowledge graph
"""

import logging
from typing import List, Dict, Any, Optional
from gremlin_python.driver import client, serializer
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import json

from .config import aws_config

logger = logging.getLogger(__name__)

class NeptuneGraphStore:
    """Neptune graph database interface for healthcare knowledge"""
    
    def __init__(self):
        self.endpoint = aws_config.neptune_endpoint
        self.port = aws_config.neptune_port
        self.connection = None
        self.g = None
        
    def connect(self):
        """Establish connection to Neptune"""
        try:
            connection_string = f'wss://{self.endpoint}:{self.port}/gremlin'
            self.connection = DriverRemoteConnection(
                connection_string,
                'g',
                message_serializer=serializer.GraphSONSerializersV2d0()
            )
            self.g = traversal().withRemote(self.connection)
            logger.info("Connected to Neptune successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Neptune: {str(e)}")
            raise
    
    def close(self):
        """Close Neptune connection"""
        if self.connection:
            self.connection.close()
            logger.info("Neptune connection closed")
    
    def add_medical_entity(self, entity_type: str, entity_id: str, properties: Dict[str, Any]) -> bool:
        """Add a medical entity to the graph"""
        try:
            vertex = self.g.addV(entity_type).property('id', entity_id)
            
            for key, value in properties.items():
                vertex = vertex.property(key, value)
            
            vertex.next()
            logger.info(f"Added {entity_type} entity: {entity_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding entity: {str(e)}")
            return False
    
    def add_relationship(self, from_id: str, to_id: str, relationship_type: str, 
                        properties: Optional[Dict[str, Any]] = None) -> bool:
        """Add a relationship between entities"""
        try:
            edge = self.g.V().has('id', from_id).addE(relationship_type).to(
                __.V().has('id', to_id)
            )
            
            if properties:
                for key, value in properties.items():
                    edge = edge.property(key, value)
            
            edge.next()
            logger.info(f"Added relationship: {from_id} -{relationship_type}-> {to_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding relationship: {str(e)}")
            return False
    
    def query_neighbors(self, entity_id: str, max_hops: int = 2) -> List[Dict[str, Any]]:
        """Query neighboring entities in the graph"""
        try:
            results = (
                self.g.V().has('id', entity_id)
                .repeat(__.both().simplePath())
                .times(max_hops)
                .dedup()
                .valueMap(True)
                .toList()
            )
            
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error querying neighbors: {str(e)}")
            return []
    
    def find_path(self, start_id: str, end_id: str, max_hops: int = 5) -> List[Dict[str, Any]]:
        """Find path between two entities"""
        try:
            path = (
                self.g.V().has('id', start_id)
                .repeat(__.both().simplePath())
                .until(__.has('id', end_id))
                .limit(1)
                .path()
                .by(__.valueMap(True))
                .toList()
            )
            
            if path:
                return self._format_path(path[0])
            return []
        except Exception as e:
            logger.error(f"Error finding path: {str(e)}")
            return []
    
    def query_by_condition(self, condition: str, region: str) -> List[Dict[str, Any]]:
        """Query entities related to a medical condition in a specific region"""
        try:
            results = (
                self.g.V()
                .has('type', 'condition')
                .has('name', condition)
                .has('region', region)
                .both()
                .dedup()
                .valueMap(True)
                .toList()
            )
            
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error querying by condition: {str(e)}")
            return []
    
    def get_treatment_path(self, condition: str, region: str) -> Dict[str, Any]:
        """Get treatment pathway for a condition"""
        try:
            # Find condition node
            condition_node = (
                self.g.V()
                .has('type', 'condition')
                .has('name', condition)
                .has('region', region)
                .valueMap(True)
                .toList()
            )
            
            if not condition_node:
                return {}
            
            # Get symptoms
            symptoms = (
                self.g.V()
                .has('type', 'condition')
                .has('name', condition)
                .out('has_symptom')
                .valueMap(True)
                .toList()
            )
            
            # Get treatments
            treatments = (
                self.g.V()
                .has('type', 'condition')
                .has('name', condition)
                .out('treated_by')
                .valueMap(True)
                .toList()
            )
            
            # Get medications
            medications = (
                self.g.V()
                .has('type', 'condition')
                .has('name', condition)
                .out('requires_medication')
                .valueMap(True)
                .toList()
            )
            
            return {
                'condition': self._format_results(condition_node)[0] if condition_node else {},
                'symptoms': self._format_results(symptoms),
                'treatments': self._format_results(treatments),
                'medications': self._format_results(medications)
            }
        except Exception as e:
            logger.error(f"Error getting treatment path: {str(e)}")
            return {}
    
    def get_regional_guidelines(self, region: str, domain: str) -> List[Dict[str, Any]]:
        """Get regional healthcare guidelines"""
        try:
            results = (
                self.g.V()
                .has('type', 'guideline')
                .has('region', region)
                .has('domain', domain)
                .valueMap(True)
                .toList()
            )
            
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error getting regional guidelines: {str(e)}")
            return []
    
    def _format_results(self, results: List) -> List[Dict[str, Any]]:
        """Format Gremlin results to dictionaries"""
        formatted = []
        for result in results:
            formatted_item = {}
            for key, value in result.items():
                if isinstance(value, list) and len(value) > 0:
                    formatted_item[key] = value[0]
                else:
                    formatted_item[key] = value
            formatted.append(formatted_item)
        return formatted
    
    def _format_path(self, path: List) -> List[Dict[str, Any]]:
        """Format path results"""
        return [self._format_results([node])[0] for node in path]
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
