Configuracion de Celery

1. Broker y Backend de Resultados
Celery requiere un intermediario de mensajes (broker) para enviar y recibir mensajes de tareas entre la aplicacion y los workers.
- Broker recomendado para produccion: RabbitMQ (amqp://usuario:password@localhost:5672//).
- Broker alternativo para desarrollo y pruebas: Redis (redis://localhost:6379/0).

Para almacenar el estado y los valores de retorno de las tareas, se configura el parametro result_backend:
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

2. Serializacion y Seguridad
Por razones de seguridad, se debe evitar pickle en entornos de produccion y utilizar serializacion JSON estricta:
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "America/Argentina/Buenos_Aires"
enable_utc = True

3. Garantias de Entrega (Acks Late)
Por defecto, Celery reconoce el mensaje (ack) inmediatamente antes de ejecutar la tarea. Si el worker cae durante la ejecucion, la tarea se pierde.
Para evitar la perdida de tareas criticas, se activa el reconocimiento tardio:
task_acks_late = True
task_reject_on_worker_lost = True

Con task_acks_late = True, el mensaje se confirma solo despues de que la funcion finaliza con exito.
