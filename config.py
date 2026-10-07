import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Claves de API
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configuracion de Pinecone
INDEX_NAME = os.getenv("INDEX_NAME", "documentos-tecnicos")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
NAMESPACE = os.getenv("NAMESPACE", "produccion")

# Proveedor de embeddings
PROVEEDOR_EMBEDDINGS = os.getenv("LLM_PROVIDER", "openai").lower()


def obtener_dimension_embeddings() -> int:
    dim_env = os.getenv("EMBEDDING_DIMENSION")
    if dim_env:
        return int(dim_env)
    if PROVEEDOR_EMBEDDINGS == "gemini":
        return 3072
    return 1536


def obtener_embeddings():
    if PROVEEDOR_EMBEDDINGS == "gemini" and GEMINI_API_KEY:
        return OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "gemini-embedding-001"),
            openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
            openai_api_key=GEMINI_API_KEY,
            check_embedding_ctx_length=False,
        )

    # Por defecto usa OpenAI text-embedding-3-small (1536 dimensiones)
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        api_key=OPENAI_API_KEY or "dummy_key",
    )
