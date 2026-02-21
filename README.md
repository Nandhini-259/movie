# Movie Data Pipeline

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline using the MovieLens dataset. It reads movie and rating data from CSV files, enriches movie details using the OMDb API, and loads the processed data into a SQLite database for analysis.

## Repository Structure
Movie/
├── etl.py
├── schema.sql
├── queries.sql
└── README.md

## Database Design
The pipeline creates the following normalized tables:
- movies — movie details and enriched metadata
- genres — normalized genre information
- ratings — user rating data

Genres are stored separately to maintain relational normalization and avoid duplication.

## Data Sources
- MovieLens Small Dataset (movies.csv, ratings.csv)  
  Download: https://grouplens.org/datasets/movielens/latest/
- OMDb API (Director, Plot, Box Office)

Note: Dataset CSV files are not included in this repository. After downloading the MovieLens small dataset, place the following files in the project root directory:
- movies.csv
- ratings.csv

## Setup Instructions
Install dependencies:
pip install -r requirements.txt

Add your OMDb API key inside etl.py.

Run the ETL pipeline:
python etl.py

A SQLite database (movies.db) will be created and populated automatically.

## Assumptions
- Movie titles may not exactly match OMDb entries
- Only the first 100 movies are enriched due to API limits
- Missing API data is stored as NULL
- The ETL process is idempotent (safe to re-run)

## Challenges
- Matching MovieLens titles with OMDb results
- Handling missing or inconsistent API responses
- Managing API rate limits

## Possible Improvements
- Use PostgreSQL instead of SQLite
- Cache OMDb responses to reduce API calls
- Schedule ETL using Airflow
- Implement incremental loading instead of full reload