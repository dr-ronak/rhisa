"""
OpenSearch Vector Store for semantic search
"""

import logging
from typing import List, Dict, Any, Optional
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

from .config import aws_config, graphrag_config

logger = logging.getLogger(__name__)

class OpenSearchVectorStore:
    """OpenSearch vector store for semantic search"""
    
    def __init__(self):
        self.endpoint = aws_config.opensearch_endpoint
        self.index_name = aws_config.opensearch_index
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup OpenSearch client with AWS authentication"""
        try:
            credentials = boto3.Session().get_credentials()
            awsauth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                aws_config.region,
                'es',
                session_token=credentials.token
            )
            
            self.client = OpenSearch(
                hosts=[{'host': self.endpoint, 'port': 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )
            logger.info("OpenSearch client initialized")
        except Exception as e:
            logger.error(f"Failed to setup OpenSearch client: {str(e)}")
            raise
    
    def create_index(self):
        """Create OpenSearch index with vector field"""
        index_body = {
            'settings': {
                'index': {
                    'knn': True,
                    'knn.algo_param.ef_search': 512
                }
            },
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'title': {'type': 'text'},
                    'content': {'type': 'text'},
                    'embedding': {
                        'type': 'knn_vector',
                        'dimension': 1024,  # Titan embeddings dimension
                        'method': {
                            'name': 'hnsw',
                            'space_type': 'cosinesimil',
                            'engine': 'nmslib',
                            'parameters': {
                                'ef_construction': 512,
                                'm': 16
                            }
                        }
                    },
                    'region': {'type': 'keyword'},
                    'language': {'type': 'keyword'},
                    'domain': {'type': 'keyword'},
                    'entity_type': {'type': 'keyword'},
                    'metadata': {'type': 'object'}
                }
            }
        }
        
        try:
            if not self.client.indices.exists(index=self.index_name):
                self.client.indices.create(index=self.index_name, body=index_body)
                logger.info(f"Created index: {self.index_name}")
            else:
                logger.info(f"Index already exists: {self.index_name}")
        except Exception as e:
            logger.error(f"Error creating index: {str(e)}")
            raise
    
    def index_document(self, doc_id: str, content: str, embedding: List[float],
                      metadata: Dict[str, Any]) -> bool:
        """Index a document with its embedding"""
        try:
            document = {
                'id': doc_id,
                'content': content,
                'embedding': embedding,
                **metadata
            }
            
            self.client.index(
                index=self.index_name,
                id=doc_id,
                body=document
            )
            logger.info(f"Indexed document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return False
    
    def vector_search(self, query_embedding: List[float], 
                     filters: Optional[Dict[str, Any]] = None,
                     k: int = 10) -> List[Dict[str, Any]]:
        """Perform vector similarity search"""
        try:
            query = {
                'size': k,
                'query': {
                    'bool': {
                        'must': [
                            {
                                'knn': {
                                    'embedding': {
                                        'vector': query_embedding,
                                        'k': k
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            
            # Add filters if provided
            if filters:
                filter_clauses = []
                for key, value in filters.items():
                    filter_clauses.append({'term': {key: value}})
                query['query']['bool']['filter'] = filter_clauses
            
            response = self.client.search(
                index=self.index_name,
                body=query
            )
            
            results = []
            for hit in response['hits']['hits']:
                results.append({
                    'id': hit['_id'],
                    'score': hit['_score'],
                    'content': hit['_source'].get('content', ''),
                    'metadata': {k: v for k, v in hit['_source'].items() 
                               if k not in ['content', 'embedding']}
                })
            
            return results
        except Exception as e:
            logger.error(f"Error in vector search: {str(e)}")
            return []
    
    def hybrid_search(self, query_text: str, query_embedding: List[float],
                     filters: Optional[Dict[str, Any]] = None,
                     k: int = 10) -> List[Dict[str, Any]]:
        """Perform hybrid search (keyword + vector)"""
        try:
            query = {
                'size': k,
                'query': {
                    'bool': {
                        'should': [
                            {
                                'multi_match': {
                                    'query': query_text,
                                    'fields': ['title^2', 'content'],
                                    'type': 'best_fields'
                                }
                            },
                            {
                                'knn': {
                                    'embedding': {
                                        'vector': query_embedding,
                                        'k': k
                                    }
                                }
                            }
                        ],
                        'minimum_should_match': 1
                    }
                }
            }
            
            # Add filters
            if filters:
                filter_clauses = []
                for key, value in filters.items():
                    filter_clauses.append({'term': {key: value}})
                query['query']['bool']['filter'] = filter_clauses
            
            response = self.client.search(
                index=self.index_name,
                body=query
            )
            
            results = []
            for hit in response['hits']['hits']:
                results.append({
                    'id': hit['_id'],
                    'score': hit['_score'],
                    'content': hit['_source'].get('content', ''),
                    'metadata': {k: v for k, v in hit['_source'].items() 
                               if k not in ['content', 'embedding']}
                })
            
            return results
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the index"""
        try:
            self.client.delete(index=self.index_name, id=doc_id)
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def bulk_index(self, documents: List[Dict[str, Any]]) -> bool:
        """Bulk index multiple documents"""
        try:
            from opensearchpy import helpers
            
            actions = []
            for doc in documents:
                action = {
                    '_index': self.index_name,
                    '_id': doc['id'],
                    '_source': doc
                }
                actions.append(action)
            
            helpers.bulk(self.client, actions)
            logger.info(f"Bulk indexed {len(documents)} documents")
            return True
        except Exception as e:
            logger.error(f"Error in bulk indexing: {str(e)}")
            return False
