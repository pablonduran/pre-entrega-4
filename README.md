# Pre-entrega 4 — Sistema RAG Escalable en la Nube con Pinecone

Módulo de recuperación híbrida (BM25 + búsqueda vectorial) sobre un índice Serverless en Pinecone con evaluación formal de métricas (Recall@5 y Precision@5).

## Requisitos

- Python 3.12 o superior
- API Key de Pinecone (cuenta gratuita en [pinecone.io](https://www.pinecone.io))
- API Key de OpenAI o Google Gemini para embeddings

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\Activate.ps1
# En Linux / Mac:
# source .venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear archivo `.env` basándose en `.env.example`:
```env
PINECONE_API_KEY=tu_pinecone_api_key_aqui
INDEX_NAME=documentos-tecnicos
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
NAMESPACE=produccion

# Embeddings:
LLM_PROVIDER=openai
OPENAI_API_KEY=tu_openai_api_key_aqui
EMBEDDING_MODEL=text-embedding-3-small
```

## Pasos para replicar el índice en Pinecone

### Opción A (Automática mediante script):
Ejecutar el script de setup que verifica si el índice existe y lo crea automáticamente en modo Serverless:
```bash
python setup_pinecone.py
```

### Opción B (Desde la consola de Pinecone):
1. Iniciar sesión en [Pinecone Console](https://app.pinecone.io).
2. Click en **Create Index**.
3. **Index Name:** `documentos-tecnicos`
4. **Dimensions:** `1536` (para `text-embedding-3-small`) o `3072` (para `gemini-embedding-001`).
5. **Metric:** `cosine`.
6. **Capacity Mode:** `Serverless` (Cloud: `AWS`, Region: `us-east-1`).
7. Click en **Create Index**.

## Ingesta de documentos

Procesa los archivos técnicos de `data/`, aplica chunking con `RecursiveCharacterTextSplitter` y sube los vectores con metadatos (texto, fuente, categoría) a Pinecone:
```bash
python ingesta.py
```

## Evaluación de métricas

Ejecuta el benchmark de 5 preguntas sobre el Golden Set calculando Recall@5 y Precision@5 con el recuperador híbrido:
```bash
python evaluate.py
```

## Resumen de resultados de evaluación

Ejemplo de salida obtenida sobre el Golden Set:

```text
Resumen de metricas:
Total de consultas evaluadas: 5
Mean Recall@5: 100.0%
Mean Precision@5: 36.0%
```

- **Recall@5 (100%):** En el 100% de las consultas, el documento técnico relevante fue recuperado dentro del Top-5.
- **Precision@5 (36%):** De los 5 fragmentos recuperados en cada consulta, el 36% corresponde directamente a la fuente primaria de la respuesta, demostrando alta concentración semántica sin saturar el contexto.
