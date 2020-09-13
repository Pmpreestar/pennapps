from flask import Flask, request
import pandas as pd, numpy, time

app = Flask(__name__)
requests = pd.DataFrame()

#This is for the users looking for help: they can post listings reaching out for help with their contact information, time frame of needed help,
#location, and a description
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

#This is for the users looking to provide help: they can search nearby listings and filter by type of help needed
@app.route("/list")
def list_requests():
    global requests, types
    #Collect the user coordinates used to calculate their distance from request locations
    user_lat = numpy.deg2rad(float(request.args["lat"]))
    user_long = numpy.deg2rad(float(request.args["long"]))
    #User will provide maximum radius for search
    maxdist = float(request.args["maxdist"])
    #Compute distance from user to all requests and stores in DataFrame
    if "filter" in request.args: filter = request.args["filter"]
    else: filter = ""
    requests = requests.assign(
        Distance = 6373.0 * 2 * numpy.arctan2(numpy.sqrt(numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2 + numpy.cos(user_lat)
                                      * numpy.cos(numpy.deg2rad(requests.Lat)) * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2),
                                 numpy.sqrt(1 - (numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2 + numpy.cos(user_lat)
                                      * numpy.cos(numpy.deg2rad(requests.Lat)) * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2))))
    #Filters out all requests out of maximum range and sorts by nearest
    filtered = requests[requests.Distance < maxdist].sort_values("Distance")
    #Filters out all expired requests
    currtime = time.time()
    filtered = filtered[filtered.ExpireTime > currtime]
    #Filters by a search keyword if provided (for example, if the user wants to provide tools, they would type "tools" 
    #and all requests with description mentioning "tools" will show
    filtered = filtered[filtered.Text.str.contains(filter)]
    #json conversion for integration with front end
    return filtered.to_json()


if __name__ == "__main__":
    app.run(debug=True)
