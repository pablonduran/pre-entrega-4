from pinecone import Pinecone, ServerlessSpec
from config import (
    PINECONE_API_KEY,
    INDEX_NAME,
    PINECONE_CLOUD,
    PINECONE_REGION,
    obtener_dimension_embeddings,
)


def inicializar_indice_pinecone():
    if not PINECONE_API_KEY or PINECONE_API_KEY.startswith("tu_"):
        print("[AVISO] Configura tu PINECONE_API_KEY en el archivo .env para interactuar con la nube.")
        return None

    cliente = Pinecone(api_key=PINECONE_API_KEY)
    dimension = obtener_dimension_embeddings()

    print(f"Verificando indice '{INDEX_NAME}' en Pinecone...")
    if not cliente.has_index(INDEX_NAME):
        print(
            f"El indice '{INDEX_NAME}' no existe. "
            f"Creando indice Serverless ({PINECONE_CLOUD}/{PINECONE_REGION}) con dimension {dimension}..."
        )
        cliente.create_index(
            name=INDEX_NAME,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )
        print(f"Indice '{INDEX_NAME}' creado exitosamente.")
    else:
        print(f"El indice '{INDEX_NAME}' ya existe y esta listo.")

    return cliente.Index(INDEX_NAME)


if __name__ == "__main__":
    inicializar_indice_pinecone()
