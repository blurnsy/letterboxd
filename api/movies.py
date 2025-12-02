import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from shared import load_movies
except ImportError as e:
    import traceback
    error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}\nCurrent dir: {current_dir}\nSys path: {sys.path}"
    def load_movies():
        raise Exception(error_msg)

def handler(request):
    try:
        movies = load_movies()
        if movies is None:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Movies file not found. Please run the scraper first.'})
            }
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'movies': movies})
        }
    except Exception as e:
        import traceback
        error_msg = str(e) + '\n' + traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': error_msg})
        }

