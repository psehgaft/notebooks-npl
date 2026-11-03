import json
from pathlib import Path
from typing import Dict, Any
import logging

class ConfigLoader:
    """Cargador de configuraciones con validación integrada."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger(__name__)
        
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Directorio de configuración no encontrado: {config_dir}")
            
    def load_config(self, filename: str) -> Dict[str, Any]:
        """Carga un archivo de configuración JSON."""
        try:
            config_path = self.config_dir / filename
            self.logger.info(f"Cargando configuración desde: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            self.logger.debug(f"Configuración cargada: {json.dumps(config, indent=2)}")
            return config
            
        except Exception as e:
            self.logger.error(f"Error al cargar configuración {filename}: {str(e)}")
            raise

    def validate_types_config(self, config: Dict[str, Any]) -> bool:
        """Valida la configuración de tipos de conversación."""
        try:
            if 'tipos' not in config:
                raise ValueError("Sección 'tipos' no encontrada en configuración")
                
            for tipo_name, tipo_config in config['tipos'].items():
                if 'contexto' not in tipo_config:
                    raise ValueError(f"Contexto no encontrado en tipo: {tipo_name}")
                    
                if 'prompts' not in tipo_config:
                    raise ValueError(f"Prompts no encontrados en tipo: {tipo_name}")
                    
                # Validar estructura de prompts
                prompts = tipo_config['prompts']
                if not all(k in prompts for k in ['sistema', 'usuario']):
                    raise ValueError(f"Estructura de prompts incompleta en tipo: {tipo_name}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error en validación de tipos: {str(e)}")
            return False

    def validate_stages_config(self, config: Dict[str, Any]) -> bool:
        """Valida la configuración de etapas de conversación."""
        try:
            if 'stages' not in config:
                raise ValueError("Sección 'stages' no encontrada en configuración")
                
            required_fields = ['system', 'user', 'focus']
            for stage_name, stage_config in config['stages'].items():
                for field in required_fields:
                    if field not in stage_config:
                        raise ValueError(f"Campo {field} no encontrado en stage: {stage_name}")
                        
            return True
            
        except Exception as e:
            self.logger.error(f"Error en validación de stages: {str(e)}")
            return False

    def validate_global_params(self, config: Dict[str, Any]) -> bool:
        """Valida los parámetros globales."""
        try:
            required_fields = ['moods', 'personalities', 'response_config']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Campo requerido no encontrado: {field}")
                    
            if not isinstance(config['moods'], list) or not isinstance(config['personalities'], list):
                raise ValueError("moods y personalities deben ser listas")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error en validación de parámetros globales: {str(e)}")
            return False

    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Carga y valida todas las configuraciones necesarias."""
        configs = {
            'types': self.load_config('conversation_types.json'),
            'stages': self.load_config('conversation_stages.json'),
            'global': self.load_config('global_parameters.json')
        }
        
        # Validar todas las configuraciones
        validations = {
            'types': self.validate_types_config(configs['types']),
            'stages': self.validate_stages_config(configs['stages']),
            'global': self.validate_global_params(configs['global'])
        }
        
        if not all(validations.values()):
            raise ValueError("Error en validación de configuraciones")
            
        return configs