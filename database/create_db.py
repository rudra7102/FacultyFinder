import sqlite3

conn = sqlite3.connect("data/faculty.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS faculty (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    email TEXT,
    phone TEXT,
    office TEXT,
    phd TEXT,
    biography TEXT,
    specialization TEXT,
    teaching TEXT,
    search_text TEXT,
    source_url TEXT

)

""")

conn.commit()

conn.close()

print("Database created successfully")