import os
import re
from tqdm import tqdm
import sqlite3
from lxml import etree
import time

ins_country = 'us'

sql_db = os.path.join(os.path.dirname( __file__ ), 'discogs2.db')
conn = sqlite3.connect(sql_db)
cur = conn.cursor()

sql_db2 = os.path.join(os.path.dirname( __file__ ), 'discogs_{}.db' .format(ins_country))
conn2 = sqlite3.connect(sql_db2)
cur2 = conn2.cursor()
cur2.execute('''CREATE TABLE if not exists discogs_{}
        (rel_date text, label text, title text, genres text, styles text, format_name text, artist_name text, catno text, track_p text, master_id text unique, dated datetime DEFAULT CURRENT_TIMESTAMP)''' .format(ins_country))

results = cur.execute("select min(released), label_name, title, genres, styles, format_name, artist_name, catno, track_p, master_id from releases where label_name not like 'Not On Label' and label_name not like '%Self-released%' and track_p not like 'None' and released not like 'None' and country like '{}' group by release_id order by released asc" .format(ins_country))

lst = []
for item in tqdm(results):
    final = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9].replace('None', item[2]+item[6])
    lst.append(final)
    if len(lst) == 2000:
        cur2.executemany('insert or ignore into discogs_{} (rel_date, label, title, genres, styles, format_name, artist_name, catno, track_p, master_id) VALUES (?,?,?,?,?,?,?,?,?,?)' .format(ins_country), (lst))
        cur2.connection.commit()
        lst = []

