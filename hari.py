#!/usr/bin/python3

import sys
import requests as r
from dateutil import parser
from anytree import Node, RenderTree

COORD_BASE = "https://api-adresse.data.gouv.fr/search"
CM_BASE = "https://citymapper.com/api/7/journeys"

def usage():
    return "A - B\n"

def locate(place):

    resp = r.get(COORD_BASE, params={"q":place.replace(" ","-"), "lat":48.8534, "lon":2.3488})
    if len(resp.json()["features"]) == 0:
        raise RuntimeError(f"{place} not found")
    else:
        coords = reversed(resp.json()["features"][0]["geometry"]["coordinates"])
        return ','.join([str(c) for c in coords])

def display(journey):

    output = ""
    d = round(journey["duration_seconds"]/60)
    eta = parser.parse(journey["legs"][-1]["arrival_time"]).strftime("%H:%M")
    root = Node(f"- Total: {d} min - ETA: {eta}")

    for l in journey["legs"]:
        if l["mode"] == "walk":
        
            d = round(l["duration_seconds"]/60)
            child = Node(f"Walk - {d} min", parent=root)

        if l["mode"] == "transit":
            
            start = l["stops"][0]
            end = l["stops"][-1]
            way = l["routes"][0]["display_name"]
            d = round(end["duration_seconds_to_here"]/60)
            
            child = Node(f"{way} - {d} min", parent=root)
            sub_start = Node(start["name"] + parser.parse(l["departure_time"]).strftime(" %H:%M"), parent=child)
            sub_end = Node(end["name"] + parser.parse(l["arrival_time"]).strftime(" %H:%M"), parent=child)

    for pre, fill, node in RenderTree(root):
        output += f"{pre}{node.name}\n"
    
    return output

def link(start, end):

    iti = ""
    [startcoord, endcoord] = [locate(x) for x in [start, end]]
    try:
        resp = r.get(CM_BASE, params={"start": startcoord, "end": endcoord, "region_id":"fr-paris"})
        journeys = resp.json()["journeys"]
        if len(journeys) == 0:
            iti = "Nothing found\n"
        else:
            best = min(journeys, key= lambda x: x["duration_seconds"])
            iti = display(best)
        iti += resp.url.replace("api/7/journeys","directions") + "\n"
        return iti

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if sys.stdin.isatty():
        args = sys.argv
        if len(args) > 1:
            args = " ".join(args[1:])
    else:
        args = sys.stdin.read()
    if args:
        if '-' not in args:
            sys.stderr.write(usage())
        else:
            [start, end] = args.split(' - ')
            sys.stdout.write(link(start, end))