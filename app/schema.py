import pandas as pd
import sqlite3

# Open dataframe
df = pd.read_csv("data/movies.csv")
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').astype(str)
df = df.where(pd.notnull(df), None)

# Connect to database
conn = sqlite3.connect("data/movies.db")
cursor = conn.cursor()

# Database schema
cursor.execute("DROP TABLE IF EXISTS movies")
cursor.execute("""
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    vote_average REAL,
    status TEXT,
    release_date TEXT,
    revenue INTEGER,
    runtime INTEGER,
    adult BOOLEAN,
    budget INTEGER,
    imdb_id TEXT,
    original_language TEXT,
    original_title TEXT,
    overview TEXT,
    popularity REAL,
    tagline TEXT,
    genres TEXT,
    production_companies TEXT,
    production_countries TEXT,
    spoken_languages TEXT,
    keywords TEXT
)
""")

# Insert data
df.to_sql("movies", conn, if_exists="append", index=False)

conn.commit()
conn.close()