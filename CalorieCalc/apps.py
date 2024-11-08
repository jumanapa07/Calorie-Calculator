from django.apps import AppConfig


class CaloriecalcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CalorieCalc'
    def ready(self):
        import CalorieCalc.signals
