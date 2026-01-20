# Create complete list of all versions of releases (FINAL – EXACT MATCH)

import os
import sqlite3
from lxml import etree
from tqdm import tqdm

sql_db = os.path.join(
    os.path.dirname(__file__),
    'Discogs_Releases_Database_2026_01_COMPLETE_CD_ONLY.db'
)

conn = sqlite3.connect(sql_db)
cur = conn.cursor()

cur.execute("PRAGMA journal_mode=WAL")
cur.execute("PRAGMA synchronous=NORMAL")

cur.execute("""
CREATE TABLE IF NOT EXISTS releases (
    release_id TEXT UNIQUE,
    title TEXT,
    format_name TEXT,
    artist_id TEXT,
    label_name TEXT,
    catno TEXT,
    country TEXT,
    genres TEXT,
    styles TEXT,
    released TEXT,
    track_p TEXT,
    master_id TEXT,
    artist_name TEXT,
    descriptions TEXT
)
""")

xmlfile = 'discogs_20260101_releases.xml'
context = etree.iterparse(xmlfile, tag='release')

batch = []
BATCH_SIZE = 2000

with conn:
    for _, elem in tqdm(context):

        release_id = elem.get("id")
        country = elem.findtext("country", "")

        if "US" not in country:
            elem.clear()
            continue

        formats = elem.findall("formats/format")

        is_cd = False
        format_name = ""

        for f in formats:
            name = f.get("name", "")
            if "CD" in name:
                is_cd = True
                format_name = name
                break

        if not is_cd:
            elem.clear()
            continue

        title = elem.findtext("title", "")
        released = elem.findtext("released", "")
        master_id = elem.findtext("master_id", "")

        label_el = elem.find("labels/label")
        label_name = label_el.get("name", "") if label_el is not None else ""
        catno = label_el.get("catno", "") if label_el is not None else ""

        genres = ", ".join(g.text for g in elem.findall("genres/genre") if g.text)
        styles = ", ".join(s.text for s in elem.findall("styles/style") if s.text)

        artist_entries = []
        for artist in elem.findall("artists/artist"):
            aid = artist.findtext("id", "")
            aname = artist.findtext("name", "")
            if aid or aname:
                artist_entries.append(f"{aid} {aname}")

        artist_id = "\n".join(artist_entries)
        artist_name = artist_entries[0].split(" ", 1)[-1] if artist_entries else ""

        track_lines = []
        for track in elem.findall("tracklist/track"):
            pos = track.findtext("position", "")
            ttitle = track.findtext("title", "")
            dur = track.findtext("duration", "")
            if pos or ttitle or dur:
                track_lines.append(f"{pos} {ttitle} {dur}")

        track_p = "\n".join(track_lines)



        descriptions_list = []

        for f in elem.findall("formats/format"):
            for d in f.findall("descriptions/description"):
                if d.text:
                    descriptions_list.append(d.text)

        descriptions = ", ".join(descriptions_list)

        batch.append((
            release_id, title, format_name, artist_id, label_name, catno,
            country, genres, styles, released, track_p,
            master_id, artist_name, descriptions
        ))

        if len(batch) >= BATCH_SIZE:
            cur.executemany("""
                INSERT OR IGNORE INTO releases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, batch)
            batch.clear()

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    if batch:
        cur.executemany("""
            INSERT OR IGNORE INTO releases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, batch)

del context
conn.commit()
conn.close()
