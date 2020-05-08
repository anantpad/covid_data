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

@app.route("/", methods = ['GET'])
def get_data():
    data = requests.get("https://covidtracking.com/api/states")
    # data is a response object
    # data.content is of type bytes
    json_data = json.loads(data.content.decode("utf-8"))
    # json.loads takes str as a parameter, so decode converts type bytes into string
    # json.loads converts string into dictionary
    for record in json_data:
        state = record["state"]
        positive = record["positive"]
        negative = record["negative"]
        pending = record["pending"]
        hospitalizedCurrently = record["hospitalizedCurrently"]
        hospitalizedCumulative = record["hospitalizedCumulative"]
        inIcuCurrently = record["inIcuCurrently"]
        inIcuCumulative = record["inIcuCumulative"]
        onVentilatorCurrently = record["onVentilatorCurrently"]
        onVentilatorCumulative = record["onVentilatorCumulative"]
        recovered = record["recovered"]
        lastUpdateEt = record["lastUpdateEt"]
        checkTimeEt = record["checkTimeEt"]
        death = record["death"]
        hash = record["hash"]
        mongo.db.state_data.insert_one(
            {
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
                "hash": hash
            }
        )
    stateList = mongo.db.state_data.find({})
    return render_template("index.html", data = stateList)

#run
if __name__ == "__main__":
    app.run("")