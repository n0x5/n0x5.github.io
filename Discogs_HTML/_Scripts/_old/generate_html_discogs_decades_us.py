import os
import sqlite3
from tqdm import tqdm
import re

conn_new = sqlite3.connect('Discogs_Releases_Database_2022-12_COMPLETE_CD_ONLY.db')
cur_new = conn_new.cursor()

sections = ['Screen', 'Classical', 'Folk', 'Hip Hop', 'Pop', 'Electronic', 'Rock']
decades = ['202', '201', '200', '199', '198']

for year in decades:
    for section in sections:
        results = [itest for itest in cur_new.execute("select master_id, artist_name, title, catno, label_name, country, min(released), genres, styles, \
                    descriptions from releases where descriptions like '%album%' \
                    and format_name like 'cd' and descriptions not like '%reissue%' and descriptions not like '%repress%' and released like '{}%' \
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
                or label_name like 'MCA%' or label_name like 'Polydor' or label_name like 'Republic Records' \
                or label_name like 'Rhino Records (2)' or label_name like 'sire' or label_name like 'vagrant records' \
                or label_name like 'Volcano (2)' or label_name like 'Zoo Entertainment' or label_name like 'Tool Dissectional' \
                or label_name like 'A&amp;M Records' or label_name like 'Astralwerks' or label_name like 'Naxos' \
                or label_name like 'Deutsche Grammophon' or label_name like 'Decca' or label_name like 'Var&#232;se Sarabande%' \
                or label_name like 'ECM Records' or label_name like 'Ariola' or label_name like 'Walt Disney Records' \
                or label_name like 'Milan' or label_name like 'Def Jam Recordings'  \
                or label_name like 'Parlophone' or label_name like 'Mute' or label_name like 'WaterTower Music' or label_name like 'UMe' \
                or label_name like 'T-Boy Records' or label_name like 'Verve Records' or label_name like 'Verve Forecast' \
                or label_name like 'Streamline Records' or label_name like 'Octone Records' or label_name like 'Fueled By Ramen' \
                or label_name like 'Sanctuary Records' or label_name like 'Shrapnel Records' or label_name like 'The Rocket Record Company') \
                group by master_id order by released desc" .format(year, section.lower()))]

        with open('{}0s_{}_Discogs_US_Major_CD.html' .format(year, section), 'w', encoding='utf8') as log_file:
            log_file.write('<style>table, th, td {border: 1px solid;border-collapse:collapse;padding:4px;}a {text-decoration:none;}</style>')
            log_file.write('<h1>List of Discogs {} releases</h1>' .format(section))
            log_file.write('<table>')
            log_file.write('<tr><td><h3>Master ID</h3></td><td><h3>Album</h3></td><td><h3>Cat #</h3></td><td><h3>Label</h3></td><td><h3>Country</h3></td><td><h3>Date</h3></td><td><h3>Genres</h3></td><td><h3>Styles</h3></td><td><h3>Info</h3></td></h3></tr>')
            for item in tqdm(results):
                log_file.write('<tr>')
                log_file.write('<td><a href="https://www.discogs.com/master/{}">{}</a></td><td>{} - {}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>' \
                                .format(item[0], item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))
                log_file.write('</tr>')
            log_file.write('</table>')



for year in decades:
    for section in sections:
        results = [itest for itest in cur_new.execute("select master_id, artist_name, title, catno, label_name, country, min(released), genres, styles, \
                    descriptions from releases where descriptions like '%album%' \
                    and format_name like 'cd' and descriptions not like '%reissue%' and descriptions not like '%repress%' and released like '{}%' \
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
                and label_name not like 'MCA%' and label_name not like 'Polydor' and label_name not like 'Republic Records' \
                and label_name not like 'Rhino Records (2)' and label_name not like 'sire' and label_name not like 'vagrant records' \
                and label_name not like 'Volcano (2)' and label_name not like 'Zoo Entertainment' and label_name not like 'Tool Dissectional' \
                and label_name not like 'A&amp;M Records' and label_name not like 'Astralwerks' and label_name not like 'Naxos' \
                and label_name not like 'Deutsche Grammophon' and label_name not like 'Decca' and label_name not like '%Sarabande' \
                and label_name not like 'ECM Records' and label_name not like 'Ariola' and label_name not like 'Walt Disney Records' \
                and label_name not like 'Milan' and label_name not like 'Def Jam Recordings' \
                and label_name not like 'Parlophone' and label_name not like 'Mute' and label_name not like 'WaterTower Music' and label_name not like 'UMe' \
                and label_name not like 'T-Boy Records' and label_name not like 'Verve Records' and label_name not like 'Verve Forecast' \
                and label_name not like 'Streamline Records' and label_name not like 'Octone Records' and label_name not like 'Fueled By Ramen' \
                and label_name not like 'Sanctuary Records' and label_name not like 'Shrapnel Records' and label_name not like 'The Rocket Record Company') \
                group by master_id order by released desc" .format(year, section.lower()))]

        with open('{}0s_{}_Discogs_US_Indie_CD.html' .format(year, section), 'w', encoding='utf8') as log_file:
            log_file.write('<style>table, th, td {border: 1px solid;border-collapse:collapse;padding:4px;}a {text-decoration:none;}</style>')
            log_file.write('<h1>List of Discogs {} releases</h1>' .format(section))
            log_file.write('<table>')
            log_file.write('<tr><td><h3>Master ID</h3></td><td><h3>Album</h3></td><td><h3>Cat #</h3></td><td><h3>Label</h3></td><td><h3>Country</h3></td><td><h3>Date</h3></td><td><h3>Genres</h3></td><td><h3>Styles</h3></td><td><h3>Info</h3></td></h3></tr>')
            for item in tqdm(results):
                log_file.write('<tr>')
                log_file.write('<td><a href="https://www.discogs.com/master/{}">{}</a></td><td>{} - {}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>' \
                                .format(item[0], item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))
                log_file.write('</tr>')
            log_file.write('</table>')




