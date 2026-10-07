from typing import Any
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_community.retrievers import BM25Retriever
from pinecone import Pinecone

try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    from langchain_classic.retrievers import EnsembleRetriever

from config import (
    PINECONE_API_KEY,
    INDEX_NAME,
    NAMESPACE,
    obtener_embeddings,
)
from ingesta import cargar_documentos, fragmentar_documentos


class RecuperadorPinecone(BaseRetriever):
    indice: Any
    embeddings: Any
    top_k: int = 5
    namespace: str = ""

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        vector_consulta = self.embeddings.embed_query(query)
        respuesta = self.indice.query(
            vector=vector_consulta,
            top_k=self.top_k,
            include_metadata=True,
            namespace=self.namespace,
        )

        documentos = []
        for coincidencia in respuesta.get("matches", []):
            metadatos = coincidencia.get("metadata", {}).copy()
            contenido = metadatos.pop("text", "")
            documentos.append(Document(page_content=contenido, metadata=metadatos))
        return documentos


class RecuperadorLocalFallback(BaseRetriever):
    fragmentos: list[Document]
    top_k: int = 5

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        palabras_clave = query.lower().split()
        puntuados = []
        for doc in self.fragmentos:
            texto = doc.page_content.lower()
            puntos = sum(1 for palabra in palabras_clave if palabra in texto)
            puntuados.append((puntos, doc))
        puntuados.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in puntuados[: self.top_k]]


class RAGSystem:
    def __init__(self, fragmentos: list[Document] | None = None, top_k: int = 5):
        self.top_k = top_k

        if fragmentos is None:
            documentos = cargar_documentos()
            fragmentos = fragmentar_documentos(documentos)
        self.fragmentos = fragmentos

        # 1. Recuperador lexico (BM25)
        self.recuperador_bm25 = BM25Retriever.from_documents(self.fragmentos)
        self.recuperador_bm25.k = top_k

        # 2. Recuperador vectorial (Pinecone o fallback local si no hay clave)
        self.modelo_embeddings = obtener_embeddings()
        self.recuperador_vectorial = self._inicializar_recuperador_vectorial()

        # 3. Recuperador hibrido (EnsembleRetriever combinando lexico y semantico)
        self.recuperador_hibrido = EnsembleRetriever(
            retrievers=[self.recuperador_bm25, self.recuperador_vectorial],
            weights=[0.5, 0.5],
        )

    def _inicializar_recuperador_vectorial(self) -> BaseRetriever:
        if PINECONE_API_KEY and not PINECONE_API_KEY.startswith("tu_"):
            try:
                cliente = Pinecone(api_key=PINECONE_API_KEY)
                indice = cliente.Index(INDEX_NAME)
                return RecuperadorPinecone(
                    indice=indice,
                    embeddings=self.modelo_embeddings,
                    top_k=self.top_k,
                    namespace=NAMESPACE,
                )
            except Exception as e:
                print(f"[AVISO] No se pudo conectar a Pinecone ({e}). Usando recuperador local de respaldo.")

        return RecuperadorLocalFallback(fragmentos=self.fragmentos, top_k=self.top_k)

    def recuperar(self, consulta: str) -> list[Document]:
        documentos = self.recuperador_hibrido.invoke(consulta)
        return documentos[: self.top_k]

    def get_top_5_documents(self, query: str) -> list[Document]:
        return self.recuperar(query)
