from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import logging
import random

@dataclass
class ConversationType:
    """Representa un tipo de conversación con sus atributos."""
    id: str
    name: str
    context: Dict[str, Any]
    prompts: Dict[str, Any]
    focus_options: List[str]
    valid_methods: List[str]
    
class ConversationTypeManager:
    """Gestiona los diferentes tipos de conversación."""
    
    def __init__(self, types_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.types_config = types_config
        self.conversation_types = self._initialize_types()
        
    def _initialize_types(self) -> Dict[str, ConversationType]:
        """Inicializa los tipos de conversación desde la configuración."""
        types = {}
        try:
            for type_id, config in self.types_config["tipos"].items():
                focus_fields = ['focus', 'style', 'consideration', 'depth']
                focus_options = []
                
                # Obtener opciones de enfoque del primer campo disponible
                for field in focus_fields:
                    if field in config:
                        focus_options = config[field]
                        break
                        
                # Obtener métodos válidos
                valid_methods = []
                for area in config.get("contexto", {}).values():
                    valid_methods.extend([
                        method for method in area.keys()
                        if method.startswith("mediante_")
                    ])
                valid_methods = list(set(valid_methods))  # Eliminar duplicados
                
                types[type_id] = ConversationType(
                    id=type_id,
                    name=type_id.replace("_", " ").title(),
                    context=config.get("contexto", {}),
                    prompts=config.get("prompts", {}),
                    focus_options=focus_options,
                    valid_methods=valid_methods
                )
                
            return types
            
        except Exception as e:
            self.logger.error(f"Error inicializando tipos: {str(e)}")
            return {}
            
    def get_type(self, type_id: str) -> Optional[ConversationType]:
        """Obtiene un tipo de conversación por su ID."""
        return self.conversation_types.get(type_id)
        
    def get_valid_types(self) -> List[str]:
        """Obtiene la lista de tipos válidos."""
        return list(self.conversation_types.keys())
        
    def get_random_context(self, type_id: str) -> Dict[str, Any]:
        """Obtiene un contexto aleatorio para un tipo de conversación."""
        conv_type = self.get_type(type_id)
        if not conv_type:
            return {}
            
        try:
            # Seleccionar área aleatoria
            area = random.choice(list(conv_type.context.keys()))
            area_context = conv_type.context[area]
            
            # Seleccionar método aleatorio
            method = random.choice([k for k in area_context.keys() if k.startswith("mediante_")])
            method_context = area_context[method]
            
            # Seleccionar tema específico aleatorio
            topic = random.choice(list(method_context.keys()))
            topic_context = method_context[topic]
            
            # Seleccionar categoría si existe
            category = ""
            if isinstance(topic_context, dict):
                category = random.choice(list(topic_context.keys()))
            
            return {
                "area": area,
                "method": method,
                "topic": topic,
                "category": category
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo contexto aleatorio: {str(e)}")
            return {}
            
    def get_system_instructions(self, type_id: str, method: str) -> List[str]:
        """Obtiene las instrucciones del sistema para un tipo y método."""
        conv_type = self.get_type(type_id)
        if not conv_type:
            return []
            
        try:
            system_config = conv_type.prompts.get("sistema", {})
            instructions = system_config.get("instrucciones", {})
            
            # Obtener instrucciones generales
            general_instructions = instructions.get("general", [])
            
            # Obtener instrucciones específicas del método
            method_instructions = instructions.get("por_medio", {}).get(method, [])
            
            return general_instructions + method_instructions
            
        except Exception as e:
            self.logger.error(f"Error obteniendo instrucciones: {str(e)}")
            return []
            
    def validate_context(self, type_id: str, area: str, method: str, topic: str) -> bool:
        """Valida que un contexto específico sea válido para un tipo."""
        conv_type = self.get_type(type_id)
        if not conv_type:
            return False
            
        try:
            # Validar jerarquía completa
            if area not in conv_type.context:
                return False
                
            area_context = conv_type.context[area]
            if method not in area_context:
                return False
                
            method_context = area_context[method]
            if topic not in method_context:
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando contexto: {str(e)}")
            return False