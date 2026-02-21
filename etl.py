import pandas as pd
import requests
from sqlalchemy import create_engine, text
import re

API_KEY = "YOUR_REAL_OMDB_KEY"
DB_PATH = "sqlite:///movies.db"
SAMPLE_SIZE = 100

engine = create_engine(DB_PATH)

with open("schema.sql", "r", encoding="utf-8") as f:
    sql = f.read()

with engine.begin() as conn:
    for stmt in sql.split(";"):
        s = stmt.strip()
        if s:
            conn.execute(text(s))

movies_df = pd.read_csv("data/movies.csv")
ratings_df = pd.read_csv("data/ratings.csv")

def split_title_year(title):
    match = re.search(r"(.*)\((\d{4})\)", title)
    if match:
        return match.group(1).strip(), int(match.group(2))
    return title, None

movies_df[["clean_title", "release_year"]] = movies_df["title"].apply(
    lambda x: pd.Series(split_title_year(x))
)

movies_df["decade"] = (movies_df["release_year"] // 10) * 10

genres_df = movies_df[["movieId", "genres"]].copy()
genres_df["genres"] = genres_df["genres"].str.split("|")
genres_df = genres_df.explode("genres")
genres_df.columns = ["movie_id", "genre"]

ratings_df = ratings_df.rename(
    columns={"userId": "user_id", "movieId": "movie_id"}
)

cache = {}

def fetch_omdb(title, year):
    key = f"{title}_{year}"
    if key in cache:
        return cache[key]

    try:

        url = f"http://www.omdbapi.com/?t={title}&y={year}&apikey={API_KEY}"
        data = requests.get(url, timeout=5).json()


        if data.get("Response") != "True":
            url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
            data = requests.get(url, timeout=5).json()

        if data.get("Response") == "True":
            result = pd.Series([
                data.get("Director"),
                data.get("Plot"),
                data.get("BoxOffice")
            ])
        else:
            result = pd.Series([None, None, None])

    except:
        result = pd.Series([None, None, None])

    cache[key] = result
    return result

sample = movies_df.head(SAMPLE_SIZE).copy()

omdb_data = sample.apply(
    lambda r: fetch_omdb(r["clean_title"], r["release_year"]),
    axis=1
)

movies_df["director"] = None
movies_df["plot"] = None
movies_df["box_office"] = None

movies_df.loc[:SAMPLE_SIZE-1, ["director", "plot", "box_office"]] = omdb_data

movies_table = movies_df[
    ["movieId", "clean_title", "release_year", "decade", "director", "plot", "box_office"]
].copy()

movies_table.columns = [
    "movie_id",
    "title",
    "release_year",
    "decade",
    "director",
    "plot",
    "box_office"
]

with engine.begin() as conn:
    conn.execute(text("DELETE FROM genres"))
    conn.execute(text("DELETE FROM ratings"))
    conn.execute(text("DELETE FROM movies"))

    movies_table.to_sql("movies", conn, if_exists="append", index=False)
    genres_df.to_sql("genres", conn, if_exists="append", index=False)
    ratings_df.to_sql("ratings", conn, if_exists="append", index=False)

print("ETL completed successfully")