#!/usr/bin/env python3
"""
seed_stations_asr.py — Load ASR District Police Stations into DB.
Usage:
    source venv/bin/activate
    python3 seed_stations_asr.py
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

import psycopg2
from urllib.parse import urlparse, parse_qs

db_url = os.getenv('DATABASE_URL', 'postgresql://ptms_user:ptms_pass@localhost:5432/ptms_db')
u = urlparse(db_url)
qs = parse_qs(u.query)
host = qs.get('host', [u.hostname or 'localhost'])[0]

conn = psycopg2.connect(
    dbname=u.path.lstrip('/'), user=u.username or 'ptms_user',
    password=u.password or 'ptms_pass', host=host, port=u.port or 5432
)
conn.autocommit = False
cur = conn.cursor()

# ── ASR District Police Stations ─────────────────────────────
stations = [

stations = [

    # ── Chintapalli Division ─────────────────────────────
    ('Mampa PS',              'PS_ASR_MAMPA',      'Chintapalli', 'SI_MAMPA'),
    ('Koyyuru PS',            'PS_ASR_KOYYURU',    'Chintapalli', 'SI_KOYYURU'),

    ('Chintapalli PS',        'PS_ASR_CHINT',      'Chintapalli', 'SI_CHINT'),
    ('Annavaram PS',          'PS_ASR_ANNAVARAM',  'Chintapalli', 'SI_ANNAVARAM'),

    ('G.K.Veedhi PS',         'PS_ASR_GKV',        'Chintapalli', 'SI_GKV'),
    ('Sileru PS',             'PS_ASR_SILERU',     'Chintapalli', 'SI_SILERU'),

    # ── Chinturu Division ─────────────────────────────
    ('Chinturu PS',           'PS_ASR_CTR',        'Chinturu', 'SI_CTR'),
    ('Moothugudem PS',        'PS_ASR_MGM',        'Chinturu', 'SI_MGM'),
    ('Donkarai PS',           'PS_ASR_DONKARAI',   'Chinturu', 'SI_DONKARAI'),

    ('Yetapaka PS',           'PS_ASR_YTP',        'Chinturu', 'SI_YTP'),
    ('Kunavaram PS',          'PS_ASR_KNVM',       'Chinturu', 'SI_KNVM'),
    ('VR Puram PS',           'PS_ASR_VRPM',       'Chinturu', 'SI_VRPM'),

    # ── RCVM Division ─────────────────────────────
    ('Addateegala PS',        'PS_ASR_ADT',        'RCVM', 'SI_ADT'),
    ('Dutcherthi PS',         'PS_ASR_DUTCHERTHI', 'RCVM', 'SI_DUTCHERTHI'),
    ('Gangavaram PS',         'PS_ASR_GANGAVARAM', 'RCVM', 'SI_GANGAVARAM'),
    ('Y Ramavaram PS',        'PS_ASR_YRMVM',      'RCVM', 'SI_YRMVM'),

    ('Rajavommangi PS',       'PS_ASR_RJVM',       'RCVM', 'SI_RJVM'),
    ('Jaddangi PS',           'PS_ASR_JADDANGI',   'RCVM', 'SI_JADDANGI'),

    ('Maredumilli PS',        'PS_ASR_MML',        'RCVM', 'SI_MML'),
    ('Gurthedu PS',           'PS_ASR_GRTD',       'RCVM', 'SI_GRTD'),

    ('Rampachodavaram PS',    'PS_ASR_RCVM',       'RCVM', 'SI_RCVM'),
    ('Devipatnam PS',         'PS_ASR_DVPM',       'RCVM', 'SI_DVPM'),

    # ── Paderu Division ─────────────────────────────
    ('Pedabayalu PS',         'PS_ASR_PEDABAYALU', 'Paderu', 'SI_PEDABAYALU'),
    ('G.Madugula PS',         'PS_ASR_GMD',        'Paderu', 'SI_GMD'),
    ('Munchingiput PS',       'PS_ASR_MUNCH',      'Paderu', 'SI_MUNCH'),

    ('Araku PS',              'PS_ASR_ARAKU',      'Paderu', 'SI_ARAKU'),
    ('Anantagiri PS',         'PS_ASR_ANANT',      'Paderu', 'SI_ANANT'),
    ('Dumbriguda PS',         'PS_ASR_DUMBRI',     'Paderu', 'SI_DUMBRI'),

    ('Paderu PS',             'PS_ASR_PDR',        'Paderu', 'SI_PDR'),
    ('Hukumpeta PS',          'PS_ASR_HKPT',       'Paderu', 'SI_HKPT'),

]

print("\n  ASR District — Seeding Police Stations\n  " + "─"*40)

ok = 0
fail = 0

for name, sid, division, sho_id in stations:
    try:
        cur.execute("SELECT name, rank FROM officers WHERE id=%s", (sho_id,))
        officer = cur.fetchone()
        if not officer:
            print(f"  ✗  {sid:<22} SHO not found: {sho_id}")
            fail += 1
            continue

        cur.execute("""
            INSERT INTO police_stations (name, station_id, division, sho_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (station_id) DO UPDATE
              SET name=%s, division=%s, sho_id=%s
        """, (name, sid, division, sho_id, name, division, sho_id))

        conn.commit()
        print(f"  ✅ {sid:<22} → {officer[1]:<12} {officer[0]}")
        ok += 1

    except Exception as e:
        conn.rollback()
        print(f"  ✗  {sid:<22} ERROR: {e}")
        fail += 1

cur.close()
conn.close()

print(f"\n  Done: {ok} inserted/updated, {fail} failed\n")
