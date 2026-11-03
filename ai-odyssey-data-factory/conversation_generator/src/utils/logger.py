import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class LoggerFactory:
    """Fábrica para crear y configurar loggers específicos."""
    
    def __init__(self, logs_dir: str = "logs", debug: bool = False):
        self.logs_dir = Path(logs_dir)
        self.debug_mode = debug
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar formato base
        self.base_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _create_rotating_handler(self, filename: str, formatter: logging.Formatter) -> RotatingFileHandler:
        """Crea un handler rotativo para los archivos de log."""
        handler = RotatingFileHandler(
            self.logs_dir / filename,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        handler.setFormatter(formatter)
        return handler

    def create_logger(self, name: str, log_file: str) -> logging.Logger:
        """Crea un logger con configuración básica."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # Limpiar handlers existentes
        if logger.hasHandlers():
            logger.handlers.clear()
            
        # Agregar handler de archivo
        file_handler = self._create_rotating_handler(log_file, self.base_formatter)
        logger.addHandler(file_handler)
        
        return logger
        
    def create_conversation_logger(self) -> logging.Logger:
        """Crea un logger especializado para conversaciones."""
        logger = logging.getLogger('conversation')
        logger.setLevel(logging.DEBUG)
        
        if logger.hasHandlers():
            logger.handlers.clear()
            
        conversation_formatter = logging.Formatter(
            '%(asctime)s\nCONVERSATION:\nSystem: %(system_prompt)s\n'
            'User: %(user_prompt)s\nResponse: %(response)s\n' + '-'*80
        )
        
        handler = self._create_rotating_handler('conversation.log', conversation_formatter)
        logger.addHandler(handler)
        
        return logger
        
    def create_classification_logger(self) -> logging.Logger:
        """Crea un logger especializado para clasificaciones."""
        logger = logging.getLogger('classification')
        logger.setLevel(logging.DEBUG)
        
        if logger.hasHandlers():
            logger.handlers.clear()
            
        classification_formatter = logging.Formatter(
            '%(asctime)s\nCLASSIFICATION:\nInput: %(input_text)s\n'
            'Result: %(result)s\n' + '-'*80
        )
        
        handler = self._create_rotating_handler('classification.log', classification_formatter)
        logger.addHandler(handler)
        
        return logger