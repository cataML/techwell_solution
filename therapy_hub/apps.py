from django.apps import AppConfig


class TherapyHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'therapy_hub'

def ready(self):
    import therapy_hub.signals