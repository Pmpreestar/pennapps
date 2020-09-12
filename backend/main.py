from flask import Flask
from flask import request
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import numpy

app = Flask(__name__)
requests = pd.DataFrame()
types = pd.DataFrame()

@app.route("/request")
def help_request():
    global requests, types
    args = request.args
    requests = requests.append(
        {"FirstName": args["firstname"],
         "LastName": args["lastname"],
         "Phone": args["phone"],
         "Lat": float(args["lat"]),
         "Long": float(args["long"])},
        ignore_index=True)
    for type in args["types"].split(","):
        types = types.append(
            {"RequestID" : int(requests.index.values[-1]),
             "Type" : type}, ignore_index=True)
    return requests.to_json() + "<br>" + types.to_json(), 200

@app.route("/list")
def list_requests():
    global requests, types
    R = 6373.0
    user_lat = radians(float(request.args["lat"]))
    user_long = radians(float(request.args["long"]))
    maxdist = float(request.args["maxdist"])
    if "typefilter" in request.args:
        typefilter = request.args["typefilter"].split(",")
    requests = requests.assign(
        Distance = R * 2 * atan2(sqrt(sin((radians(requests.Lat) - user_lat) / 2)**2 + cos(user_lat)
                                      * cos(radians(requests.Lat)) * sin((radians(requests.Long) - user_long) / 2)**2),
                                 sqrt(1 - (sin((radians(requests.Lat) - user_lat) / 2)**2 + cos(user_lat)
                                      * cos(radians(requests.Lat)) * sin((radians(requests.Long) - user_long) / 2)**2))))
    if "typefilter" in locals(): filtered = types[types.Type.isin(typefilter)]
    else: filtered = types
    requestfilter = set(map(lambda n: numpy.int64(n), list(filtered["RequestID"])))
    ret = pd.DataFrame()
    for type in filtered:
        get RequestID row from requests
        put that in ret
        store type as array in new Types column for ret
    return "ret"


if __name__ == "__main__":
    app.run(debug=True)