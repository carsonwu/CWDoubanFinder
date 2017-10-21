import json
import csv
from time import sleep
import urllib2
from bs4 import BeautifulSoup
import requests

DOUBAN_API_DOMAIN = 'https://api.douban.com/v2/'
DOUBAN_DOMAIN = 'https://www.douban.com/'

# Find all the posts in a specific group within the page limit
# (say, only search the posts of the group within 100 pages)


def get_posts_from_groups(groups, user_id):
    all_posts = []
    group_index = 1
    for group in groups:
        count = 50
        start = 0
        print '================ NOW SEARCH %d GROUP ================' % group_index
        group_index += 1
        while start < 1000:
            url = DOUBAN_API_DOMAIN + 'group/' + group + \
                '/topics?count=%d&start=%d' % (count, start)
            print 'Fetching posts from froup: %s' % url
            response = requests.get(url)
            response_json = json.loads(response.text)
            try:
                posts_list = response_json['topics']
                for post_dict in posts_list:
                    author_id = post_dict['author']['uid']
                    if author_id == user_id:
                        all_posts.append(post_dict['alt'])
                start += count
                sleep(10)
            except:
                break
    for post_url in all_posts:
        print 'Post url: %s' % post_url


def get_groups_of_user(user_id):
    page_url = DOUBAN_DOMAIN + 'group/people/%s/joins' % user_id
    page_html = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page_html, 'html.parser')
    title_box_list = soup.findAll('div', attrs={'class': 'title'})
    group_name_list = []
    for title_box in title_box_list:
        # URL sample -> https://www.douban.com/group/558305/
        group_name = title_box.a.get('href').split('/group/')[-1][:-1]
        # print group_name
        group_name_list.append(group_name)
    print 'This user joined %d groups' %len(group_name_list)
    return group_name_list


def get_posts_of_user(user_id):
    groups_the_user_joined = get_groups_of_user(user_id)
    get_posts_from_groups(groups_the_user_joined, user_id)

get_posts_of_user('146514079')