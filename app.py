#set up server
#import packages
from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo
from flask import redirect, session, flash
import requests
import json

#initialize
#this function initializes any application
app = Flask(__name__)
app.debug = True

app.secret_key = "sri"

#config
app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/covid_state_db?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-aou9c.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)
print(mongo.db)

@app.route("/", methods = ['GET','POST'])
def get_data():
    if request.method == 'GET':
        data = requests.get("https://covidtracking.com/api/states")
        # data is a response object
        # data.content is of type bytes
        # json_data = json.loads(data.content.decode("utf-8"))
        # json.loads takes str as a parameter, so decode converts type bytes into string
        # json.loads converts string into dictionary
        # stateList = mongo.db.state_data.find({})
        stateList = json.loads(data.content.decode("utf-8"))
        return render_template("index.html", data = stateList)
    else:
        state = request.form["state"]
        positive = request.form["positive"]
        negative = request.form["negative"]
        pending = request.form["pending"]
        hospitalizedCurrently = request.form["hospitalizedCurrently"]
        hospitalizedCumulative = request.form["hospitalizedCumulative"]
        inIcuCurrently = request.form["inIcuCurrently"]
        inIcuCumulative = request.form["inIcuCumulative"]
        onVentilatorCurrently = request.form["onVentilatorCurrently"]
        onVentilatorCumulative = request.form["onVentilatorCumulative"]
        recovered = request.form["recovered"]
        lastUpdateEt = request.form["lastUpdateEt"]
        checkTimeEt = request.form["checkTimeEt"]
        death = request.form["death"]
        dateModified = request.form["dateModified"]
        mongo.db.state_data.update_one({"dateModified":dateModified, "state":state},{"$set":{
              "state":state,
              "positive":positive,
              "negative":negative,
              "pending":pending,
              "hospitalizedCurrently":hospitalizedCurrently,
              "hospitalizedCumulative":hospitalizedCumulative,
              "inIcuCurrently":inIcuCurrently,
              "inIcuCumulative":inIcuCumulative,
              "onVentilatorCurrently":onVentilatorCurrently,
              "onVentilatorCumulative":onVentilatorCumulative,
              "recovered":recovered,
              "lastUpdateEt":lastUpdateEt,
              "checkTimeEt":checkTimeEt,
              "death":death,
              "dateModified":dateModified
              }},upsert=True)
        return "success"

@app.route("/state", methods = ['GET','POST'])
def get_state_data():
    if request.method == 'GET':
        results = mongo.db.state_data.find({})
        trends = []
        for i in results:
            trends.append(i)
        print(trends)
        state_master = []
        for dict in trends:
            if dict["state"] not in state_master:
                state_master.append(dict["state"])
    return render_template("trend_state.html", trends = trends, state_master = state_master)

#run
if __name__ == "__main__":
    app.run("")