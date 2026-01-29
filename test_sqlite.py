import sqlite3
conn = sqlite3.connect(':memory:')
print("✅ SQLite3 is working perfectly!")
conn.close()
