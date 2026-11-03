# Proyecto: Generador de Conversaciones con Gobierno Conversacional

## Contexto Actual
Estamos trabajando en un generador de conversaciones en español que utiliza el modelo Mistral. Acabamos de implementar mejoras en:
- Separación de llamadas LLM para conversación y clasificación
- Sistema de logging mejorado
- Manejo de errores más robusto

## Objetivo Actual
Implementar un sistema de gobierno conversacional que:
1. Defina rutas predeterminadas para las conversaciones
2. Use la clasificación LLM como validación, no como decisor principal
3. Mantenga la coherencia y naturalidad del diálogo

## Componentes Principales
1. Tipos de Conversación:
   - clarification_and_framing
   - structured_emotional_support
   - informative_analytical
   - practical_assistance

2. Etapas de Conversación:
   - initiation
   - development
   - consolidation
   - transition

## Formato de Trabajo
Al discutir cambios o mejoras:
1. Identificar el componente específico a mejorar
2. Mostrar el código actual relevante
3. Proponer mejoras específicas
4. Implementar y validar

## Reglas de Revisión
Al revisar código:
1. Verificar manejo de errores
2. Validar logging apropiado
3. Comprobar coherencia con el sistema de gobierno
4. Asegurar calidad de documentación

## Guidelines de Implementación
1. Mantener separación clara de responsabilidades
2. Priorizar legibilidad y mantenibilidad
3. Documentar decisiones de diseño importantes
4. Incluir ejemplos de uso cuando sea relevante

## Formato para Reportar Problemas
1. Descripción del problema
2. Código o logs relevantes
3. Comportamiento esperado vs actual
4. Impacto en el sistema de gobierno

## Áreas de Enfoque
1. Sistema de gobierno conversacional
2. Validación de rutas de conversación
3. Integración con sistema existente
4. Métricas y monitoreo