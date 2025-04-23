import sqlite3
import os
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Defining databases paths
main_db = 'data/movies.db'
test_db = 'data/test_movies.db'

# Setting correct database
db = main_db if os.path.exists(main_db) else test_db
print(f"Connecting to database: {db}")

def get_db_connection():
   conn = sqlite3.connect(db)
   conn.row_factory = sqlite3.Row

   return conn


def close_db_connection(conn):
   if conn:
      conn.close()


@app.route('/')
def homepage():
   return "The API is online"


@app.route('/movies', methods=['GET'])
def get_movies():

   conn = get_db_connection()
   cursor = conn.cursor()
   page = request.args.get('page', 1, type=int)
   per_page = request.args.get('per_page', 10, type=int)
   start = (page - 1) * per_page
   cursor.execute("SELECT title, id, release_date FROM movies LIMIT ?, ?", (start, per_page))
   movies = cursor.fetchall()
   close_db_connection(conn)

   return jsonify([dict(row) for row in movies])


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
   movie = cursor.fetchone()
   close_db_connection(conn)

   if movie:
      return jsonify(dict(movie))

   else:
      return jsonify({"message": "Movie not found"}), 404


@app.route('/movies/search', methods=['GET'])
def search_movies():

   title = request.args.get('title', '')
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, release_date FROM movies WHERE LOWER(title) LIKE ?", ('%' + title.lower() + '%',))
   results = cursor.fetchall()
   close_db_connection(conn)
   
   if results:
      return jsonify([dict(row) for row in results])
   
   else:
      return jsonify({"message": "No movies found for the given title."}), 404


@app.route('/movies/year/<int:year>', methods=['GET'])
def get_movies_by_year(year):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, release_date FROM movies WHERE strftime('%Y', release_date) = ?", (str(year),))
   results = cursor.fetchall()
   close_db_connection(conn)
   
   if results:
      return jsonify([dict(row) for row in results])
   
   else:
      return jsonify({"message": "No movies found for the given year."}), 404


@app.route('/movies/top-rated', methods=['GET'])
def get_top_rated():

   limit = request.args.get('limit', 10, type=int)
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, vote_average FROM movies ORDER BY vote_average DESC LIMIT ?", (limit,))
   results = cursor.fetchall()
   close_db_connection(conn)
   
   return jsonify([dict(row) for row in results])


@app.route('/movies/genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, genres FROM movies WHERE LOWER(genres) LIKE ?", ('%' + genre.lower() + '%',))
   results = cursor.fetchall()
   close_db_connection(conn)
   
   if results:
      return jsonify([dict(row) for row in results])
   
   else:
      return jsonify({"message": "No movies found for the given genre."}), 404
      

@app.route('/movies/language/<lang>', methods=['GET'])
def get_movies_by_language(lang):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, original_language FROM movies WHERE LOWER(original_language) = ?", (lang.lower(),))
   results = cursor.fetchall()
   close_db_connection(conn)

   if results:
      return jsonify([dict(row) for row in results])
   else:
      return jsonify({"message": "No movies found for the given language."}), 404


@app.route('/movies/country/<country>', methods=['GET'])
def get_movies_by_country(country):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, production_countries FROM movies WHERE LOWER(production_countries) LIKE ?", ('%' + country.lower() + '%',))
   results = cursor.fetchall()
   close_db_connection(conn)

   if results:
      return jsonify([dict(row) for row in results])
      
   else:
      return jsonify({"message": "No movies found for the given country."}), 404


@app.route('/movies/keyword/<keyword>', methods=['GET'])
def get_movies_by_keyword(keyword):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, keywords FROM movies WHERE LOWER(keywords) LIKE ?", ('%' + keyword.lower() + '%',))
   results = cursor.fetchall()
   close_db_connection(conn)

   if results:
      return jsonify([dict(row) for row in results])

   else:
      return jsonify({"message": "No movies found for the given keyword."}), 404


@app.route('/movies/company/<company>', methods=['GET'])
def get_movies_by_company(company):

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT id, title, production_companies FROM movies WHERE LOWER(production_companies) LIKE ?", ('%' + company.lower() + '%',))
   results = cursor.fetchall()
   close_db_connection(conn)

   if results:
      return jsonify([dict(row) for row in results])
   else:
      return jsonify({"message": "No movies found for the given production company."}), 404


@app.route('/genres', methods=['GET'])
def get_genres():

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT DISTINCT genres FROM movies")
   rows = cursor.fetchall()
   close_db_connection(conn)

   genres = set()
   for row in rows:
      if row["genres"]:
         genres.update([g.strip() for g in row["genres"].split(",")])

   return jsonify(sorted(genres))


@app.route('/production_companies', methods=['GET'])
def get_production_companies():

   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT DISTINCT production_companies FROM movies")
   rows = cursor.fetchall()
   close_db_connection(conn)

   companies = set()
   for row in rows:
      if row["production_companies"]:
         companies.update([c.strip() for c in row["production_companies"].split(",")])

   return jsonify(sorted(companies))
      

@app.errorhandler(Exception)
def handle_error(e):

   if isinstance(e, HTTPException):
      response = jsonify({"error": e.description})
      response.status_code = e.code
   
   else:
      response = jsonify({"error": "Internal Server Error"})
      response.status_code = 500
   
   return response

if __name__ == '__main__':
   app.run(debug=True)