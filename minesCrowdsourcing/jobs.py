from datetime import datetime
from participant.models import Task
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", hour=0)
def daily_expired_task_cleaner():
    date_of_today = datetime.date(datetime.now(pytz.timezone('America/Denver')))
    all_active_tasks = Task.objects.filter(status=Task.ACTIVE)
    for task in all_active_tasks:
        if task.status == Task.ACTIVE and task.end_date < date_of_today:
            task.status = Task.COMPLETED
            task.save()


register_events(scheduler)
scheduler.start()
