#!/usr/bin/python3

import sys
import requests as r
from dateutil import parser
import colorama

COORD_BASE = "https://api-adresse.data.gouv.fr/search"
CM_BASE = "https://citymapper.com/api/7/journeys"

def usage():

    print("A - B")

def locate(place):

    resp = r.get(COORD_BASE, params={"q":place.replace(" ","-")})
    if len(resp.json()["features"]) == 0:
        raise RuntimeError(f"{place} not found")
    else:
        coords = reversed(resp.json()["features"][0]["geometry"]["coordinates"])
        return ','.join(str(c) for c in coords)

def fetch(payload):
    resp = r.get(CM_BASE, params=payload)
    return resp

def output(journey):

    d = round(journey["duration_seconds"]/60)
    print(f"- Total - {d} min")

    for l in journey["legs"]:
        if l["mode"] == "walk":
            d = round(l["duration_seconds"]/60)
            print(f"- Walk - {d} min")
        if l["mode"] == "transit":
            start = l["stops"][0]
            end = l["stops"][-1]
            line = l["routes"][0]["display_name"]
            d = round(end["duration_seconds_to_here"]/60)
            print(f"- {line} - {d} min")
            print("\t+ " + start["name"] + parser.parse(l["departure_time"]).strftime(" %H:%M"))
            print("\t|")
            print("\t+ " + end["name"] + parser.parse(l["arrival_time"]).strftime(" %H:%M"))

def main(args):

    if '-' not in args:
        usage()
    else:
        [start, end] = " ".join(args).split(' - ')
        try:
            [startcoord, endcoord] = [locate(x) for x in [start, end]]
            resp = fetch({"start": startcoord, "end": endcoord, "region_id":"fr-paris"})
            journeys = resp.json()["journeys"]
            output(min(journeys, key= lambda x: x["duration_seconds"]))
            print(resp.url)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    main(sys.argv[1:])