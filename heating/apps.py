from django.apps import AppConfig


class HeatingConfig(AppConfig):
    name = 'heating'
    
    def ready(self):
        from heating.updater import start
        start()