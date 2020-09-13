from flask import Flask, request
import pandas as pd, numpy, time

app = Flask(__name__)
requests = pd.DataFrame({"Name": [""], "Phone": [""], "Lat": [-1.0],
                         "Long": [-1.0], "Text": [""], "RequestTime": [0.0],
                         "ExpireTime": [0.0]})

# This is for the users looking for help: they can post listings reaching out
# for help with their contact information, time frame of needed help, location,
# and a description
@app.route("/request")
def help_request():
    global requests
    try:
        args = request.args
        currtime = time.time()
        requestinfo = {
            "Name": args["name"],
            "Phone": args["phone"],
            "Lat": float(args["lat"]),
            "Long": float(args["long"]),
            "Text": args["text"],
            "RequestTime": currtime,
            "ExpireTime": currtime + int(args["duration"])
        }
    except:
        return """Please provide name, phone, lat (float), long (float), text, 
            and duration (integer seconds).""", 400
    try:
        requests = requests.append(requestinfo, ignore_index=True)
    except:
        return "Server error: Could not update data", 500
    return "Success!"

# This is for the users looking to provide help: they can search nearby listings
# and filter by type of help needed
@app.route("/list")
def list_requests():
    global requests
    try:
        # Collect the user coordinates used to calculate their distance from
        # request locations
        user_lat = numpy.deg2rad(float(request.args["lat"]))
        user_long = numpy.deg2rad(float(request.args["long"]))
        # User will provide maximum radius for search
        if "maxdist" in request.args: maxdist = float(request.args["maxdist"])
        else: maxdist = float("inf")
        # Compute distance from user to all requests and stores in DataFrame
        if "filter" in request.args: filter = request.args["filter"]
        else: filter = ""
    except:
        return """Please provide lat (float), long (float), maxdist
            (optional float), and filter (optional).""", 400
    try:
        requests = requests.assign(
            Distance = 6373.0 * 2 * numpy.arctan2(
                numpy.sqrt(numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2
                           + numpy.cos(user_lat) * numpy.cos(numpy.deg2rad(requests.Lat))
                           * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2),
                numpy.sqrt(1 - (numpy.sin((numpy.deg2rad(requests.Lat) - user_lat) / 2)**2
                                + numpy.cos(user_lat) * numpy.cos(numpy.deg2rad(requests.Lat))
                                * numpy.sin((numpy.deg2rad(requests.Long) - user_long) / 2)**2))))
        # Filters out all requests out of maximum range and sorts by nearest
        filtered = requests[requests.Distance < maxdist].sort_values("Distance")
        # Filters out all expired requests
        currtime = time.time()
        filtered = filtered[filtered.ExpireTime > currtime]
        # Filters by a search keyword if provided (for example, if the user
        # wants to provide tools, they would type "tools" and all requests with
        # description mentioning "tools" will show
        filtered = filtered[filtered.Text.str.contains(filter)]
        # json conversion for integration with front end
        filtered_json = filtered.to_json()
    except:
        return "Server error: Could not fetch data", 500
    return filtered_json


if __name__ == "__main__":
    app.run(debug=True)
