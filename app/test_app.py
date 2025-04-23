import pytest
from app import app

@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
      yield client


def test_homepage(client):
   response = client.get('/')
   assert response.status_code == 200
   assert b"The API is online" in response.data


def test_get_movies(client):
   response = client.get('/movies')
   assert response.status_code == 200
   assert isinstance(response.json, list)
   

def test_get_movie_by_id(client):   
   response = client.get('/movies/2')
   assert response.status_code in [200, 404]

def test_search_movies(client):
   response = client.get('/movies/search?title=the')
   assert response.status_code in [200, 404]

def test_get_movies_by_year(client):
   response = client.get('/movies/year/2000')
   assert response.status_code in [200, 404]


def test_top_rated(client):
   response = client.get('/movies/top-rated?limit=5')
   assert response.status_code == 200
   assert isinstance(response.json, list)


def test_movies_by_genre(client):
   response = client.get('/movies/genre/action')
   assert response.status_code in [200, 404]


def test_movies_by_language(client):
   response = client.get('/movies/language/en')
   assert response.status_code in [200, 404]


def test_movies_by_country(client):
   response = client.get('/movies/country/united states of america')
   assert response.status_code in [200, 404]


def test_movies_by_keyword(client):
   response = client.get('/movies/keyword/love')
   assert response.status_code in [200, 404]


def test_movies_by_company(client):
   response = client.get('/movies/company/warner')
   assert response.status_code in [200, 404]


def test_get_genres(client):
   response = client.get('/genres')
   assert response.status_code in [200, 404]


def test_get_production_companies(client):
   response = client.get('/production_companies')
   assert response.status_code in [200, 404]
