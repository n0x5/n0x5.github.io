from google.cloud import bigquery
from google.oauth2 import service_account
import os
import sqlite3
from tqdm import tqdm

conn2 = sqlite3.connect('pypi_new4.db')
cur = conn2.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS pypi_meta
            (project_name text, classifiers text, summary text, description text, version text, keywords text, platform text, dated datetime DEFAULT CURRENT_TIMESTAMP)''')


key_path = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

project_id = 'PROJECT_ID'
client = bigquery.Client(credentials= credentials, project=project_id,)

sql4 = 'SELECT name, TO_JSON_STRING(classifiers), summary, description, version, keywords, TO_JSON_STRING(platform) FROM `bigquery-public-data.pypi.distribution_metadata` group by name, TO_JSON_STRING(classifiers), summary, description, version, keywords, TO_JSON_STRING(platform)'
query_job = client.query(sql4)

results = query_job.result()

lst = []
for item in results:
    stuff = item[0], item[1], item[2], item[3], item[4], item[5], item[6]
    lst.append(stuff)
    if len(lst) == 5000:
        cur.executemany('insert or ignore into pypi_meta (project_name, classifiers, summary, description, version, keywords, platform) VALUES (?,?,?,?,?,?,?)', (lst))
        cur.connection.commit()
        lst = []
