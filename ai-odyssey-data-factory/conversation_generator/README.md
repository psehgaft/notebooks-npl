# Generador de Conversaciones con Gobierno Conversacional

Este proyecto implementa un generador de conversaciones sintéticas con un sistema de gobierno conversacional integrado.

## Instalación

```bash
# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar el paquete en modo desarrollo
pip install -e .
```

## Estructura del Proyecto

```
conversation_generator/
├── config/                 # Configuraciones JSON
├── logs/                  # Directorio para logs
├── generated/            # Archivos generados
├── src/                 # Código fuente
│   ├── core/          # Núcleo del generador
│   ├── domain/       # Lógica de dominio
│   ├── services/    # Servicios y procesamiento
│   └── utils/      # Utilidades
├── notebooks/     # Jupyter notebooks
└── tests/       # Tests unitarios
```

## Uso Básico

```python
from src.core.conversation_generator import ConversationGenerator

# Inicializar generador
generator = ConversationGenerator(
    model="mistral-7b-instruct",
    api_url="tu-url-api",
    api_key="tu-api-key",
    debug=True
)

# Generar una conversación
conversation_data = generator.generate_natural_conversation(num_turns=3)

# Generar un dataset
df = generator.generate_dataset(num_conversations=2)
```

## Configuración

El proyecto requiere archivos de configuración JSON en el directorio `config/`:
- conversation_types.json
- conversation_stages.json
- global_parameters.json

## Desarrollo

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz tus cambios y commits
4. Push a tu fork
5. Crea un Pull Request