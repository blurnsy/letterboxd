import json
import urllib.request
import time

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/blurnsy/letterboxd/main/movies.json'
MOVIES_CACHE = {'data': None, 'timestamp': 0}
CACHE_DURATION = 300

def fetch_movies_from_github():
    try:
        with urllib.request.urlopen(GITHUB_RAW_URL, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def load_movies():
    current_time = time.time()
    
    if MOVIES_CACHE['data'] and (current_time - MOVIES_CACHE['timestamp']) < CACHE_DURATION:
        return MOVIES_CACHE['data']
    
    movies = fetch_movies_from_github()
    
    if movies is None:
        return None
    
    for movie in movies:
        if isinstance(movie.get('score'), str):
            try:
                movie['score'] = float(movie['score'])
            except ValueError:
                movie['score'] = 0.0
    
    MOVIES_CACHE['data'] = movies
    MOVIES_CACHE['timestamp'] = current_time
    return movies

