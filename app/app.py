import sqlite3
import os
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

db = 'data/movies.db' 

def get_db_connection():
   print(f"Attempting to connect to: {db}")
   if not os.path.exists(db):
      print(f"Database file does not exist: {db}")
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