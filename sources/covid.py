import requests
import json
from datetime import datetime as dt, timedelta
import pandas as pd
import io
import pytz
from pytz import timezone

def query_berkeley(start_date, end_date):
    """
    start_date and end_date should be formatted like: 2022-01-07
    """
    url = "https://calviz.berkeley.edu/t/COVIDRecoveryPublic/" + \
        "views/UHSCovidData/Output/aCovidData.csv" + \
        f"?Begin%20Date%20Parameter={start_date}&End%20Date%20Parameter={end_date}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    df = pd.read_csv(io.StringIO(response.text)).fillna(0)
    positive = float(str(df['# Total Cases Within Timeframe'][0]).replace(',', ''))
    return positive
    

def fetch_campus_covid_data():

    results = []

    for i in range(1, 8):
        dtfmt = lambda date : date.strftime("%Y-%m-%d")
        today = dt.now(tz=pytz.utc)
        today = today.astimezone(timezone('US/Pacific'))
        target = today - timedelta(days=i)
        start = dtfmt(target)
        end = start
        positive = query_berkeley(start, end)
        display_date = target.strftime("%-m/%-d")
        results.append({
            'date': display_date,
            'positive': positive
        })

    return json.dumps(results)
