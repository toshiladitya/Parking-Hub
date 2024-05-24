import os
import environ

environ.Env.read_env()
broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')

database_engine_options = {'echo': True},
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['application/json']
timezone = 'UTC'
enable_utc = True
