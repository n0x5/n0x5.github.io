import os
import sqlite3
from tqdm import tqdm
import re


conn2 = sqlite3.connect('pypi_new_2022.db')
cur = conn2.cursor()

conn_meta = sqlite3.connect('pypi_new4.db')
cur_meta = conn_meta.cursor()

conn_new = sqlite3.connect('pypi_meta_new_2022_local.db')
cur_new = conn_new.cursor()
cur_new.execute('''CREATE TABLE IF NOT EXISTS pypi_new
            (project_name text unique, downloads int, meta text, dev_status text, summary text, version text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')

results = [item1 for item1 in cur.execute('select * from pypi_stats where cast(downloads as int) > 500')]
count = len(results)


for item in tqdm(results):
    results_test = [itest for itest in cur_new.execute('select lower(project_name) from pypi_new where lower(project_name) = "{}"' .format(item[0].lower()))]
    if len(results_test) == 0:
        try:
            sql4 = "select project_name, classifiers, summary, version from pypi_meta where lower(project_name) = '{}' and classifiers like '%Topic%' order by dated desc limit 1" .format(item[0].lower())
            results2 = [item2 for item2 in cur_meta.execute(sql4)]
            try:
                summary1 = results2[0][2]
            except Exception:
                summary1 = 'none'
            try:
                version = results2[0][3]
            except Exception:
                version = 'none'
            try:
                topic = re.findall(r'"Topic :: (.+?)"', str(results2))
                topics = ','.join(topic)
            except Exception:
                topics = 'none'
            try:
                dev_status = re.search(r'"Development Status :: (.+?)"', str(results2))
                dev_stat = dev_status.group(1)
            except Exception:
                dev_stat = 'No status'
            stuff = item[0], int(item[1]), topics, dev_stat, summary1, version
            print(stuff)
            cur_new.execute('insert or ignore into pypi_new (project_name, downloads, meta, dev_status, summary, version) VALUES (?,?,?,?,?,?)', (stuff))
            cur_new.connection.commit()
        except Exception as e:
            print(e)
            print('skipping', item[0], item[1], topics, dev_stat)
    else:
        print('exists')
