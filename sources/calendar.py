import requests
import json
from ics import Calendar
import time


def fetch_calendar(url):
    c = Calendar(requests.get(url).text)
    events = []
    for event in c.events:
        if event.begin == None:
            continue
        if event.end == None:
            continue
        if time.time() - event.end.timestamp >= 0:
            continue
        events.append({
            'name': event.name,
            'begin': event.begin.timestamp * 1000 if event.begin != None else None,
            'end': event.end.timestamp * 1000 if event.end != None else None,
            'description': event.description,
            'location': event.location,
        })
    events = sorted(events, key=lambda e: e['begin'])
    return json.dumps(events)
