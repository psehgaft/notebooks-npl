import requests
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Estructura de respuesta del LLM."""
    content: str
    raw_response: Dict[str, Any]
    status: bool
    error: Optional[str] = None

class LLMService:
    """Servicio para interactuar con modelos LLM."""
    
    def __init__(self, api_url: str, api_key: str, model: str):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(__name__)
        
    def _make_request(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 150,
        stop: List[str] = None
    ) -> LLMResponse:
        """Realiza una llamada a la API del modelo."""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if stop:
                payload["stop"] = stop
                
            self.logger.debug(f"Realizando llamada LLM con temperatura {temperature}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = self._extract_content(result)
                return LLMResponse(
                    content=content,
                    raw_response=result,
                    status=True
                )
            else:
                error_msg = f"Error en API: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return LLMResponse(
                    content="",
                    raw_response={},
                    status=False,
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"Error en llamada LLM: {str(e)}"
            self.logger.error(error_msg)
            return LLMResponse(
                content="",
                raw_response={},
                status=False,
                error=error_msg
            )
            
    def _extract_content(self, api_result: Dict[str, Any]) -> str:
        """Extrae el contenido de la respuesta del API."""
        if not api_result or 'choices' not in api_result:
            return ""
            
        choice = api_result['choices'][0]
        if 'text' in choice:
            return choice['text'].strip()
        elif 'message' in choice:
            return choice['message'].get('content', '').strip()
            
        return ""
        
    def generate_conversation(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 150
    ) -> LLMResponse:
        """Genera una respuesta conversacional."""
        return self._make_request(
            prompt=f"{system_prompt}\n\nUser: {user_prompt}",
            temperature=temperature,
            max_tokens=max_tokens,
            stop=["User:", "\n\n"]
        )
        
    def classify_message(
        self,
        message: str,
        possible_types: List[str],
        possible_stages: List[str]
    ) -> LLMResponse:
        """Clasifica un mensaje según tipo y etapa."""
        classification_prompt = f"""
        Classify the following message according to type and stage.

        Message: {message}

        Valid types: {', '.join(possible_types)}
        Valid stages: {', '.join(possible_stages)}

        Respond ONLY with a JSON object containing type and stage.
        Example: {{"type": "informative_analytical", "stage": "development"}}
        """
        
        return self._make_request(
            prompt=classification_prompt,
            temperature=0.3,
            max_tokens=30,
            stop=["\n", "}"] + ["}}" if not classification_prompt.endswith("}}") else ""]
        )