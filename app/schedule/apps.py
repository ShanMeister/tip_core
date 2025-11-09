from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schedule'

    def ready(self):
        from schedule.connector_enricher_schedule import start_schedule_task
        start_schedule_task()
