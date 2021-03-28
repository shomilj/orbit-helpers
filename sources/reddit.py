import requests
import json
import html2text

h = html2text.HTML2Text()

def fetch_reddit():
    data = requests.get('https://www.reddit.com/r/berkeley.json',
                        headers={'User-agent': 'your bot 0.1'}).json()
    posts = []
    for postData in data['data']['children']:
        post = postData['data']
        if post['stickied']:
            continue
        else:
            posts.append({
                'title': h.handle(post.get('title', '')).strip(),
                'text': h.handle(post.get('selftext', '')).strip(),
                'author': post['author'],
                'created': post['created_utc'] * 1000,
                'url': post['url'],
                'ups': post['ups'],
                'downs': post['downs'],
                'comments': post['num_comments']
            })
    return json.dumps(posts)
