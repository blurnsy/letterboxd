import json
from shared import load_movies

def handler(request):
    try:
        movies = load_movies()
        if movies is None:
            return json.dumps({'error': 'Movies file not found. Please run the scraper first.'}), 404, {'Content-Type': 'application/json'}
        return json.dumps({'movies': movies}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

