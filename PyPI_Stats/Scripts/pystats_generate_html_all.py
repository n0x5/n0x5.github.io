import os
import sqlite3
from tqdm import tqdm
import re

conn_new = sqlite3.connect('pypi_meta_new_2022_local.db')
cur_new = conn_new.cursor()

section = 'all'

results = [itest for itest in cur_new.execute('select project_name, downloads, meta, dev_status, summary from pypi_new')]

with open('{}.html' .format(section), 'a', encoding='utf8') as log_file:
    log_file.write('<style>table, th, td {border: 1px solid;border-collapse:collapse;padding:4px;}a {text-decoration:none;}</style>')
    log_file.write('<h1>List of Pypi {} packages</h1>' .format(section))
    log_file.write('<table>')
    log_file.write('<tr><td><h3>Name</h3></td><td><h3>Downloads</h3></td><td><h3>Categories</h3></td><td><h3>Status</h3></td><td><h3>Description</h3></td></h3></tr>')
    for item in results:
        log_file.write('<tr>')
        log_file.write('<td><a href="https://pypi.org/project/{}">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>'.format(item[0], item[0], item[1], item[2], item[3], item[4]))
        log_file.write('</tr>')
        print(item)
    log_file.write('</table>')