Monitoreo de Celery con Flower

1. Que es Flower y Como Iniciar
Flower es una herramienta web de administracion y observabilidad en tiempo real para clusters de Celery.
Permite visualizar workers activos, estado de tareas, historicos de fallos y tasas de ejecucion.

Comando de inicio en terminal:
celery -A sistema_envios flower --port=5555 --basic_auth=admin:ClaveSegura2026

La interfaz web se expone en el puerto 5555 (http://localhost:5555).

2. Metricas y Funcionalidades Principales
- Dashboard en tiempo real: Muestra el numero de workers en linea, tareas ejecutandose actualmente y tareas encoladas.
- Detalle de tareas: Graficos de latencia, argumentos pasados a la tarea, excepciones capturadas con su stacktrace completo y duracion de ejecucion.
- Control remoto de workers:
  - Cancelar tareas en ejecucion (revoke).
  - Ajustar el nivel de concurrencia de workers en caliente sin reiniciar el proceso.
  - Habilitar o deshabilitar eventos de monitoreo.
- Alertas y Webhooks: Envio de notificaciones HTTP automáticas cuando la tasa de fallos supera un umbral configurado.
