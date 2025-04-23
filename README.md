# IMDB API - Technical Challenge

This project was developed as part of a technical challenge. It includes processing a large movie dataset and exposing it through a Flask-based REST API.

## Project Structure

```
IMDB_API/
├── app/                      # Flask app
│   ├── app.py                # Main API with all routes
│   ├── schema.py             # Dataset processing and database creation
│   └── test_app.py           # Pytest tests for API endpoints
|
├── data/                     # Data folder
|   ├── movies.csv            # Original dataset
│   ├── movies.db             # Full DB (ignored by Git)
│   ├── processed_movies.csv  # Processed dataset
│   └── test_movies.db        # 100k records DB for testing
|
├── clean_dataset.ipynb       # Preprocessing notebook
├── README.md
└── requirements.txt
```

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Preprocess dataset
```bash
jupyter notebook clean_dataset.ipynb 
```

This will generate:
- `processed_movies.csv` cleaned and ready for loading

### 3. Generate the SQLite databases
```bash
python app/schema.py
```
This will create:
- `movies.db` with the full dataset
- `test_movies.db` with the first 100,000 rows

### 3. Run the API
```bash
python app/app.py
```

API will start at: http://127.0.0.1:5000

If `movies.db` is not found, `test_movies.db` will be used automatically.

## Available Endpoints

| Method | Endpoint                            | Description                                  |
|--------|-------------------------------------|----------------------------------------------|
| GET    | `/`                                 | Check if API is online                       |
| GET    | `/movies`                           | Paginated list of movies                     |
| GET    | `/movies/<id>`                      | Movie by ID                                  |
| GET    | `/movies/search?title=...`          | Search movies by title                       |
| GET    | `/movies/year/<year>`               | Movies released in a specific year           |
| GET    | `/movies/top-rated?limit=N`         | Top N movies by rating                       |
| GET    | `/movies/genre/<genre>`             | Movies by genre                              |
| GET    | `/movies/language/<lang>`           | Movies by original language                  |
| GET    | `/movies/country/<country>`         | Movies by production country                 |
| GET    | `/movies/keyword/<keyword>`         | Movies by keyword                            |
| GET    | `/movies/company/<company>`         | Movies by production company                 |
| GET    | `/genres`                           | List of unique genres                        |
| GET    | `/production_companies`             | List of unique production companies          |

## Testing

### Run all tests
```bash
pytest
```

Tests are written using `pytest` and validate all endpoints.

## Technical Notes

- Dataset: [Kaggle TMDB 2023](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
- Database: SQLite
- API: Flask
- Tests: Pytest

## Author & License

Developed for technical assessment purposes.
