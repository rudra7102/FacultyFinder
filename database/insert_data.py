import sqlite3
import pandas as pd

df = pd.read_csv(
    "data/processed/final_combined_faculty.csv"
)

conn = sqlite3.connect("data/faculty.db")

df.to_sql(
    "faculty",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Faculty data inserted successfully")