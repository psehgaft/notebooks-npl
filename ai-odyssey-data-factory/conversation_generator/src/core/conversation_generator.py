import logging
import random
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from tqdm import tqdm

from conversation_generator.src.utils.logger import LoggerFactory
from conversation_generator.src.utils.config_loader import ConfigLoader
from conversation_generator.src.services.llm_service import LLMService
from conversation_generator.src.services.mistral_formatter import MistralFormatter
from conversation_generator.src.services.prompt_manager import PromptManager, PromptContext
from conversation_generator.src.domain.conversation_governance import ConversationGovernance
from conversation_generator.src.domain.conversation_types import ConversationTypeManager
from conversation_generator.src.domain.conversation_stages import ConversationStageManager

@dataclass
class ConversationTurn:
    """Representa un turno en la conversación."""
    message: str
    role: str
    type: str
    stage: str
    conversation_id: int
    message_id: int

class ConversationGenerator:
    """Generador principal de conversaciones."""
    
    def __init__(
        self,
        model: str,
        api_url: str,
        api_key: str,
        config_dir: str = "config",
        debug: bool = False
    ):
        # Inicializar componentes base
        self.logger_factory = LoggerFactory(debug=debug)
        self.logger = self.logger_factory.create_logger("generator", "generator.log")
        self.conversation_logger = self.logger_factory.create_conversation_logger()
        self.classification_logger = self.logger_factory.create_classification_logger()
        
        # Cargar configuraciones
        self.config_loader = ConfigLoader(config_dir)
        self.configs = self.config_loader.load_all_configs()
        
        # Inicializar servicios
        self.llm_service = LLMService(api_url, api_key, model)
        self.mistral_formatter = MistralFormatter()
        self.prompt_manager = PromptManager(
            self.configs['types'],
            self.configs['stages']
        )
        
        # Inicializar componentes de dominio
        self.type_manager = ConversationTypeManager(self.configs['types'])
        self.stage_manager = ConversationStageManager(self.configs['stages'])
        self.governance = ConversationGovernance(
            self.configs['types'],
            self.configs['stages']
        )
        
        # Estado de la conversación
        self.conversation_history = []
        self.current_context = None
        
        self.logger.info(f"ConversationGenerator inicializado con modelo: {model}")
        
    def set_initial_domain(self) -> Optional[PromptContext]:
        """Establece el dominio inicial de la conversación."""
        try:
            # Seleccionar tipo aleatorio
            conv_type = random.choice(self.type_manager.get_valid_types())
            
            # Obtener contexto aleatorio para el tipo
            context = self.type_manager.get_random_context(conv_type)
            if not context:
                raise ValueError(f"No se pudo obtener contexto para tipo: {conv_type}")
                
            # Seleccionar mood y personality
            mood = random.choice(self.configs['global']['moods'])
            personality = random.choice(self.configs['global']['personalities'])
            
            self.current_context = PromptContext(
                conv_type=conv_type,
                stage='initiation',
                mood=mood,
                personality=personality,
                method=context['method'],
                area=context['area'],
                specific_topic=context['topic'],
                attributes={'category': context['category']}
            )
            
            return self.current_context
            
        except Exception as e:
            self.logger.error(f"Error estableciendo dominio inicial: {str(e)}")
            return None
            
    def generate_conversation_turn(
        self,
        user_message: str,
        conv_type: str,
        stage: str
    ) -> Optional[str]:
        """Genera un turno de conversación."""
        try:
            # Validar tipo y etapa
            if not self.type_manager.get_type(conv_type):
                raise ValueError(f"Tipo de conversación inválido: {conv_type}")
            if not self.stage_manager.get_stage(stage):
                raise ValueError(f"Etapa de conversación inválida: {stage}")
                
            # Generar prompt del sistema
            system_prompt = self.prompt_manager.generate_system_prompt(self.current_context)
            if not system_prompt:
                raise ValueError("No se pudo generar prompt del sistema")
                
            # Formatear prompts con Mistral
            formatted_prompt = self.mistral_formatter.format_conversation_history(
                [
                    {"role": "system", "content": system_prompt},
                    *self.conversation_history,
                    {"role": "user", "content": user_message}
                ],
                f"{self.current_context.mood}{self.current_context.personality}"
            )
            
            # Obtener parámetros de la etapa
            stage_params = self.stage_manager.get_stage_parameters(stage)
            
            # Llamar al LLM
            response = self.llm_service.generate_conversation(
                system_prompt=system_prompt,
                user_prompt=user_message,
                temperature=0.7,
                max_tokens=stage_params['max_tokens']
            )
            
            if not response.status:
                raise ValueError(f"Error en llamada LLM: {response.error}")
                
            # Logging
            self.conversation_logger.info(
                "",
                extra={
                    "system_prompt": system_prompt,
                    "user_prompt": user_message,
                    "response": response.content
                }
            )
            
            return response.content
            
        except Exception as e:
            self.logger.error(f"Error generando turno de conversación: {str(e)}")
            return None
            
    def determine_message_type_and_stage(
        self,
        message: str,
        previous_stage: Optional[str] = None
    ) -> tuple[str, str]:
        """Determina el tipo y etapa del mensaje."""
        try:
            # Clasificar mensaje
            classification = self.llm_service.classify_message(
                message=message,
                possible_types=self.type_manager.get_valid_types(),
                possible_stages=self.stage_manager.get_valid_stages()
            )
            
            if not classification.status:
                raise ValueError(f"Error en clasificación: {classification.error}")
                
            # Logging de clasificación
            self.classification_logger.info(
                "",
                extra={
                    "input_text": message,
                    "result": classification.content
                }
            )
            
            # Validar y determinar siguiente estado
            current_type = self.current_context.conv_type if self.current_context else "clarification_and_framing"
            current_stage = previous_stage or "initiation"
            
            next_type, next_stage, confidence = self.governance.predict_next_state(
                current_type,
                current_stage,
                {"type": classification.content, "confidence": 0.7}
            )
            
            return next_type, next_stage
            
        except Exception as e:
            self.logger.error(f"Error determinando tipo y etapa: {str(e)}")
            return (
                self.current_context.conv_type if self.current_context else "clarification_and_framing",
                self.stage_manager.get_next_stage(previous_stage or "initiation")
            )
            
    def generate_natural_conversation(self, num_turns: int = 5) -> Dict[str, List]:
        """Genera una conversación natural completa."""
        self.logger.info(f"Generando conversación natural de {num_turns} turnos")
        
        conversation_data = {
            "messages": [],
            "types": [],
            "stages": [],
            "message_lengths": []
        }
        
        try:
            # Establecer dominio inicial
            if not self.set_initial_domain():
                raise ValueError("No se pudo establecer dominio inicial")
                
            # Generar mensaje inicial
            user_message = self.prompt_manager.generate_initial_prompt(self.current_context)
            prev_stage = None
            
            for turn in range(num_turns):
                self.logger.info(f"Generando turno {turn + 1}/{num_turns}")
                
                # Determinar tipo y etapa
                conv_type, stage = self.determine_message_type_and_stage(user_message, prev_stage)
                
                # Generar respuesta
                assistant_response = self.generate_conversation_turn(
                    user_message,
                    conv_type,
                    stage
                )
                
                if not assistant_response:
                    raise ValueError("No se pudo generar respuesta")
                    
                # Actualizar datos de la conversación
                conversation_data["messages"].extend([user_message, assistant_response])
                conversation_data["types"].extend([conv_type, conv_type])
                conversation_data["stages"].extend([stage, stage])
                conversation_data["message_lengths"].extend([
                    len(user_message),
                    len(assistant_response)
                ])
                
                # Actualizar historial
                self.conversation_history.extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_response}
                ])
                
                # Generar siguiente mensaje del usuario
                user_message = self.prompt_manager.generate_next_user_prompt(
                    self.current_context,
                    self.conversation_history
                )
                
                prev_stage = stage
                
            return conversation_data
            
        except Exception as e:
            self.logger.error(f"Error generando conversación natural: {str(e)}")
            return conversation_data
            
    def generate_dataset(self, num_conversations: int = 1) -> pd.DataFrame:
        """Genera un dataset de conversaciones."""
        self.logger.info(f"Generando dataset con {num_conversations} conversaciones")
        
        all_data = {
            "message": [],
            "conversation_id": [],
            "message_id": [],
            "role": [],
            "type": [],
            "stage": []
        }
        
        for conv_id in tqdm(range(num_conversations)):
            self.logger.info(f"Generando conversación {conv_id + 1}/{num_conversations}")
            self.conversation_history = []
            
            try:
                conv_data = self.generate_natural_conversation()
                
                for msg_id, (message, type_, stage_) in enumerate(zip(
                    conv_data["messages"],
                    conv_data["types"],
                    conv_data["stages"]
                )):
                    all_data["message"].append(message)
                    all_data["conversation_id"].append(conv_id)
                    all_data["message_id"].append(msg_id)
                    all_data["role"].append("user" if msg_id % 2 == 0 else "assistant")
                    all_data["type"].append(type_)
                    all_data["stage"].append(stage_)
                    
            except Exception as e:
                self.logger.error(f"Error en conversación {conv_id}: {str(e)}")
                continue
                
        return pd.DataFrame(all_data)