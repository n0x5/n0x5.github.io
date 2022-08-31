# Create complete list of all versions of releases

import os
import re
from tqdm import tqdm
import sqlite3
from lxml import etree
import time

sql_db = os.path.join(os.path.dirname( __file__ ), 'Discogs_Releases_Database_2022-08_COMPLETE.db')
conn = sqlite3.connect(sql_db)
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists releases \
        (release_id text unique, title text, format_name text, artist_id text, label_name text, \
        catno text, country text, genres text, styles text, released text, track_p text, master_id text, artist_name text, \
        descriptions text)''')


xmlfile = 'discogs_20220801_releases.xml'

context = etree.iterparse(xmlfile, tag='release')
lst = []

for event, elem in tqdm(context):
    tree = etree.tostring(elem).decode()
    release = re.search(r'<release id="(\d+)" status="(.+?)">', tree)
    try:
        country = re.search(r'<country>(.+?)<\/country>', tree)
        country = country.group(1)
    except:
        country = 'None'
    try:
        label = re.search(r'<label name="(.+?)" catno="(.+?)" id="(.+?)"\/>', tree)
        try:
            label_name = label.group(1)
        except:
            label_name = 'None'
        try:
            catno = label.group(2)
        except:
            catno = 'None'
        try:
            label_id = label.group(3)
        except:
            label_id = 'None'
    except:
        label = 'None'
    try:
        genres = re.findall(r'<genre>(.+?)<\/genre>', tree)
    except:
        genres = 'None'
    try:
        styles = re.findall(r'<style>(.+?)<\/style>', tree)
    except:
        styles = 'None'
    try:
        year = re.search(r'<year>(.+?)<\/year>', tree)
        year = year.group(1)
    except:
        year = 'None'
    try:
        title = re.search(r'<title>(.+?)<\/title>', tree)
        title = title.group(1)
    except:
        title = 'None'
    try:
        data_quality = re.search(r'<data_quality>(.+?)<\/data_quality>', tree)
        data_quality = data_quality.group(1)
    except:
        data_quality = 'None'
    try:
        formats = re.search(r'<format name="(.+?)" qty="(\d{0,5}?)"', tree)
        try:
            format_name = formats.group(1)
        except:
            format_name = 'None'
        try:
            format_qty = formats.group(2)
        except:
            format_qty = 'None'
    except:
        formats = 'None'
    try:
        released = re.search(r'<released>(.+?)<\/released>', tree)
        released = released.group(1)
    except:
        released = 'None'
    try:
        notes = re.search(r'<notes>(.+?)<\/notes>', tree)
        notes = notes.group(1)
    except:
        notes = 'None'
    master_id = re.search(r'<master_id.+">(.+?)<\/master_id>', tree)
    try:
        master = master_id.group(1)
    except:
        master = 'None'
    artist_id = re.findall(r'<artist><id>(.+?)<\/id><name>(.+?)<\/name>', tree)
    art_lst = []
    for artis1 in artist_id:
        try:
            artis1 = artis1[0]+' '+artis1[1]+'\n'
            art_lst.append(artis1)
        except:
            artis1 = 'None'
    try:
        art_name = str(''.join(art_lst)).split('\n')[0]
        art_name = re.sub('^\d+ ', '', art_name)
    except:
        art_name = 'No artist name'
    try:
        tracklist = re.search(r'<tracklist>(.+?)<\/tracklist>', tree)
        tracks = re.findall(r'<track>(.+?)<\/track>', str(tracklist.group(1)))
        track_p = []
        for item9 in tracks:
            try:
                position = re.search(r'<position>(.+?)<\/position>', str(item9))
                track_title = re.search(r'<title>(.+?)<\/title>', str(item9))
                duration = re.search(r'<duration>(.+?)<\/duration>', str(item9))
                track_a = position.group(1)+' '+track_title.group(1)+' '+duration.group(1)+'\n'
                track_p.append(track_a)
            except:
                track_p = 'None'

    except:
        tracklist = 'None'
    try:
        descs = re.search(r'<descriptions>(.+?)<\/descriptions>', tree)
        descs = descs.group(1)
        try:
            descs = re.findall(r'<description>(.+?)<\/description>', str(descs))
        except:
            descs = ''
    except:
        descs = 'None'
        
    stuff = str(release.group(1)), str(title), str(format_name), str(''.join(art_lst)), str(label_name), str(catno),\
             str(country), str(', '.join(genres)), str(', '.join(styles)), str(released), str(''.join(track_p)), master, art_name, ', '.join(descs)
    lst.append(stuff)
    if len(lst) == 2000:
        cur.executemany('insert or ignore into releases (release_id, title, format_name, artist_id, label_name, \
                        catno, country, genres, styles, released, track_p, master_id, artist_name, descriptions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (lst))
        cur.connection.commit()
        lst = []


    elem.clear()
    for ancestor in elem.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]
del context