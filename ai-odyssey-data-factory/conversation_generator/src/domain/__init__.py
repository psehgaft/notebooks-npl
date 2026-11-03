"""
Módulo de dominio con tipos de conversación y etapas.
"""

from .conversation_types import ConversationTypeManager
from .conversation_stages import ConversationStageManager
from .conversation_governance import ConversationGovernance

__all__ = [
    "ConversationTypeManager",
    "ConversationStageManager", 
    "ConversationGovernance"
]