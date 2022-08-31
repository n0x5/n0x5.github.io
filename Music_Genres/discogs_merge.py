# Create compact version

import os
import re
from tqdm import tqdm
import sqlite3
from lxml import etree
import time


sql_db = os.path.join(os.path.dirname( __file__ ), 'Discogs_Releases_Database_2022-08_COMPLETE.db')
conn = sqlite3.connect(sql_db)
cur = conn.cursor()

sql_db2 = os.path.join(os.path.dirname( __file__ ), 'Discogs_Releases_Database_COMPACT_2022-08_COMPLETE.db')
conn2 = sqlite3.connect(sql_db2)
cur2 = conn2.cursor()
cur2.execute('''CREATE TABLE if not exists discogs_merge \
        (release_id text, title text, format_name text, artist_id text, label_name text, \
        catno text, country text, genres text, styles text, released text, track_p text, master_id text unique, artist_name text, \
        descriptions text)''')

results = cur.execute("select release_id, title, format_name, artist_id, label_name, \
                        catno, country, genres, styles, min(released), track_p, master_id, artist_name, descriptions from releases group by master_id")

lst = []
for item in tqdm(results):
    final = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11].replace('None', item[1]+item[12]), item[12], item[13]
    lst.append(final)
    if len(lst) == 2000:
        cur2.executemany('insert or ignore into discogs_merge (release_id, title, format_name, artist_id, label_name, \
                        catno, country, genres, styles, released, track_p, master_id, artist_name, descriptions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (lst))
        cur2.connection.commit()
        lst = []

cur2.executemany('insert or ignore into discogs_merge (release_id, title, format_name, artist_id, label_name, \
                        catno, country, genres, styles, released, track_p, master_id, artist_name, descriptions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (lst))
cur2.connection.commit()