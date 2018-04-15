import json
import os
import requests
import threading
import time
from bs4 import BeautifulSoup as Soup

archive_filename = 'archive.json'  # this is temporary, needs to be changed


class Collector:

    def __init__(self):
        prefix = 'https://www.socialbakers.com/statistics/'
        self.url_formats = {
            'facebook': prefix + 'facebook/pages/total/denmark/page-%d-%d/',
            'twitter': prefix + 'twitter/profiles/denmark/page-%d-%d/',
            'youtube': prefix + 'youtube/channels/denmark/page-%d-%d'
        }
        self.facebook_users = []
        self.twitter_users = []
        self.youtube_users = []
        self.collector_threads = set()
        main_thread = threading.Thread(
            target=self.main,
        )
        main_thread.start()

    def main(self):
        self.fetch()
        while True:
            if len(self.collector_threads) == 0:
                break
            else:
                print('active threads:', len(self.collector_threads))
                time.sleep(1)
        self.store()

    def fetch_users_from_page(self, url, network, thread_name):
        try:
            response = requests.get(url).content
        except Exception as e:
            print('There was some error, processing the url:', url)
            print(e)
            self.collector_threads.remove(thread_name)
            return
        soup = Soup(response, 'html.parser')
        try:
            table = soup.find('table', attrs={'class': 'brand-table-list'})
            rows = [tr for tr in table.findAll('tr') if not tr.get(
                'class') or (tr.get('class')[0] != 'replace-with-show-more')]
        except:
            self.collector_threads.remove(thread_name)
            return
        user_list = []
        for row in rows:
            anchor = row.find('td', attrs={'class': 'name'}).find(
                'div', attrs={'class': 'item'}).find('a')
            link = anchor.get('href')
            user_id = link.split('/')[-1].split('-')[0]
            user_list.append(user_id)
        if network == 'facebook':
            self.facebook_users.extend(user_list)
        elif network == 'twitter':
            self.twitter_users.extend(user_list)
        else:
            self.youtube_users.extend(user_list)
        self.collector_threads.remove(thread_name)

    def fetch_users(self, network):
        url_format = self.url_formats[network]
        for i in range(1, 100, 5):
            url = url_format % (i, i+4)
            try:
                thread_name = '%s-%d-%d' % (network, i, i+4)
                thread = threading.Thread(
                    target=self.fetch_users_from_page,
                    args=(url, network, thread_name),
                )
                self.collector_threads.add(thread_name)
                self.flag = True
                thread.start()
            except Exception as e:
                # print(e)
                break

    def fetch(self):
        self.fetch_users('facebook')
        self.fetch_users('twitter')
        self.fetch_users('youtube')

    def store(self):
        json_object = {
            'facebook': self.facebook_users,
            'twitter': self.twitter_users,
            'youtube': self.youtube_users
        }
        json_string = json.dumps(json_object, indent=4, sort_keys=True)
        with open(archive_filename, 'w+') as f:
            f.write(json_string)

c = Collector()
