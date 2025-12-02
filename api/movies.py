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

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            movies = load_movies()
            if movies is None:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Movies file not found. Please run the scraper first.'}).encode('utf-8'))
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'movies': movies}).encode('utf-8'))
        except Exception as e:
            import traceback
            error_msg = str(e) + '\n' + traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': error_msg}).encode('utf-8'))

