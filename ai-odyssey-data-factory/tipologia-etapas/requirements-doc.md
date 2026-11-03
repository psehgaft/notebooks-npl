# Especificación de Requerimientos
## Sistema de Generación de Conversaciones Sintéticas

### 1. Descripción General

Sistema diseñado para generar conversaciones sintéticas que simulen interacciones naturales entre usuarios y asistentes, utilizando una estructura jerárquica de contextos como guía para la generación de consultas iniciales coherentes.

### 2. Motivación

La necesidad de generar datos de entrenamiento que capturen la naturaleza orgánica de las conversaciones de asistencia, manteniendo la coherencia contextual sin sobre-estructurar las interacciones.

### 3. Requerimientos de Procesamiento de Contexto

#### 3.1 Lectura de Nodos de Contexto

El sistema debe procesar los nodos de contexto para establecer el dominio de la conversación siguiendo estos requisitos:

1. **Extracción de Ruta Contextual**
   - Identificar la ruta completa desde el nodo raíz hasta el nodo específico
   - Preservar las relaciones jerárquicas "es_parte_de"
   - Mantener los atributos específicos de cada nivel

2. **Determinación de Dominio**
   - Establecer el área general de la conversación (ej: asistencia_practica, apoyo_emocional)
   - Identificar el subdominio específico
   - Extraer los parámetros relevantes del contexto actual

3. **Mapeo de Atributos Contextuales**
   - Extraer atributos específicos del nodo actual
   - Heredar atributos relevantes de nodos superiores
   - Resolver conflictos de atributos entre niveles

### 4. Requerimientos de Procesamiento de Prompts

#### 4.1 Lectura de Nodos de Prompt de Sistema

El sistema debe generar el prompt final del asistente mediante la combinación de:

1. **Contexto General**
   - Procesar el prompt base según el tipo de conversación
   - Incorporar instrucciones generales del tipo de asistencia
   - Mantener el tono y enfoque apropiados para el dominio

2. **Contexto Particular**
   - Extraer instrucciones específicas del nodo actual
   - Incorporar parámetros contextuales relevantes
   - Adaptar el prompt según el nivel de especificidad requerido

3. **Integración de Prompts**
   - Combinar el contexto general con el particular de manera coherente
   - Priorizar instrucciones específicas sobre generales cuando sea apropiado
   - Mantener la consistencia en el tono y enfoque

### 5. Requerimientos Adicionales

#### 5.1 Verificación de Coherencia

1. **Validación de Contexto**
   - Asegurar que el contexto seleccionado es válido y completo
   - Verificar que todos los atributos requeridos están presentes
   - Validar la consistencia entre niveles jerárquicos

2. **Validación de Prompts**
   - Verificar la compatibilidad entre el contexto general y particular
   - Asegurar que las instrucciones no son contradictorias
   - Validar que el prompt final cumple con los requisitos del dominio

#### 5.2 Trazabilidad

1. **Registro de Contexto**
   - Mantener referencia a la ruta contextual utilizada
   - Registrar los atributos aplicados
   - Preservar la jerarquía de decisiones

2. **Registro de Generación de Prompts**
   - Documentar la composición del prompt final
   - Mantener referencia a las fuentes de instrucciones
   - Registrar las adaptaciones realizadas

### 6. Criterios de Aceptación

1. **Para Procesamiento de Contexto**
   - El dominio establecido debe ser coherente con la ruta jerárquica
   - Los atributos extraídos deben ser relevantes y no redundantes
   - La herencia de propiedades debe respetar la jerarquía

2. **Para Generación de Prompts**
   - El prompt final debe mantener coherencia entre contexto general y particular
   - Las instrucciones deben ser claras y no contradictorias
   - El tono y enfoque deben ser apropiados para el dominio