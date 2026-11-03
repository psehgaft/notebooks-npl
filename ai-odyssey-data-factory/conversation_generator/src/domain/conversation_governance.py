from typing import Dict, List, Tuple, Optional
import logging
import json

class ConversationGovernance:
    """Gestiona las reglas y transiciones de la conversación."""
    
    def __init__(self, types_config: Dict, stages_config: Dict):
        self.logger = logging.getLogger(__name__)
        self.types_config = types_config
        self.stages_config = stages_config
        self.transition_rules = self._initialize_transition_rules()
        
    def _initialize_transition_rules(self) -> Dict:
        """Inicializa las reglas de transición entre tipos y etapas."""
        return {
            'clarification_and_framing': {
                'initiation': ['development', 'practical_assistance'],
                'development': ['consolidation', 'informative_analytical'],
                'consolidation': ['transition', 'structured_emotional_support'],
                'transition': ['initiation']
            },
            'practical_assistance': {
                'initiation': ['development', 'informative_analytical'],
                'development': ['consolidation', 'clarification_and_framing'],
                'consolidation': ['transition'],
                'transition': ['initiation', 'clarification_and_framing']
            },
            'informative_analytical': {
                'initiation': ['development', 'practical_assistance'],
                'development': ['consolidation', 'clarification_and_framing'],
                'consolidation': ['transition'],
                'transition': ['initiation']
            },
            'structured_emotional_support': {
                'initiation': ['development'],
                'development': ['consolidation', 'clarification_and_framing'],
                'consolidation': ['transition'],
                'transition': ['initiation', 'practical_assistance']
            }
        }
        
    def predict_next_state(
        self,
        current_type: str,
        current_stage: str,
        message_intent: Dict
    ) -> Tuple[str, str, float]:
        """Predice el siguiente estado de la conversación."""
        try:
            possible_transitions = self.transition_rules.get(current_type, {}).get(current_stage, [])
            
            if not possible_transitions:
                self.logger.warning(f"No hay transiciones definidas para {current_type}.{current_stage}")
                return current_type, 'initiation', 0.5
                
            # Analizar el intent para determinar transición
            next_state = self._analyze_intent_for_transition(
                possible_transitions,
                message_intent,
                current_type,
                current_stage
            )
            
            return next_state
            
        except Exception as e:
            self.logger.error(f"Error prediciendo siguiente estado: {str(e)}")
            return current_type, self._get_next_stage(current_stage), 0.5
            
    def _analyze_intent_for_transition(
        self,
        possible_transitions: List[str],
        intent: Dict,
        current_type: str,
        current_stage: str
    ) -> Tuple[str, str, float]:
        """Analiza el intent para determinar la mejor transición."""
        try:
            intent_type = intent.get('type', current_type)
            intent_confidence = intent.get('confidence', 0.5)
            
            # Si el intent sugiere un tipo diferente y está permitido
            if intent_type in possible_transitions:
                return intent_type, 'initiation', intent_confidence
                
            # Mantener tipo actual pero avanzar etapa
            return (
                current_type,
                self._get_next_stage(current_stage),
                0.7  # Confianza moderada en transiciones de etapa
            )
            
        except Exception as e:
            self.logger.error(f"Error analizando intent: {str(e)}")
            return current_type, self._get_next_stage(current_stage), 0.5
            
    def _get_next_stage(self, current_stage: str) -> str:
        """Determina la siguiente etapa en la secuencia natural."""
        stages = ['initiation', 'development', 'consolidation', 'transition']
        try:
            current_index = stages.index(current_stage)
            next_index = (current_index + 1) % len(stages)
            return stages[next_index]
        except ValueError:
            return 'initiation'
            
    def validate_transition(
        self,
        current_type: str,
        current_stage: str,
        proposed_type: str,
        proposed_stage: str
    ) -> Tuple[bool, float, Optional[Tuple[str, str]]]:
        """Valida si una transición propuesta es permitida."""
        try:
            # Verificar si la transición está en las reglas
            allowed_transitions = self.transition_rules.get(current_type, {}).get(current_stage, [])
            
            if proposed_type in allowed_transitions:
                return True, 0.8, None
                
            # Sugerir alternativa válida
            alternative = None
            if allowed_transitions:
                alternative = (allowed_transitions[0], 'initiation')
                
            return False, 0.3, alternative
            
        except Exception as e:
            self.logger.error(f"Error validando transición: {str(e)}")
            return False, 0.3, None
            
    def get_conversation_parameters(self, conv_type: str, stage: str) -> Dict:
        """Obtiene parámetros específicos para tipo y etapa."""
        try:
            type_config = self.types_config["tipos"].get(conv_type, {})
            stage_config = self.stages_config["stages"].get(stage, {})
            
            return {
                'system_template': type_config.get('prompts', {}).get('sistema', {}).get('base', ''),
                'focus_options': type_config.get('focus', []),
                'stage_focus': stage_config.get('focus', []),
                'max_tokens': {
                    'initiation': 100,
                    'development': 150,
                    'consolidation': 200,
                    'transition': 100
                }.get(stage, 150)
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo parámetros: {str(e)}")
            return {}