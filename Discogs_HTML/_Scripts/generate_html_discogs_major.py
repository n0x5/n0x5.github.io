import os
import sqlite3
from tqdm import tqdm
import re

conn_new = sqlite3.connect('Discogs_Releases_Database_2022-08_COMPLETE.db')
cur_new = conn_new.cursor()

section = 'Screen'

results = [itest for itest in cur_new.execute("select master_id, artist_name, title, catno, label_name, country, min(released), genres, styles, \
            descriptions from releases where descriptions like '%album%' \
            and format_name like 'cd' and descriptions not like '%reissue%' and descriptions not like '%repress%' \
            and descriptions not like '%remastered%' and genres like '%{}%' and country like 'us' and released not like 'none' \
            and (label_name like 'maverick' or label_name like 'Universal%' or label_name like 'jive' \
        or label_name like '%TVT Records%' or label_name like '%roadrunner%' or label_name like '%Hollywood Records%' \
        or label_name like '%reprise%' or label_name like '%Arista%' or label_name like '%Immortal Records%' or label_name like 'American Recordings' \
        or label_name like '%Wind-Up%' or label_name like 'RCA' or label_name like '%Wind-Up%' or label_name like 'Mercury' \
        or label_name like 'Elektra' or label_name like 'Virgin%' or label_name like 'Capitol Records' or label_name like 'Sony%' \
        or label_name like 'Rise Records (3)' or label_name like 'columbia' or label_name like 'Century Media' or label_name like 'BMG%' \
        or label_name like 'EMI' or label_name like 'island records' or label_name like 'warner%' or label_name like 'interscope%' \
        or label_name like 'geffen%' or label_name like 'Another Century' or label_name like 'atlantic' or label_name like 'Lakeshore' \
        or label_name like 'disney' or label_name like 'dreamworks%' or label_name like 'American Recordings' or \
        label_name like 'Caroline Records' or label_name like 'epic' or label_name like 'london records' \
        or label_name like 'MCA Records' or label_name like 'Polydor' or label_name like 'Republic Records' \
        or label_name like 'Rhino Records (2)' or label_name like 'sire' or label_name like 'vagrant records' \
        or label_name like 'Volcano (2)' or label_name like 'Zoo Entertainment' or label_name like 'Tool Dissectional' \
        or label_name like 'A&amp;M Records' or label_name like 'Astralwerks' or label_name like 'Naxos' \
        or label_name like 'Deutsche Grammophon' or label_name like 'Decca' or label_name like 'Var&#232;se Sarabande%' \
        or label_name like 'ECM Records' or label_name like 'Ariola' or label_name like 'Walt Disney Records' \
        or label_name like 'Milan' or label_name like 'Def Jam Recordings'  \
        or label_name like 'Parlophone' or label_name like 'Mute' or label_name like 'WaterTower Music') \
             group by master_id order by released desc" .format(section.lower()))]

with open('{}_Discogs_US_Major_CD.html' .format(section), 'a', encoding='utf8') as log_file:
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