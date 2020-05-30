from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=20)
def timed_job():
    data = requests.get("https://infection-data.herokuapp.com/")
    stateList = json.loads(data.content.decode("utf-8"))
    state = stateList.form["state"]
    positive = stateList.form["positive"]
    negative = stateList.form["negative"]
    pending = stateList.form["pending"]
    hospitalizedCurrently = stateList.form["hospitalizedCurrently"]
    hospitalizedCumulative = stateList.form["hospitalizedCumulative"]
    inIcuCurrently = stateList.form["inIcuCurrently"]
    inIcuCumulative = stateList.form["inIcuCumulative"]
    onVentilatorCurrently = stateList.form["onVentilatorCurrently"]
    onVentilatorCumulative = stateList.form["onVentilatorCumulative"]
    recovered = stateList.form["recovered"]
    lastUpdateEt = stateList.form["lastUpdateEt"]
    checkTimeEt = stateList.form["checkTimeEt"]
    death = stateList.form["death"]
    dateModified = stateList.form["dateModified"]
    mongo.db.state_data.update_one({"dateModified": dateModified, "state": state}, {"$set": {
        "state": state,
        "positive": positive,
        "negative": negative,
        "pending": pending,
        "hospitalizedCurrently": hospitalizedCurrently,
        "hospitalizedCumulative": hospitalizedCumulative,
        "inIcuCurrently": inIcuCurrently,
        "inIcuCumulative": inIcuCumulative,
        "onVentilatorCurrently": onVentilatorCurrently,
        "onVentilatorCumulative": onVentilatorCumulative,
        "recovered": recovered,
        "lastUpdateEt": lastUpdateEt,
        "checkTimeEt": checkTimeEt,
        "death": death,
        "dateModified": dateModified
    }}, upsert=True)
    print('Sent the request to the route')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    requests.get("https://infection-data.herokuapp.com/")
    print('This job is run every weekday at 5pm.')
    stateList = json.loads(data.content.decode("utf-8"))
    state = stateList.form["state"]
    positive = stateList.form["positive"]
    negative = stateList.form["negative"]
    pending = stateList.form["pending"]
    hospitalizedCurrently = stateList.form["hospitalizedCurrently"]
    hospitalizedCumulative = stateList.form["hospitalizedCumulative"]
    inIcuCurrently = stateList.form["inIcuCurrently"]
    inIcuCumulative = stateList.form["inIcuCumulative"]
    onVentilatorCurrently = stateList.form["onVentilatorCurrently"]
    onVentilatorCumulative = stateList.form["onVentilatorCumulative"]
    recovered = stateList.form["recovered"]
    lastUpdateEt = stateList.form["lastUpdateEt"]
    checkTimeEt = stateList.form["checkTimeEt"]
    death = stateList.form["death"]
    dateModified = stateList.form["dateModified"]
    mongo.db.state_data.update_one({"dateModified": dateModified, "state": state}, {"$set": {
        "state": state,
        "positive": positive,
        "negative": negative,
        "pending": pending,
        "hospitalizedCurrently": hospitalizedCurrently,
        "hospitalizedCumulative": hospitalizedCumulative,
        "inIcuCurrently": inIcuCurrently,
        "inIcuCumulative": inIcuCumulative,
        "onVentilatorCurrently": onVentilatorCurrently,
        "onVentilatorCumulative": onVentilatorCumulative,
        "recovered": recovered,
        "lastUpdateEt": lastUpdateEt,
        "checkTimeEt": checkTimeEt,
        "death": death,
        "dateModified": dateModified
    }}, upsert=True)

sched.start()