import json
import csv
from time import sleep
import requests

DOUBAN_API_DOMAIN = 'https://api.douban.com/v2/'

# Find all the posts in a specific group within the page limit
# (say, only search the posts of the group within 100 pages)


def get_posts_from_groups(groups):
    all_posts = []
    for aGroup in groups:
        count = 50
        start = 0
        while start < 1000:
            url = DOUBAN_API_DOMAIN + 'group/' + aGroup + \
                '/topics?count=%d&start=%d' % (count, start)
            print 'Fetching posts from froup: %s' % url
            response = requests.get(url)
            response_json = json.loads(response.text)
            try:
                posts_list = response_json['topics']
                for aDict in posts_list:
                    author_id = aDict['author']['uid']
                    if author_id == '146514079':
                        all_posts.append(aDict['alt'])
                start += count
                sleep(1)
            except:
                break
    for post_url in all_posts:
        print 'Post url: %s' % post_url


get_posts_from_groups(['kaopulove', 'lovesh', '159755', 'sz-love', 'shenzhen'])
