# need API auth token

import sqlite3
import requests
import json
import argparse


token = ''

parser = argparse.ArgumentParser()
parser.add_argument('genre')
parser.add_argument('page')
args = parser.parse_args()

genre = args.genre
page = args.page

sql_db = 'discogs_api.db'
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists discogs_api
            (artist text, title text, year text, genres text, styles text, country text, 
                master_id text unique, catno text, format text, id text, cover_image text, label text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


headers = {
'User-Agent': 'CUSTOM USER AGENT'
}

url = 'https://api.discogs.com/database/search?year=2022&format=cd,album&genre={}&country=us&token={}&type=release&per_page=100&page={}' .format(genre, token, page)

response = requests.get(url, headers=headers)

data = json.loads(response.text)

for item in data['results']:
    artist = item['title'].split(' - ')[0]
    title_final = item['title'].split(' - ')[1]
    stuff = artist, title_final, item['year'], ', '.join(item['genre']), ', '.join(item['style']), \
                item['country'], item['master_id'], item['catno'], ', '.join(item['format']), item['id'], item['cover_image'], ', '.join(item['label'])
    print(stuff)
    cur.execute('insert or ignore into discogs_api (artist, title, year, genres, styles, country, master_id, catno, \
                 format, id, cover_image, label) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (stuff))
    cur.connection.commit()
