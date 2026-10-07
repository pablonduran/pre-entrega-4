Definicion y Ejecucion de Tareas en Celery

1. Creacion de Tareas con Decorador
Las tareas se declaran decorando funciones de Python con @app.task:
from celery import Celery

app = Celery("sistema_envios", broker="redis://localhost:6379/0")

@app.task(bind=True, name="enviar_notificacion")
def enviar_notificacion(self, usuario_id: int, mensaje: str):
    print(f"Enviando mensaje a {usuario_id}: {mensaje}")
    return {"status": "enviado", "id": self.request.id}

2. Invocacion: delay vs apply_async
Existen dos formas principales de encolar una tarea:
- tarea.delay(args, kwargs): Acceso directo y simplificado para enviar la tarea inmediatamente a la cola predeterminada.
- tarea.apply_async(args, kwargs, ...): Permite control avanzado de ejecucion mediante opciones adicionales:
  - countdown: Demora la ejecucion en una cantidad determinada de segundos (ejemplo: countdown=60 ejecuta en 1 minuto).
  - eta: Recibe un objeto datetime con la hora exacta en la que el worker debe procesar la tarea.
  - queue: Permite enrutar la tarea a una cola especifica como cola_alta_prioridad.

Ejemplo con apply_async:
enviar_notificacion.apply_async(
    args=[1045, "Tu pedido esta en camino"],
    countdown=120,
    queue="prioridad_alta"
)
