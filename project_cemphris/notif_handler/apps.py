from django.apps import AppConfig


class NotifHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notif_handler'
    def ready(self):
        import notif_handler.tasks
        import notif_handler.signals