import os
import sqlite3
from tqdm import tqdm
import re

conn_new = sqlite3.connect('Discogs_Releases_Database_2022-08_COMPLETE.db')
cur_new = conn_new.cursor()

section = ''

results = [itest for itest in cur_new.execute("select master_id, artist_name, title, catno, label_name, country, min(released), genres, styles, \
            descriptions from releases where descriptions like '%blu%ray%' or format_name like '%Blu%ray%' \
            group by master_id order by artist_name asc")]

with open('{}_Discogs_US_Blu-ray.html' .format(section), 'a', encoding='utf8') as log_file:
    log_file.write('<style>table, th, td {border: 1px solid;border-collapse:collapse;padding:4px;}a {text-decoration:none;}</style>')
    log_file.write('<h1>List of Discogs {} releases</h1>' .format(section))
    log_file.write('<table>')
    log_file.write('<tr><td><h3>Master ID</h3></td><td><h3>Album</h3></td><td><h3>Cat #</h3></td><td><h3>Label</h3></td><td><h3>Country</h3></td><td><h3>Date</h3></td><td><h3>Genres</h3></td><td><h3>Styles</h3></td><td><h3>Info</h3></td></h3></tr>')
    for item in tqdm(results):
        log_file.write('<tr>')
        log_file.write('<td><a href="https://www.discogs.com/master/{}">{}</a></td><td>{} - {}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>' \
                        .format(item[0], item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))
        log_file.write('</tr>')
        #print(item)
    log_file.write('</table>')