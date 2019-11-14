from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from participant.models import Task


def myjob():
    print("Daily expired job clean up")
    current_time = datetime.now(pytz.timezone('America/Denver'))
    print("time now: ", current_time)



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(myjob, 'interval', seconds=10)
    scheduler.start()
