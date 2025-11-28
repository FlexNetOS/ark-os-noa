"""
Coding Agents Package for ark-os-noa

This package contains automated development agents that speed up
common development tasks in the ark-os-noa platform.
"""

from .base_agent import BaseAgent, AgentRegistry, agent_registry
from .service_generator import ServiceGeneratorAgent

__all__ = [
    "BaseAgent",
    "AgentRegistry", 
    "agent_registry",
    "ServiceGeneratorAgent"
]