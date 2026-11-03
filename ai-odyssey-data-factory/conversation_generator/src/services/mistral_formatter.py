import logging
from typing import List, Dict, Any

class MistralFormatter:
    """Formateador especializado para prompts de Mistral."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.language_instruction = """
        A partir de este momento, asume el papel de un asistente con dominio perfecto 
        del español. Todas tus respuestas deben estar en español, utilizando vocabulario,
        expresiones y estructuras gramaticales propias del idioma. Adapta tu estilo según
        el contexto, manteniendo la coherencia lingüística y cultural en todas tus
        interacciones.
        """.strip()
        
    def format_system_instruction(self, base_instruction: str, personality_config: str) -> str:
        """Formatea la instrucción del sistema."""
        return f"<s>[INST] {self.language_instruction}\n{base_instruction} {personality_config} [/INST]"
        
    def format_user_message(self, message: str, is_first: bool = False) -> str:
        """Formatea un mensaje del usuario."""
        reminder = " Recuerda mantener todas tus respuestas en español." if not is_first else ""
        return f"[INST]{message}{reminder}[/INST]"
        
    def format_assistant_response(self, response: str, is_first: bool = False) -> str:
        """Formatea una respuesta del asistente."""
        suffix = " </s>" if is_first else ""
        return f"{response}{suffix}"
        
    def format_conversation_history(
        self,
        messages: List[Dict[str, str]],
        personality_config: str
    ) -> str:
        """Formatea el historial completo de una conversación."""
        formatted_prompt = ""
        
        # Formatear instrucciones del sistema si existen
        system_messages = [m for m in messages if m["role"] == "system"]
        if system_messages:
            formatted_prompt = self.format_system_instruction(
                system_messages[0]["content"],
                personality_config
            )
            
        # Formatear el primer intercambio usuario-asistente
        user_messages = [m for m in messages if m["role"] == "user"]
        assistant_messages = [m for m in messages if m["role"] == "assistant"]
        
        if user_messages and assistant_messages:
            formatted_prompt += self.format_user_message(
                user_messages[0]["content"],
                is_first=True
            )
            formatted_prompt += self.format_assistant_response(
                assistant_messages[0]["content"],
                is_first=True
            )
            
        # Formatear el resto de la conversación
        for user_msg, asst_msg in zip(
            user_messages[1:],
            assistant_messages[1:]
        ):
            formatted_prompt += self.format_user_message(user_msg["content"])
            formatted_prompt += self.format_assistant_response(asst_msg["content"])
            
        return formatted_prompt
        
    def format_classification_prompt(
        self,
        message: str,
        valid_types: List[str],
        valid_stages: List[str]
    ) -> str:
        """Formatea un prompt para clasificación."""
        return f"""<s>[INST]
        Clasifica el siguiente mensaje según su tipo y etapa.
        
        MENSAJE: {message}
        
        TIPOS VÁLIDOS: {', '.join(valid_types)}
        ETAPAS VÁLIDAS: {', '.join(valid_stages)}
        
        FORMATO REQUERIDO: JSON con 'type' y 'stage'
        EJEMPLO: {{"type": "informative_analytical", "stage": "development"}}
        [/INST]"""
        
    def clean_response(self, text: str) -> str:
        """Limpia y formatea una respuesta."""
        if not text:
            return ""
            
        # Eliminar tags de instrucción
        text = text.replace("[INST]", "").replace("[/INST]", "")
        
        # Eliminar tags de sistema
        text = text.replace("<s>", "").replace("</s>", "")
        
        # Limpiar espacios extra
        text = " ".join(text.split())
        
        return text.strip()