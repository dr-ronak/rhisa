"""
Amazon Bedrock client for LLM and embeddings
"""

import logging
import json
from typing import List, Dict, Any, Optional
import boto3
from botocore.config import Config

from .config import aws_config, graphrag_config

logger = logging.getLogger(__name__)

class BedrockClient:
    """Amazon Bedrock client for LLM operations"""
    
    def __init__(self):
        self.region = aws_config.bedrock_region
        self.model_id = aws_config.bedrock_model_id
        self.embedding_model = aws_config.bedrock_embedding_model
        
        config = Config(
            region_name=self.region,
            retries={'max_attempts': 3, 'mode': 'adaptive'}
        )
        
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            config=config
        )
        
        self.bedrock = boto3.client(
            'bedrock',
            config=config
        )
        
        logger.info("Bedrock client initialized")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Titan Embeddings"""
        try:
            body = json.dumps({
                'inputText': text
            })
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.embedding_model,
                body=body,
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            embedding = response_body.get('embedding', [])
            
            logger.debug(f"Generated embedding of dimension: {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None,
                         temperature: Optional[float] = None,
                         max_tokens: Optional[int] = None) -> str:
        """Generate response using Claude 3"""
        try:
            temp = temperature if temperature is not None else graphrag_config.temperature
            max_tok = max_tokens if max_tokens is not None else graphrag_config.max_tokens
            
            messages = [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
            
            body = {
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': messages,
                'temperature': temp,
                'max_tokens': max_tok,
                'top_p': graphrag_config.top_p
            }
            
            if system_prompt:
                body['system'] = system_prompt
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text from Claude 3 response
            content = response_body.get('content', [])
            if content and len(content) > 0:
                return content[0].get('text', '')
            
            return ''
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return ''
    
    def generate_with_tools(self, prompt: str, tools: List[Dict[str, Any]],
                           system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response with tool calling capability"""
        try:
            messages = [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
            
            body = {
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': messages,
                'temperature': graphrag_config.temperature,
                'max_tokens': graphrag_config.max_tokens,
                'tools': tools
            }
            
            if system_prompt:
                body['system'] = system_prompt
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            return response_body
        except Exception as e:
            logger.error(f"Error in tool calling: {str(e)}")
            return {}
    
    def rerank_results(self, query: str, documents: List[Dict[str, Any]],
                      top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Rerank search results using LLM"""
        try:
            k = top_k if top_k is not None else graphrag_config.rerank_top_k
            
            # Create reranking prompt
            docs_text = "\n\n".join([
                f"Document {i+1}:\n{doc.get('content', '')[:500]}"
                for i, doc in enumerate(documents)
            ])
            
            prompt = f"""Given the query: "{query}"

Rank the following documents by relevance. Return only the document numbers in order of relevance (most relevant first), separated by commas.

{docs_text}

Ranking (comma-separated document numbers):"""
            
            response = self.generate_response(
                prompt=prompt,
                temperature=0.1,
                max_tokens=100
            )
            
            # Parse ranking
            try:
                rankings = [int(x.strip()) - 1 for x in response.split(',')]
                reranked = [documents[i] for i in rankings if i < len(documents)]
                return reranked[:k]
            except:
                # Fallback to original order
                return documents[:k]
                
        except Exception as e:
            logger.error(f"Error reranking results: {str(e)}")
            return documents[:top_k] if top_k else documents
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract medical entities from text"""
        try:
            prompt = f"""Extract medical entities from the following text. Return a JSON array of entities with their type (condition, symptom, medication, treatment, or body_part).

Text: {text}

JSON array:"""
            
            response = self.generate_response(
                prompt=prompt,
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse JSON response
            try:
                entities = json.loads(response)
                return entities
            except:
                return []
                
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return []
