import pandas as pd
import sqlite3

# Open dataframe
df = pd.read_csv("data/processed_movies.csv")
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').astype(str)
df = df.where(pd.notnull(df), None)

# Removing non-necessary columns
columns_rm = ['vote_count', 'backdrop_path', 'homepage', 'poster_path']
df.drop(columns=columns_rm, inplace=True)

# Schema SQL
schema_sql = """
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
"""

# Create complete database
conn_full = sqlite3.connect("data/movies.db")
cursor_full = conn_full.cursor()
cursor_full.execute("DROP TABLE IF EXISTS movies")
cursor_full.execute(schema_sql)
df.to_sql("movies", conn_full, if_exists="append", index=False)
conn_full.commit()
conn_full.close()

# Creating test database
df_test = df.head(100000)
conn_test = sqlite3.connect("data/test_movies.db")
cursor_test = conn_test.cursor()
cursor_test.execute("DROP TABLE IF EXISTS movies")
cursor_test.execute(schema_sql)
df_test.to_sql("movies", conn_test, if_exists="append", index=False)
conn_test.commit()
conn_test.close()