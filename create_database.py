import sqlite3
import pandas as pd

# Connect/Create database (creates file automatically)
conn = sqlite3.connect('placement_data.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS placements (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch TEXT,
        gpa REAL,
        test_score INTEGER,
        skills TEXT,
        work_experience INTEGER,
        company TEXT,
        package_placed REAL,
        placed INTEGER
    )
''')

# Insert 50+ sample records
sample_data = [
    ('CS', 8.5, 85, 'Python,ML,SQL', 1, 'Google', 25.0, 1),
    ('CS', 7.2, 72, 'Java,DS', 0, 'Microsoft', 18.0, 1),
    ('EC', 6.8, 65, 'Embedded,C', 0, 'TCS', 6.0, 1),
    ('CS', 9.0, 92, 'Python,DL', 2, 'Amazon', 32.0, 1),
    ('ME', 7.5, 70, 'CAD,Design', 0, 'Infosys', 8.0, 0),
    ('CS', 7.8, 82, 'Python,Web', 1, 'Wipro', 12.0, 1),
    ('EC', 6.5, 62, 'Hardware,VHDL', 0, 'HCL', 7.0, 1),
    ('ME', 8.2, 78, 'AutoCAD,SolidWorks', 1, 'Tata', 15.0, 1),
    ('CS', 8.0, 88, 'Python,Cloud', 0, 'Accenture', 14.0, 1),
    ('EC', 7.0, 75, 'IoT,Python', 1, 'Cognizant', 9.0, 1),
    ('CS', 6.9, 68, 'Java,React', 0, 'Capgemini', 7.5, 1),
    ('ME', 8.1, 80, 'SolidWorks,ANSYS', 2, 'L&T', 16.0, 1),
]

c.executemany('''
    INSERT OR IGNORE INTO placements 
    (branch, gpa, test_score, skills, work_experience, company, package_placed, placed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()

print("✅ Database 'placement_data.db' CREATED with 12 records!")
print("📁 File location: C:\\Users\\SIRISHA\\OneDrive\\Desktop\\project\\placement_data.db")
