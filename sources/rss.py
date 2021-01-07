import requests
import json
import feedparser
from time import mktime
from html2text import html2text
import html2text

text_maker = html2text.HTML2Text()
text_maker.ignore_images = True
text_maker.ignore_tables = True
text_maker.ignore_links = True


def clean(content):
    content = text_maker.handle(content)
    return content.replace('\n\n', ':::').replace('\n', ' ').replace(':::', '\n\n').strip()


def fetch_articles(url, source='dailycal'):
    d = feedparser.parse(url)
    articles = []
    for entry in d.entries:
        if source == 'dailycal':
            summary = clean(entry['summary']).replace('Read More…', '').replace('The Daily Californian', '').strip()
            summary = ' '.join(summary.split('\n')[1:]).strip()
        else:
            summary = clean(entry['summary']).replace('Read More…', '').replace('The Daily Californian', '').strip()

        articles.append({
            'title': entry['title'],
            'url': entry['link'],
            'date': mktime(entry['published_parsed'] * 1000),
            'author': entry['author'],
            'summary': summary,
            'content': clean('\n'.join([x.value for x in entry.content])).strip() if source == 'dailycal' else None
        })

    featured = articles[0]
    feature_title = featured['title']
    if source == 'dailycal':
        feature_summary = ' '.join(featured['summary'].split('\n')[1:]).strip()
    else:
        feature_summary = ' '.join(featured['summary'].split('\n'))

    return json.dumps({
        'featured': {
            'title': feature_title,
            'summary': feature_summary,
        },
        'articles': articles
    })