import logging
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class PromptContext:
    """Contexto para generación de prompts."""
    conv_type: str
    stage: str
    mood: str
    personality: str
    method: str
    area: str
    specific_topic: str
    attributes: Dict[str, Any]

class PromptManager:
    """Gestor de prompts para el generador de conversaciones."""
    
    def __init__(self, types_config: Dict, stages_config: Dict):
        self.logger = logging.getLogger(__name__)
        self.types_config = types_config
        self.stages_config = stages_config
        
    def generate_initial_prompt(self, context: PromptContext) -> str:
        """Genera el prompt inicial basado en el contexto."""
        try:
            type_config = self.types_config["tipos"].get(context.conv_type, {})
            prompts = type_config.get("prompts", {}).get("usuario", {})
            patterns = prompts.get("patrones_inicio", {}).get(context.method, [])
            
            if not patterns:
                self.logger.warning(f"No se encontraron patrones para {context.method}")
                return f"¿Qué necesitas saber sobre {context.specific_topic}?"
                
            template = random.choice(patterns)
            
            # Obtener categoría si existe
            category = (f"{context.attributes.get('category', '')}" 
                      if 'category' in context.attributes else "")
            topic = f"{context.specific_topic} - {category}".strip(" -")
            
            return template.format(
                tema=topic,
                concepto=topic,
                situacion=topic,
                aspecto=topic,
                servicio=topic,
                dispositivo=topic,
                elemento=topic,
                software=topic,
                aplicacion=topic,
                sistema=topic
            )
            
        except Exception as e:
            self.logger.error(f"Error generando prompt inicial: {str(e)}")
            return "¿En qué puedo ayudarte?"
            
    def generate_system_prompt(self, context: PromptContext) -> str:
        """Genera el prompt del sistema con instrucciones específicas."""
        try:
            # Obtener configuraciones
            type_config = self.types_config["tipos"][context.conv_type]
            stage_config = self.stages_config["stages"][context.stage]
            
            # Obtener campo de enfoque del tipo
            focus_fields = ['focus', 'style', 'consideration', 'depth']
            focus_field = next((f for f in focus_fields if f in type_config), None)
            
            if not focus_field:
                self.logger.warning(f"No se encontró campo de enfoque para {context.conv_type}")
                focus = ""
            else:
                focus = random.choice(type_config[focus_field])
                
            stage_focus = random.choice(stage_config["focus"])
            
            # Construir prompt del sistema
            system_prompt = f"""
            {type_config['prompts']['sistema']['base'].format(
                mood=context.mood,
                personality=context.personality
            )}
            
            {stage_config['system'].format(
                mood=context.mood,
                personality=context.personality
            )}
            
            Contexto actual: {context.specific_topic}
            Enfoque del tipo: {focus}
            Enfoque de la etapa: {stage_focus}
            
            IMPORTANTE: Mantén todas las respuestas estrictamente relacionadas con 
            el tema de '{context.specific_topic}'.
            No te desvíes hacia otros temas o ejemplos no relacionados.
            """.strip()
            
            return system_prompt
            
        except Exception as e:
            self.logger.error(f"Error generando prompt del sistema: {str(e)}")
            return ""
            
    def generate_next_user_prompt(self, context: PromptContext, conversation_history: List[Dict[str, str]]) -> str:
        """Genera un prompt para el siguiente mensaje del usuario."""
        try:
            type_config = self.types_config["tipos"][context.conv_type]
            prompts = type_config.get("prompts", {}).get("usuario", {})
            
            if not conversation_history:
                return self.generate_initial_prompt(context)
                
            # Obtener el último mensaje y respuesta
            last_exchange = conversation_history[-2:]  # Usuario y asistente
            if len(last_exchange) < 2:
                return self.generate_initial_prompt(context)
                
            # Usar template de seguimiento
            template = prompts.get("generacion_contexto", {}).get("template_seguimiento", "")
            if not template:
                return f"¿Podrías explicar más sobre {context.specific_topic}?"
                
            # Mapear acciones según el tipo de conversación
            mapping = prompts.get("generacion_contexto", {}).get("mapeo_acciones", {})
            topic_mapping = mapping.get(context.area, {}).get(context.specific_topic, [])
            
            if not topic_mapping:
                topic_mapping = ["explicar", "detallar", "profundizar", "analizar"]
                
            action = random.choice(topic_mapping)
            
            return template.format(
                elemento_previo=context.specific_topic,
                tema_previo=context.specific_topic,
                nueva_accion=action
            )
            
        except Exception as e:
            self.logger.error(f"Error generando siguiente prompt: {str(e)}")
            return f"¿Podrías decirme más sobre {context.specific_topic}?"