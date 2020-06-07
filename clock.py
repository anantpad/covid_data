from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
sched = BlockingScheduler()
app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/covid_state_db?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    data = requests.get("https://covidtracking.com/api/states")
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
    data = requests.get("https://infection-data.herokuapp.com/")
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