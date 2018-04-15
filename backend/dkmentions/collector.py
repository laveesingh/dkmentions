import json
import os
import requests
from bs4 import BeautifulSoup as Soup

archive_filename = 'archive.json' # this is temporary, needs to be changed

class Collector:

    def __init__(self):
        prefix = 'https://www.socialbakers.com/statistics/'
        self.url_formats = {
            'facebook': prefix + 'facebook/pages/total/denmark/page-%d-%d/',
            'twitter': prefix + 'twitter/profiles/denmark/page-%d-%d/',
            'youtube': prefix +'youtube/channels/denmark/page-%d-%d'
        }

    def fetch_users_from_page(self, url):
        '''takes a url and returns a list of user_id's'''
        try:
            response = requests.get(url).content
        except Exception as e:
            print('There was some error, processing the url:', url)
            print(e)
            return []
        soup = Soup(response, 'html.parser')
        table = soup.find('table', attrs={'class': 'brand-table-list'})
        rows = [tr for tr in table.findAll('tr') if not tr.get(
            'class') or (tr.get('class')[0] != 'replace-with-show-more')]
        user_list = []
        for row in rows:
            anchor = row.find('td', attrs={'class': 'name'}).find(
                'div', attrs={'class': 'item'}).find('a')
            link = anchor.get('href')
            user_id = link.split('/')[-1].split('-')[0]
            user_list.append(user_id)
        return user_list

    def fetch_users(self, network):
        url_format = self.url_formats[network]
        users_list = []
        for i in range(1, 100, 5):
            print('fetching list from %d to %d' % (i, i+4))
            url = url_format % (i, i+4)
            try:
                new_users_list = self.fetch_users_from_page(url)
                print('fetched:', new_users_list)
                users_list.extend(new_users_list)
            except:
                break
        return users_list

    def fetch(self):
        self.facebook_users = self.fetch_users('facebook')
        self.twitter_users = self.fetch_users('twitter')
        self.youtube_users = self.fetch_users('youtube')

    def store(self):
        json_object = {
            'facebook': self.facebook_users,
            'twitter': self.twitter_users,
            'youtube': self.youtube_users
        }
        json_string = json.dumps(json_object, indent=4, sort_keys=True)
        with open(archive_filename, 'w+') as f:
            f.write(json_string)

# c = Collector()
# c.fetch()
# c.store()
