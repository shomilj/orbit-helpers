from bs4 import BeautifulSoup
import requests
import json

def fetch_dining():
    soup = BeautifulSoup(requests.get('https://caldining.berkeley.edu/menus/').text, 'html.parser')
    halls = {}
    for menu in soup.find_all(class_='location-name'):
        hall = {}
        title = menu.find(class_='cafe-title').text
        times = []
        for row in menu.find(class_='cafe-status').find_all('span'):
            times.append(row.text)
        times = 'Times for ' + times[-1] + ':\n' + '\n'.join(times[:-1])
        hall['times'] = times
        hall['periods'] = []
        for name in menu.find_all(class_='preiod-name'):
            period = name.attrs.get('class')[1]
            period_data = {}
            period_data['name'] = period 
            period_data['categories'] = []
            for cat in name.find_all(class_='cat-name'):
                category_data = {}
                cat_name = cat.find('span').text
                category_data = {'name': cat_name, 'items': []}
                for row in cat.find_all(class_='recip'):
                    category_data['items'].append(row.find('span').text)
                period_data['categories'].append(category_data)
            hall['periods'].append(period_data)
        halls[title] = hall

    return json.dumps(halls)