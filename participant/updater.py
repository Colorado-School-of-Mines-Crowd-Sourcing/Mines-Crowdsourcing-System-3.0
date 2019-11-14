from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz


def daily_expired_task_cleaner():
    date_of_today = datetime.date(datetime.now(pytz.timezone('America/Denver')))
    try:
        from participant.models import Task
        all_active_tasks = Task.objects.filter(status=Task.ACTIVE)
        for task in all_active_tasks:
            if task.end_date < date_of_today:
                task.status = Task.COMPLETED
                task.save()
    except:
        pass


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_expired_task_cleaner, 'interval', hours=24)
    scheduler.start()
