import json
import sys
import os

sys.path.append(os.path.dirname(__file__))
from shared import load_movies

def handler(request):
    try:
        movies = load_movies()
        if movies is None:
            return json.dumps({'error': 'Movies file not found. Please run the scraper first.'}), 404, {'Content-Type': 'application/json'}
        return json.dumps({'movies': movies}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        import traceback
        error_msg = str(e) + '\n' + traceback.format_exc()
        return json.dumps({'error': error_msg}), 500, {'Content-Type': 'application/json'}

