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
            and (label_name not like 'maverick' and label_name not like '%universal%' and label_name not like 'jive' \
        and label_name not like '%TVT Records%' and label_name not like '%roadrunner%' and label_name not like '%Hollywood Records%' \
        and label_name not like '%reprise%' and label_name not like '%Arista%' and label_name not like '%Immortal Records%' and label_name not like 'American Recordings' \
        and label_name not like '%Wind-Up%' and label_name not like 'RCA' and label_name not like '%Wind-Up%' and label_name not like 'Mercury' \
        and label_name not like 'Elektra' and label_name not like 'Virgin%' and label_name not like 'Capitol Records' and label_name not like 'Sony%' \
        and label_name not like 'Rise%' and label_name not like 'columbia' and label_name not like 'Century Media' and label_name not like 'BMG%' \
        and label_name not like 'EMI' and label_name not like 'island records' and label_name not like 'warner%' and label_name not like 'interscope%' \
        and label_name not like 'geffen%' and label_name not like 'Another Century' and label_name not like 'atlantic' and label_name not like 'Lakeshore' \
        and label_name not like 'disney' and label_name not like 'dreamworks%' \
        and label_name not like 'American Recordings' and \
        label_name not like 'Caroline Records' and label_name not like 'epic' and label_name not like 'london records' \
        and label_name not like 'MCA Records' and label_name not like 'Polydor' and label_name not like 'Republic Records' \
        and label_name not like 'Rhino Records (2)' and label_name not like 'sire' and label_name not like 'vagrant records' \
        and label_name not like 'Volcano (2)' and label_name not like 'Zoo Entertainment' and label_name not like 'Tool Dissectional' \
        and label_name not like 'A&amp;M Records' and label_name not like 'Astralwerks' and label_name not like 'Naxos' \
        and label_name not like 'Deutsche Grammophon' and label_name not like 'Decca' and label_name not like '%Sarabande' \
        and label_name not like 'ECM Records' and label_name not like 'Ariola' and label_name not like 'Walt Disney Records' \
        and label_name not like 'Milan' and label_name not like 'Def Jam Recordings' \
        and label_name not like 'Parlophone' and label_name not like 'Mute' and label_name not like 'WaterTower Music') \
             group by master_id order by released desc" .format(section.lower()))]

with open('{}_Discogs_US_Indie_CD.html' .format(section), 'a', encoding='utf8') as log_file:
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