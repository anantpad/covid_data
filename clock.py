from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
from pymongo import MongoClient

uri = "mongodb://" + app.config["USERNAME"] + ":" + app.config["PASSWORD"] + "@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/covid_state_db?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(uri)
print(client)

sched = BlockingScheduler()

@sched.scheduled_job('interval', day=1)
# this interval job is used to specify how often this has to repeat
def timed_job():
    data = requests.get("https://covidtracking.com/api/states")
    stateList = json.loads(data.content.decode("utf-8"))
    print(stateList)
    for stateRecord in stateList:
        state = stateRecord["state"]
        positive = stateRecord["positive"]
        negative = stateRecord["negative"]
        pending = stateRecord["pending"]
        hospitalizedCurrently = stateRecord["hospitalizedCurrently"]
        hospitalizedCumulative = stateRecord["hospitalizedCumulative"]
        inIcuCurrently = stateRecord["inIcuCurrently"]
        inIcuCumulative = stateRecord["inIcuCumulative"]
        onVentilatorCurrently = stateRecord["onVentilatorCurrently"]
        onVentilatorCumulative = stateRecord["onVentilatorCumulative"]
        recovered = stateRecord["recovered"]
        lastUpdateEt = stateRecord["lastUpdateEt"]
        checkTimeEt = stateRecord["checkTimeEt"]
        death = stateRecord["death"]
        dateModified = stateRecord["dateModified"]
        # client.database name or auth source attribute.collectionName.query
        client.covid_state_db.state_data.update_one({"dateModified": dateModified, "state": state}, {"$set": {
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

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # cronjob you mention what time it has to occur
# def scheduled_job():
#     data = requests.get("https://infection-data.herokuapp.com/")
#     print('This job is run every weekday at 5pm.')
#     stateList = json.loads(data.content.decode("utf-8"))
#     state = stateRecord["state"]
#     positive = stateRecord["positive"]
#     negative = stateRecord["negative"]
#     pending = stateRecord["pending"]
#     hospitalizedCurrently = stateRecord["hospitalizedCurrently"]
#     hospitalizedCumulative = stateRecord["hospitalizedCumulative"]
#     inIcuCurrently = stateRecord["inIcuCurrently"]
#     inIcuCumulative = stateRecord["inIcuCumulative"]
#     onVentilatorCurrently = stateRecord["onVentilatorCurrently"]
#     onVentilatorCumulative = stateRecord["onVentilatorCumulative"]
#     recovered = stateRecord["recovered"]
#     lastUpdateEt = stateRecord["lastUpdateEt"]
#     checkTimeEt = stateRecord["checkTimeEt"]
#     death = stateRecord["death"]
#     dateModified = stateRecord["dateModified"]
    # mongo.db.state_data.update_one({"dateModified": dateModified, "state": state}, {"$set": {
    #     "state": state,
    #     "positive": positive,
    #     "negative": negative,
    #     "pending": pending,
    #     "hospitalizedCurrently": hospitalizedCurrently,
    #     "hospitalizedCumulative": hospitalizedCumulative,
    #     "inIcuCurrently": inIcuCurrently,
    #     "inIcuCumulative": inIcuCumulative,
    #     "onVentilatorCurrently": onVentilatorCurrently,
    #     "onVentilatorCumulative": onVentilatorCumulative,
    #     "recovered": recovered,
    #     "lastUpdateEt": lastUpdateEt,
    #     "checkTimeEt": checkTimeEt,
    #     "death": death,
    #     "dateModified": dateModified
    # }}, upsert=True)

sched.start()