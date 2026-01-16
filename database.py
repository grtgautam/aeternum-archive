import sqlite3
import os
from datetime import datetime

DB_NAME = "capsules.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table for storing keys
    c.execute('''CREATE TABLE IF NOT EXISTS capsules
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  release_date TEXT NOT NULL,
                  decryption_key TEXT NOT NULL,
                  created_at TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def store_capsule_key(email, release_date, key_bytes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    key_str = key_bytes.decode('utf-8')
    c.execute("INSERT INTO capsules (email, release_date, decryption_key, created_at) VALUES (?, ?, ?, ?)",
              (email, release_date, key_str, datetime.now().isoformat()))
    # Get the ID to show the user or just confirm
    capsule_id = c.lastrowid
    conn.commit()
    conn.close()
    return capsule_id

def get_key_by_email_and_id(email, capsule_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT decryption_key, release_date FROM capsules WHERE email = ? AND id = ?", (email, capsule_id))
    result = c.fetchone()
    conn.close()
    return result
