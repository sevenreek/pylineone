from django.apps import AppConfig
from utils import pull_docker_image

class CodeeditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codeedit'
    def ready(self):
        pull_docker_image()