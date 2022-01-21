from django.apps import AppConfig
from utils import pull_docker_image
import os

class CodeeditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codeedit'
    def ready(self):
        if(os.environ.get('RUN_MAIN', None) != 'true'):
            pull_docker_image()