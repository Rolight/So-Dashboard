from django.apps import AppConfig


class SoConfig(AppConfig):
    name = 'so'

    def ready(self):
        from so.connector import signal_register
        signal_register()
