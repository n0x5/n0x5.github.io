from google.cloud import bigquery
from google.oauth2 import service_account
import os
import sqlite3
from tqdm import tqdm

conn2 = sqlite3.connect('pypi_new_2022_max1.db')
cur = conn2.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS pypi_stats
            (project_name text, downloads text, version text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


key_path = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

project_id = 'PROJECT_ID'
client = bigquery.Client(credentials= credentials, project=project_id,)

sql4 = 'select file.project, count(project) c, split(file.version, ".") from `bigquery-public-data.pypi.file_downloads` where date(timestamp) = "2022-08-11" group by project order by c desc'
query_job = client.query(sql4)

results = query_job.result()

lst = []
for item in results:
    stuff = item[0], item[1], item[2]
    lst.append(stuff)
    if len(lst) == 5000:
        cur.executemany('insert or ignore into pypi_stats (project_name, downloads, version) VALUES (?,?,?)', (lst))
        cur.connection.commit()
        lst = []
