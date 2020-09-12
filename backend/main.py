from flask import Flask, request
import pandas as pd, numpy, time

app = Flask(__name__)
requests = pd.DataFrame()

@app.route("/request")
def help_request():
    global requests, types
    args = request.args
    currtime = time.time()
    requests = requests.append(
        {"Name": args["name"],
         "Phone": args["phone"],
         "Lat": float(args["lat"]),
         "Long": float(args["long"]),
         "Text": args["text"],
         "RequestTime": currtime,
         "ExpireTime": currtime + int(args["duration"])
         }, ignore_index=True)
    return requests.to_json()

@app.route("/list")
def list_requests():
    global requests, types
    user_lat = numpy.deg2rad(float(request.args["lat"]))
    user_long = numpy.deg2rad(float(request.args["long"]))
    maxdist = float(request.args["maxdist"])
    if "filter" in request.args: filter = request.args["filter"]
    else: filter = ""
    requests = requests.assign(
        Distance = 6373.0 * 2 * numpy.arctan2(numpy.sqrt(numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2 + numpy.cos(user_lat)
                                      * numpy.cos(numpy.deg2rad(requests.Lat)) * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2),
                                 numpy.sqrt(1 - (numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2 + numpy.cos(user_lat)
                                      * numpy.cos(numpy.deg2rad(requests.Lat)) * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2))))
    filtered = requests[requests.Distance < maxdist].sort_values("Distance")
    currtime = time.time()
    filtered = filtered[filtered.ExpireTime > currtime]
    filtered = filtered[filtered.Text.str.contains(filter)]
    return filtered.to_json()


if __name__ == "__main__":
    app.run(debug=True)