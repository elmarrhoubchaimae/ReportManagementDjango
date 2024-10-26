from django.apps import AppConfig

class ProjectRegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_register'

    def ready(self):
        import project_register.signals
