"""
Base Agent Framework for ark-os-noa Coding Agents

This module provides the foundation for all coding agents in the ark-os-noa platform.
Each agent is designed to automate specific development tasks and improve productivity.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import json
from datetime import datetime

class BaseAgent(ABC):
    """Base class for all coding agents"""
    
    def __init__(self, name: str, workspace_path: Path = None):
        self.name = name
        self.workspace_path = workspace_path or Path.cwd()
        self.logger = self._setup_logging()
        self.execution_log: List[Dict[str, Any]] = []
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the agent"""
        logger = logging.getLogger(f"agent.{self.name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def log_execution(self, action: str, details: Dict[str, Any] = None):
        """Log agent execution for audit trail"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "action": action,
            "details": details or {},
        }
        self.execution_log.append(entry)
        self.logger.info(f"Action: {action}")
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def validate_workspace(self) -> bool:
        """Validate that we're in a valid ark-os-noa workspace"""
        required_files = ["requirements.txt", "docker-compose.yml", "services"]
        
        for item in required_files:
            path = self.workspace_path / item
            if not path.exists():
                self.logger.error(f"Required workspace item not found: {item}")
                return False
        
        return True
    
    def save_execution_log(self, output_path: Path = None):
        """Save execution log to file"""
        if not output_path:
            output_path = self.workspace_path / f"logs/{self.name}_execution.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.execution_log, f, indent=2)
        
        self.logger.info(f"Execution log saved to {output_path}")

class AgentRegistry:
    """Registry to manage and discover coding agents"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
    
    def register(self, agent: BaseAgent):
        """Register an agent"""
        self._agents[agent.name] = agent
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self._agents.keys())
    
    def execute_agent(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute an agent by name"""
        agent = self.get_agent(name)
        if not agent:
            raise ValueError(f"Agent '{name}' not found")
        
        return agent.execute(**kwargs)

# Global agent registry instance
agent_registry = AgentRegistry()

def register_agent(agent_class):
    """Decorator to auto-register agents"""
    def wrapper(*args, **kwargs):
        agent = agent_class(*args, **kwargs)
        agent_registry.register(agent)
        return agent
    return wrapper