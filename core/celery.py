from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkinghub_server.settings')
app = Celery('core', include=['core.tasks'])

app.config_from_object('parkinghub_server.celeryconfig')

# Optional configuration, see the application user guide.
app.conf.update(
  result_expires=3600,
)

if __name__ == '__main__':
    app.start()
