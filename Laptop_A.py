{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os, socket, time\
\
# BibleShow paths\
BASE = os.path.expanduser("~") + r"\\AppData\\Roaming\\BibleShow"\
HISTORY = os.path.join(BASE, "History.txt")\
BIBLES = os.path.join(BASE, "Bibles")\
\
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)\
\
def get_last_verse():\
    try:\
        with open(HISTORY, "r", encoding="utf-16") as f:\
            return f.readlines()[-1].strip()\
    except: return None\
\
print("FOLDBACK MASTER: Running...")\
last_v = get_last_verse()\
\
while True:\
    curr_v = get_last_verse()\
    if curr_v and curr_v != last_v:\
        # Format: SYNC|Book Chapter:Verse|Version\
        sock.sendto(f"SYNC|\{curr_v\}".encode('utf-16'), ('<broadcast>', 5005))\
        print(f"Sent to Lower-Thirds: \{curr_v\}")\
        last_v = curr_v\
    \
    # Listen for Bible File requests from Slave\
    sock.settimeout(0.1)\
    try:\
        data, addr = sock.recvfrom(1024)\
        msg = data.decode('utf-16')\
        if msg.startswith("GET_BIBLE"):\
            ver = msg.split("|")[1]\
            b_path = os.path.join(BIBLES, f"\{ver\}.bsv")\
            if os.path.exists(b_path):\
                with open(b_path, "rb") as f:\
                    sock.sendto(b"FILE_START|" + ver.encode('utf-16'), addr)\
                    sock.sendto(f.read(), addr)\
    except: pass\
    time.sleep(0.5)}