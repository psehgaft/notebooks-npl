from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import logging
import random

@dataclass
class ConversationStage:
    """Representa una etapa de conversación con sus atributos."""
    id: str
    name: str
    system_template: str
    user_template: str
    focus_options: List[str]
    max_tokens: int

class ConversationStageManager:
    """Gestiona las diferentes etapas de la conversación."""
    
    def __init__(self, stages_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.stages_config = stages_config
        self.conversation_stages = self._initialize_stages()
        self.stage_sequence = ['initiation', 'development', 'consolidation', 'transition']
        
    def _initialize_stages(self) -> Dict[str, ConversationStage]:
        """Inicializa las etapas desde la configuración."""
        stages = {}
        try:
            for stage_id, config in self.stages_config["stages"].items():
                stages[stage_id] = ConversationStage(
                    id=stage_id,
                    name=stage_id.replace("_", " ").title(),
                    system_template=config.get("system", ""),
                    user_template=config.get("user", ""),
                    focus_options=config.get("focus", []),
                    max_tokens=self._get_stage_tokens(stage_id)
                )
                
            return stages
            
        except Exception as e:
            self.logger.error(f"Error inicializando etapas: {str(e)}")
            return {}
            
    def _get_stage_tokens(self, stage_id: str) -> int:
        """Determina el número de tokens para una etapa."""
        tokens_map = {
            'initiation': 100,
            'development': 150,
            'consolidation': 200,
            'transition': 100
        }
        return tokens_map.get(stage_id, 150)
        
    def get_stage(self, stage_id: str) -> Optional[ConversationStage]:
        """Obtiene una etapa por su ID."""
        return self.conversation_stages.get(stage_id)
        
    def get_valid_stages(self) -> List[str]:
        """Obtiene la lista de etapas válidas."""
        return self.stage_sequence
        
    def get_next_stage(self, current_stage: str) -> str:
        """Obtiene la siguiente etapa en la secuencia."""
        try:
            current_index = self.stage_sequence.index(current_stage)
            next_index = (current_index + 1) % len(self.stage_sequence)
            return self.stage_sequence[next_index]
        except ValueError:
            return 'initiation'
            
    def get_stage_parameters(self, stage_id: str) -> Dict[str, Any]:
        """Obtiene los parámetros específicos de una etapa."""
        stage = self.get_stage(stage_id)
        if not stage:
            return {}
            
        return {
            'max_tokens': stage.max_tokens,
            'focus': random.choice(stage.focus_options) if stage.focus_options else "",
            'system_template': stage.system_template,
            'user_template': stage.user_template
        }
        
    def format_stage_prompt(
        self,
        stage_id: str,
        conv_type: str,
        context: str,
        mood: str,
        personality: str
    ) -> str:
        """Formatea el prompt del sistema para una etapa específica."""
        stage = self.get_stage(stage_id)
        if not stage:
            return ""
            
        try:
            focus = random.choice(stage.focus_options) if stage.focus_options else ""
            
            return stage.system_template.format(
                mood=mood,
                personality=personality,
                conv_type=conv_type,
                context=context,
                focus=focus
            )
            
        except Exception as e:
            self.logger.error(f"Error formateando prompt de etapa: {str(e)}")
            return ""
            
    def validate_stage_sequence(self, stages: List[str]) -> bool:
        """Valida que una secuencia de etapas sea válida."""
        if not stages:
            return False
            
        try:
            # Verificar que todas las etapas existan
            if not all(stage in self.conversation_stages for stage in stages):
                return False
                
            # Verificar orden lógico
            for i in range(len(stages) - 1):
                current = stages[i]
                next_stage = stages[i + 1]
                
                current_index = self.stage_sequence.index(current)
                next_index = self.stage_sequence.index(next_stage)
                
                # Permitir avanzar o volver al inicio
                if next_index != (current_index + 1) % len(self.stage_sequence):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando secuencia de etapas: {str(e)}")
            return False