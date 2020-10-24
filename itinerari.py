import requests as r
from dateutil import parser

COORD_BASE = "https://api-adresse.data.gouv.fr/search"
CM_BASE = "https://citymapper.com/api/7/journeys"

def locate(place):

    resp = r.get(COORD_BASE, params={"q":place.replace(" ","-")})
    if len(resp.json()["features"]) == 0:
        raise RuntimeError(f"{place} not found")
    else:
        coords = reversed(resp.json()["features"][0]["geometry"]["coordinates"])
        return ','.join(str(c) for c in coords)

def display(journey):

    output = ""
    d = round(journey["duration_seconds"]/60)
    output += f"- Total - {d} min\n"

    for l in journey["legs"]:
        if l["mode"] == "walk":
            d = round(l["duration_seconds"]/60)
            output += f"- Walk - {d} min\n"

        if l["mode"] == "transit":
            start = l["stops"][0]
            end = l["stops"][-1]
            line = l["routes"][0]["display_name"]
            d = round(end["duration_seconds_to_here"]/60)
            output += f"- {line} - {d} min\n"
            output += "\t+ " + start["name"] + parser.parse(l["departure_time"]).strftime(" %H:%M") + "\n"
            output += "\t| \n"
            output += "\t+ " + end["name"] + parser.parse(l["arrival_time"]).strftime(" %H:%M") + "\n"
    
    return output

def link(start, end):

    iti = ""
    [startcoord, endcoord] = [locate(x) for x in [start, end]]
    try:
        resp = r.get(CM_BASE, params={"start": startcoord, "end": endcoord, "region_id":"fr-paris"})
        journeys = resp.json()["journeys"]
        if len(journeys) > 0:
            iti = display(min(journeys, key= lambda x: x["duration_seconds"]))
        else:
            iti = "Nothing found\n"
        iti += resp.url.replace("api/7/journeys","directions")
        return iti

    except Exception as e:
        return e