import sqlite3
import pandas as pd   # ← ADD THIS LINE!

conn = sqlite3.connect('placement_data.db')
df = pd.read_sql_query("SELECT COUNT(*) as count FROM placements", conn)
print(f"✅ Database working! Records: {df['count'][0]}")
conn.close()
