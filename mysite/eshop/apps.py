from django.apps import AppConfig

class EshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eshop'

    def ready(self):
        from .signals import create_profile, save_profile, payment_notification
