Manejo de Errores y Reintentos en Celery

1. Reintentos Automaticos con autoretry_for
Celery permite reintentar tareas ante excepciones especificas de forma automatica:
import requests
from celery.exceptions import MaxRetriesExceededError

@app.task(
    autoretry_for=(requests.RequestException, ConnectionError),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def sincronizar_pagos(pago_id: str):
    respuesta = requests.post(f"https://api.pagos.com/v1/{pago_id}/verificar", timeout=10)
    respuesta.raise_for_status()
    return respuesta.json()

- retry_backoff=True: Aplica retroceso exponencial duplicando el tiempo entre reintentos.
- retry_jitter=True: Agrega una variacion aleatoria para prevenir el problema del thundering herd.

2. Excepciones Comunes de Celery
- WorkerLostError: Se produce cuando un proceso de worker termina de forma inesperada (por ejemplo, por fallo de memoria OOM-killer del sistema operativo o corte de energia).
- SoftTimeLimitExceeded: Lanzada cuando la tarea supera el limite blando de tiempo, permitiendo capturar el error y realizar limpieza de recursos antes de que se envie la senal SIGKILL del time_limit estricto.
- MaxRetriesExceededError: Ocurre cuando se alcanza el numero maximo de intentos configurado en max_retries.
