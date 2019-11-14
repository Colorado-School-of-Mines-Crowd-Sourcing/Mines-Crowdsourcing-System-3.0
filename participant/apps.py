from django.apps import AppConfig
from participant import updater


class ParticipantConfig(AppConfig):
    name = 'participant'
    verbose_name = 'Tasks'

    def ready(self):
        updater.start()
