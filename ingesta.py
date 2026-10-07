from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    PINECONE_API_KEY,
    INDEX_NAME,
    NAMESPACE,
    obtener_embeddings,
)
from setup_pinecone import inicializar_indice_pinecone

CARPETA_DATA = Path("./data")


def cargar_documentos() -> list[Document]:
    documentos = []
    for ruta_archivo in sorted(CARPETA_DATA.glob("*")):
        if ruta_archivo.suffix.lower() in [".md", ".txt"]:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            categoria = ruta_archivo.stem.replace("celery_", "")
            documentos.append(
                Document(
                    page_content=contenido,
                    metadata={
                        "fuente": ruta_archivo.name,
                        "categoria": categoria,
                    },
                )
            )
    return documentos


def fragmentar_documentos(documentos: list[Document]) -> list[Document]:
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""],
    )
    return divisor.split_documents(documentos)


def subir_a_pinecone(fragmentos: list[Document]):
    indice = inicializar_indice_pinecone()
    if indice is None:
        print("[INFO] Omitiendo subida a la nube por falta de PINECONE_API_KEY.")
        return False

    modelo_embeddings = obtener_embeddings()

    vectores = []
    print(f"Generando embeddings para {len(fragmentos)} fragmentos...")
    for indice_chunk, fragmento in enumerate(fragmentos):
        vector_emb = modelo_embeddings.embed_query(fragmento.page_content)
        identificador = f"{fragmento.metadata.get('fuente')}_{indice_chunk}"

        vectores.append(
            {
                "id": identificador,
                "values": vector_emb,
                "metadata": {
                    "text": fragmento.page_content,
                    "fuente": fragmento.metadata.get("fuente", ""),
                    "categoria": fragmento.metadata.get("categoria", ""),
                    "chunk_id": indice_chunk,
                },
            }
        )

    print(f"Insertando {len(vectores)} vectores en Pinecone (namespace='{NAMESPACE}')...")
    # Subida en lotes de 50 vectores
    tamano_lote = 50
    for i in range(0, len(vectores), tamano_lote):
        lote = vectores[i : i + tamano_lote]
        indice.upsert(vectors=lote, namespace=NAMESPACE)

    print("Ingesta en Pinecone completada exitosamente.")
    return True


def ejecutar_ingesta():
    documentos = cargar_documentos()
    print(f"Cargados {len(documentos)} documentos desde data/.")

    fragmentos = fragmentar_documentos(documentos)
    print(f"Generados {len(fragmentos)} fragmentos tras el chunking.")

    subir_a_pinecone(fragmentos)
    return fragmentos


if __name__ == "__main__":
    ejecutar_ingesta()
