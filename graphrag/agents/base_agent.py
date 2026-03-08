"""
Base Agent class for agentic GraphRAG
"""

import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.execution_history = []
        self.tools = []
        
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task"""
        pass
    
    def add_tool(self, tool: Dict[str, Any]):
        """Add a tool to the agent's toolkit"""
        self.tools.append(tool)
        logger.info(f"Added tool '{tool['name']}' to agent '{self.name}'")
    
    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get schema for all available tools"""
        return self.tools
    
    def log_execution(self, task: Dict[str, Any], result: Dict[str, Any]):
        """Log agent execution"""
        self.execution_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'task': task,
            'result': result
        })
    
    def reflect(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on execution result and suggest improvements"""
        reflection = {
            'success': result.get('success', False),
            'suggestions': [],
            'needs_retry': False
        }
        
        if not result.get('success'):
            reflection['needs_retry'] = True
            reflection['suggestions'].append('Task failed, consider retrying with different approach')
        
        return reflection
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get agent's execution history"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
        logger.info(f"Cleared execution history for agent '{self.name}'")
