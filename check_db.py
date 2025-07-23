import sqlite3

#!/usr/bin/env python3

try:
    conn = sqlite3.connect('ehb5.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('Database tables:', [table[0] for table in tables])
    conn.close()
except Exception as e:
    print(f"Error checking database: {e}")
