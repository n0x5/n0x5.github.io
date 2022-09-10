# need API auth token

import sqlite3
import requests
import json
import argparse
import os
import time

token = ''


sql_db = os.path.join(os.path.dirname( __file__ ), '..', 'databases', 'discogs_api.db')
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists discogs_api
            (artist text, title text, year text, genres text, styles text, country text, 
                master_id text unique, catno text, format text, id text, cover_image text, label text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


headers = {
'User-Agent': 'CUSTOM USER AGENT'
}

def get_rels(page, url):
    print(url)
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    pages = data['pagination']['pages']
    for item in data['results']:
        artist = item['title'].split(' - ')[0]
        title_final = item['title'].split(' - ')[1]
        stuff = artist, title_final, item['year'], ', '.join(item['genre']), ', '.join(item['style']), \
                    item['country'], item['master_id'], item['catno'], ', '.join(item['format']), item['id'], item['cover_image'], ', '.join(item['label'])
        print(stuff)
        cur.execute('insert or ignore into discogs_api (artist, title, year, genres, styles, country, master_id, catno, \
                     format, id, cover_image, label) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (stuff))
        cur.connection.commit()

    print('page {} / {}' .format(page, pages))
    page += 1
    time.sleep(2)
    if page <= pages:
        url = 'https://api.discogs.com/database/search?year=2021&format=cd,album&country=us&token={}&type=release&per_page=100&page={}' .format(token, page)
        get_rels(page, url)

page = 1
url = 'https://api.discogs.com/database/search?year=2021&format=cd,album&country=us&token={}&type=release&per_page=100&page={}' .format(token, page)
get_rels(page, url)


