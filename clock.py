from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=20)
def timed_job():
    requests.get("https://infection-data.herokuapp.com/")
    print('Sent the request to the route')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    requests.get("https://infection-data.herokuapp.com/")
    print('This job is run every weekday at 5pm.')

sched.start()