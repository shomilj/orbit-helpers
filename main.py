from flask import escape
import json
from sources.reddit import fetch_reddit
from sources.calendar import fetch_calendar
from sources.rss import fetch_articles
from sources.covid import fetch_campus_covid_data
from sources.dininghall import fetch_dining

# gcloud config set project orbit-000
# gcloud functions deploy orbit_api --runtime python38 --trigger-http --allow-unauthenticated


def orbit_api(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    if type(request) is not dict:
        request_json = request.get_json(silent=True)
        request_args = request.args
    else:
        request_json = request.get('json')
        request_args = request.get('args')

    if request_json and 'source' in request_json:
        source = request_json['source']
        request = request_json
    elif request_args and 'source' in request_args:
        source = request_args['source']
        request = request_args
    else:
        return json.dumps({'error': 'Source not found.'})

    if source == 'reddit':
        return fetch_reddit()
    elif source == 'calendar':
        return fetch_calendar(url=request['url'])
    elif source == 'dailycal':
        return fetch_articles(url=request['url'], source='dailycal')
    elif source == 'berkeleyside':
        return fetch_articles(url=request['url'], source='berkeleyside')
    elif source == 'campus_covid':
        return fetch_campus_covid_data()
    elif source == 'dining':
        return fetch_dining()
    else:
        return json.dumps({'error': 'Unknown route.'})
