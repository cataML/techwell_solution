from django.apps import AppConfig


class ProdevConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prodev'

def ready(self):
        import prodev.signals