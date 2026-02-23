{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os, socket, tkinter as tk\
from tkinter import ttk\
\
BASE = os.path.expanduser("~") + r"\\AppData\\Roaming\\BibleShow"\
HISTORY = os.path.join(BASE, "History.txt")\
BIBLES = os.path.join(BASE, "Bibles")\
\
# GUI for Progress\
root = tk.Tk()\
root.title("Lower-Thirds Sync")\
root.geometry("300x100")\
progress = ttk.Progressbar(root, length=200, mode='determinate')\
progress.pack(pady=20)\
\
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
sock.bind(("", 5005))\
\
def listen():\
    try:\
        data, addr = sock.recvfrom(65507)\
        msg = data.decode('utf-16', errors='ignore')\
        \
        if msg.startswith("SYNC"):\
            verse = msg.split("|")[1]\
            # Ensure verse is written to history to trigger display\
            with open(HISTORY, "a", encoding="utf-16") as f:\
                f.write("\\n" + verse)\
            print(f"Updated Lower-Third: \{verse\}")\
            \
        elif msg.startswith("FILE_START"):\
            progress['value'] = 50\
            root.update()\
            # Handle incoming Bible file...\
            \
    except: pass\
    root.after(500, listen)\
\
root.after(500, listen)\
root.mainloop()}