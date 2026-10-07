import json
from pathlib import Path
from rag_system import RAGSystem

RUTA_BENCHMARK = Path("./golden_set.json")


def cargar_golden_set() -> list[dict]:
    with open(RUTA_BENCHMARK, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluar_sistema_rag():
    casos = cargar_golden_set()
    sistema = RAGSystem(top_k=5)

    resultados = []
    print("\nEvaluacion de recuperador hibrido (RAG)\n")

    for caso in casos:
        pregunta = caso["pregunta"]
        esperado = caso["documento_esperado"]

        documentos = sistema.recuperar(pregunta)
        fuentes_recuperadas = [doc.metadata.get("fuente", "") for doc in documentos]

        # Calculo de metricas
        relevante_encontrado = esperado in fuentes_recuperadas
        recall_at_5 = 1.0 if relevante_encontrado else 0.0

        aciertos = sum(1 for f in fuentes_recuperadas if f == esperado)
        precision_at_5 = aciertos / len(documentos) if documentos else 0.0

        resultados.append(
            {
                "id": caso["id"],
                "pregunta": pregunta,
                "esperado": esperado,
                "recuperados": fuentes_recuperadas,
                "recall@5": recall_at_5,
                "precision@5": precision_at_5,
            }
        )

        print(f"[{caso['id']}] Pregunta: {pregunta}")
        print(f"    - Documento esperado : {esperado}")
        print(f"    - Fuentes en Top-5   : {fuentes_recuperadas}")
        print(f"    - Recall@5           : {recall_at_5:.2f}")
        print(f"    - Precision@5        : {precision_at_5:.2f}\n")

    # Resumen promedio
    recall_medio = sum(r["recall@5"] for r in resultados) / len(resultados)
    precision_media = sum(r["precision@5"] for r in resultados) / len(resultados)

    print("Resumen de metricas:")
    print(f"Total de consultas evaluadas: {len(resultados)}")
    print(f"Mean Recall@5: {recall_medio * 100:.1f}%")
    print(f"Mean Precision@5: {precision_media * 100:.1f}%\n")

    return {
        "mean_recall@5": recall_medio,
        "mean_precision@5": precision_media,
        "detalles": resultados,
    }


if __name__ == "__main__":
    evaluar_sistema_rag()
