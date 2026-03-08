"""
Orchestrator Agent for coordinating multiple agents
"""

import logging
from typing import Dict, Any, List, Optional
import json

from .base_agent import BaseAgent
from .graph_query_agent import GraphQueryAgent
from .vector_search_agent import VectorSearchAgent
from ..bedrock_client import BedrockClient
from ..config import graphrag_config

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """Main orchestrator agent that coordinates other agents"""
    
    def __init__(self, graph_agent: GraphQueryAgent, vector_agent: VectorSearchAgent,
                 bedrock_client: BedrockClient):
        super().__init__(
            name="OrchestratorAgent",
            description="Orchestrates multiple agents to answer complex healthcare queries"
        )
        self.graph_agent = graph_agent
        self.vector_agent = vector_agent
        self.bedrock_client = bedrock_client
        self.max_iterations = graphrag_config.max_agent_iterations
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestrated task"""
        try:
            query = task.get('query', '')
            region = task.get('region', 'gujarat')
            language = task.get('language', 'en')
            domain = task.get('domain', 'eye_health')
            
            # Step 1: Analyze query and plan execution
            plan = self._create_execution_plan(query, region, domain)
            
            # Step 2: Execute plan with multiple agents
            context = self._execute_plan(plan, query, region, domain)
            
            # Step 3: Generate final response
            response = self._generate_response(query, context, region, language)
            
            result = {
                'success': True,
                'response': response,
                'context': context,
                'plan': plan
            }
            
            self.log_execution(task, result)
            return result
            
        except Exception as e:
            logger.error(f"Error in OrchestratorAgent execution: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _create_execution_plan(self, query: str, region: str, domain: str) -> Dict[str, Any]:
        """Create execution plan using LLM"""
        try:
            system_prompt = """You are a healthcare query planner. Analyze the user query and create an execution plan.
Determine which agents to use:
- graph_query: For finding relationships, treatment paths, guidelines
- vector_search: For semantic search of healthcare documents
- both: When both graph and vector search are needed

Return a JSON object with:
{
    "agents": ["graph_query", "vector_search"],
    "graph_tasks": [{"query_type": "...", "parameters": {...}}],
    "vector_tasks": [{"search_type": "...", "parameters": {...}}],
    "reasoning": "explanation of the plan"
}"""
            
            prompt = f"""Query: {query}
Region: {region}
Domain: {domain}

Create an execution plan:"""
            
            response = self.bedrock_client.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3
            )
            
            # Parse JSON response
            try:
                plan = json.loads(response)
                return plan
            except:
                # Fallback plan
                return {
                    'agents': ['vector_search', 'graph_query'],
                    'graph_tasks': [{'query_type': 'neighbors', 'parameters': {}}],
                    'vector_tasks': [{'search_type': 'hybrid', 'parameters': {'query': query}}],
                    'reasoning': 'Default plan'
                }
                
        except Exception as e:
            logger.error(f"Error creating execution plan: {str(e)}")
            return {'agents': ['vector_search'], 'vector_tasks': [], 'graph_tasks': []}
    
    def _execute_plan(self, plan: Dict[str, Any], query: str, region: str, 
                     domain: str) -> Dict[str, Any]:
        """Execute the planned tasks"""
        context = {
            'graph_results': [],
            'vector_results': [],
            'combined_context': ''
        }
        
        try:
            agents = plan.get('agents', [])
            
            # Execute vector search tasks
            if 'vector_search' in agents:
                vector_tasks = plan.get('vector_tasks', [])
                if not vector_tasks:
                    # Default vector search
                    vector_tasks = [{
                        'search_type': 'hybrid',
                        'parameters': {
                            'query': query,
                            'filters': {'region': region, 'domain': domain},
                            'k': 5
                        }
                    }]
                
                for task in vector_tasks:
                    result = self.vector_agent.execute(task)
                    if result.get('success'):
                        context['vector_results'].extend(result.get('data', []))
            
            # Execute graph query tasks
            if 'graph_query' in agents:
                graph_tasks = plan.get('graph_tasks', [])
                
                for task in graph_tasks:
                    result = self.graph_agent.execute(task)
                    if result.get('success'):
                        context['graph_results'].append(result.get('data', {}))
            
            # Combine context
            context['combined_context'] = self._combine_context(
                context['vector_results'],
                context['graph_results']
            )
            
            return context
            
        except Exception as e:
            logger.error(f"Error executing plan: {str(e)}")
            return context
    
    def _combine_context(self, vector_results: List[Dict], 
                        graph_results: List[Dict]) -> str:
        """Combine results from different sources"""
        combined = []
        
        # Add vector search results
        if vector_results:
            combined.append("=== Semantic Search Results ===")
            for i, result in enumerate(vector_results[:3], 1):
                combined.append(f"\n{i}. {result.get('content', '')[:300]}...")
        
        # Add graph results
        if graph_results:
            combined.append("\n\n=== Knowledge Graph Results ===")
            for i, result in enumerate(graph_results, 1):
                combined.append(f"\n{i}. {json.dumps(result, indent=2)[:300]}...")
        
        return "\n".join(combined)
    
    def _generate_response(self, query: str, context: Dict[str, Any], 
                          region: str, language: str) -> str:
        """Generate final response using LLM"""
        try:
            system_prompt = f"""You are RHISA, a healthcare assistant for {region.title()}.
Provide accurate, helpful healthcare information based on the context provided.
Respond in {language} language.
Always include disclaimers about consulting healthcare professionals."""
            
            prompt = f"""User Query: {query}

Context:
{context.get('combined_context', '')}

Provide a comprehensive, accurate response:"""
            
            response = self.bedrock_client.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error generating a response."
