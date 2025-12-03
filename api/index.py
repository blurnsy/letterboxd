HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Letterboxd Movie Recommendation Wheel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #fafafa;
            min-height: 100vh;
            padding: 20px;
            color: #1a1a1a;
            line-height: 1.5;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 4px;
            color: #1a1a1a;
            letter-spacing: -1px;
        }
        
        .subtitle {
            font-size: 16px;
            color: #666;
            margin-bottom: 12px;
            font-weight: 400;
        }
        
        .wheel-section {
            background: white;
            border-radius: 12px;
            padding: 32px 24px;
            border: 1px solid #e5e5e5;
            margin-bottom: 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .wheel-container {
            position: relative;
            width: 320px;
            height: 320px;
            margin: 0 auto 24px;
        }
        
        .wheel {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid #1a1a1a;
            background: conic-gradient(
                from 0deg,
                #f5f5f5 0deg 30deg,
                #e8e8e8 30deg 60deg,
                #f5f5f5 60deg 90deg,
                #e8e8e8 90deg 120deg,
                #f5f5f5 120deg 150deg,
                #e8e8e8 150deg 180deg,
                #f5f5f5 180deg 210deg,
                #e8e8e8 210deg 240deg,
                #f5f5f5 240deg 270deg,
                #e8e8e8 270deg 300deg,
                #f5f5f5 300deg 330deg,
                #e8e8e8 330deg 360deg
            );
            position: relative;
            transition: transform 3s cubic-bezier(0.17, 0.67, 0.12, 0.99);
            transform: rotate(0deg);
        }
        
        .wheel-pointer {
            position: absolute;
            top: -16px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-top: 24px solid #1a1a1a;
            z-index: 10;
        }
        
        .selected-movie-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        
        .selected-movie-overlay.visible {
            opacity: 1;
            pointer-events: all;
        }
        
        .selected-movie {
            position: relative;
            padding: 32px;
            background: white;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 20px;
            max-width: 90vw;
            max-height: 90vh;
            overflow: auto;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }
        
        .selected-movie-overlay.visible .selected-movie {
            transform: scale(1);
        }
        
        .selected-movie-close {
            position: absolute;
            top: 12px;
            right: 12px;
            background: none;
            border: none;
            font-size: 28px;
            color: #666;
            cursor: pointer;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
            z-index: 10;
        }
        
        .selected-movie-close:hover {
            background: #f5f5f5;
            color: #1a1a1a;
        }
        
        .selected-movie-poster {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: block;
        }
        
        .selected-movie-link {
            font-size: 20px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 4px;
            text-align: center;
            text-decoration: underline;
            width: 100%;
            cursor: pointer;
        }
        
        .selected-movie-link:hover {
            color: #40bcf4;
            text-decoration: none;
        }
        
        .selected-movie-score {
            font-size: 14px;
            color: #666;
        }

        .selected-movie-genres {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-top: 4px;
        }

        .genre-tag {
            background: #f5f5f5;
            color: #666;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 600;
        }

        .selected-movie-description {
            font-size: 14px;
            color: #444;
            line-height: 1.6;
            text-align: center;
            max-width: 600px;
            margin-top: 8px;
            overflow-y: auto;
            max-height: 150px;
            padding: 0 12px;
        }
        
        .spin-button {
            background: #1a1a1a;
            color: white;
            border: none;
            padding: 12px 32px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
            margin-top: 0;
        }
        
        .spin-button:hover {
            background: #333;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .spin-button:active {
            background: #000;
            transform: translateY(0);
        }
        
        .spin-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .stats {
            display: inline-flex;
            gap: 16px;
            font-size: 14px;
            color: #666;
            margin-bottom: 16px;
        }
        
        .stat-item {
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-value {
            font-weight: 700;
            color: #1a1a1a;
            display: inline;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Letterboxd Wheel</h1>
        <div class="subtitle">Random Selection From Popular Films This Week</div>
        
        <div class="stats">
            <div class="stat-item">
                Total Movies: <span class="stat-value" id="totalMovies">0</span>
            </div>
            <div class="stat-item">
                Average Score: <span class="stat-value" id="averageScore">0.0</span>
            </div>
        </div>
        
        <div class="wheel-section">
            <div class="wheel-container">
                <div class="wheel-pointer"></div>
                <div class="wheel" id="wheel"></div>
            </div>
            <button class="spin-button" id="spinButton" onclick="spinWheel()">Pick a Movie</button>
        </div>
    </div>
    
    <div class="selected-movie-overlay" id="selectedMovieOverlay" onclick="if(event.target === this) closeMovieNotification()">
        <div class="selected-movie" id="selectedMovie">
            <button class="selected-movie-close" onclick="closeMovieNotification()" aria-label="Close">×</button>
            <img class="selected-movie-poster" id="selectedMoviePoster" src="" alt="" style="display: none;">
            <a class="selected-movie-link" id="selectedMovieLink" target="_blank" rel="noopener noreferrer"></a>
            <div class="selected-movie-score" id="selectedMovieScore"></div>
            <div class="selected-movie-genres" id="selectedMovieGenres"></div>
            <div class="selected-movie-description" id="selectedMovieDescription"></div>
        </div>
    </div>
    
    <script>
        let movies = [];
        let isSpinning = false;
        const SPIN_CONFIG = {
            minTurns: 10,
            maxTurns: 18,
            minDuration: 3.1,
            maxDuration: 4.7
        };
        const LETTERBOXD_SEARCH_URL = 'https://letterboxd.com/search/';
        
        function loadMovies() {
            fetch('/api/movies')
                .then(response => response.json())
                .then(data => {
                    movies = data.movies;
                    updateStats();
                })
                .catch(error => {
                    console.error('Error loading movies:', error);
                });
        }
        
        function updateStats() {
            document.getElementById('totalMovies').textContent = movies.length;
            if (movies.length > 0) {
                const avgScore = movies.reduce((sum, m) => sum + m.score, 0) / movies.length;
                document.getElementById('averageScore').textContent = avgScore.toFixed(2);
            }
        }
        
        function closeMovieNotification() {
            const overlay = document.getElementById('selectedMovieOverlay');
            overlay.classList.remove('visible');
        }
        
        function randomInRange(min, max) {
            return min + (Math.random() * (max - min));
        }
        
        function getSpinDegrees() {
            const turns = randomInRange(SPIN_CONFIG.minTurns, SPIN_CONFIG.maxTurns);
            const offset = Math.random() * 360;
            return (turns * 360) + offset;
        }
        
        function getSpinDuration() {
            return randomInRange(SPIN_CONFIG.minDuration, SPIN_CONFIG.maxDuration);
        }
        
        function buildMovieLink(movie) {
            if (movie.url) {
                return { href: movie.url, isDirect: true };
            }
            if (!movie.name) {
                return { href: '', isDirect: false };
            }
            const encodedName = encodeURIComponent(movie.name.trim());
            return { href: `${LETTERBOXD_SEARCH_URL}${encodedName}/`, isDirect: false };
        }
        
        function spinWheel() {
            if (isSpinning || movies.length === 0) return;
            
            isSpinning = true;
            const button = document.getElementById('spinButton');
            const wheel = document.getElementById('wheel');
            const overlay = document.getElementById('selectedMovieOverlay');
            
            button.disabled = true;
            closeMovieNotification();
            
            const randomMovie = movies[Math.floor(Math.random() * movies.length)];
            const currentRotation = getCurrentRotation(wheel);
            const rotationDelta = getSpinDegrees();
            const spinDuration = getSpinDuration();
            
            wheel.style.transition = `transform ${spinDuration}s cubic-bezier(0.17, 0.67, 0.12, 0.99)`;
            wheel.style.transform = `rotate(${currentRotation + rotationDelta}deg)`;
            
            setTimeout(() => {
                const movieLink = document.getElementById('selectedMovieLink');
                const { href, isDirect } = buildMovieLink(randomMovie);
                movieLink.textContent = randomMovie.name;
                if (href) {
                    movieLink.href = href;
                    movieLink.style.pointerEvents = 'auto';
                    movieLink.dataset.direct = isDirect ? 'true' : 'false';
                    movieLink.title = isDirect
                        ? 'Open on Letterboxd'
                        : 'Search this title on Letterboxd';
                } else {
                    movieLink.removeAttribute('href');
                    movieLink.style.pointerEvents = 'none';
                    movieLink.removeAttribute('data-direct');
                    movieLink.removeAttribute('title');
                }
                document.getElementById('selectedMovieScore').textContent = 
                    `${randomMovie.score.toFixed(2)} / 5.00`;

                // Update Genres
                const genresContainer = document.getElementById('selectedMovieGenres');
                genresContainer.innerHTML = '';
                if (randomMovie.genres && randomMovie.genres.length > 0) {
                    randomMovie.genres.forEach(genre => {
                        const tag = document.createElement('span');
                        tag.className = 'genre-tag';
                        tag.textContent = genre;
                        genresContainer.appendChild(tag);
                    });
                }

                // Update Description
                const descEl = document.getElementById('selectedMovieDescription');
                descEl.textContent = randomMovie.description || '';
                
                const posterImg = document.getElementById('selectedMoviePoster');
                if (randomMovie.image) {
                    posterImg.src = randomMovie.image;
                    posterImg.alt = randomMovie.name;
                    posterImg.style.display = 'block';
                } else {
                    posterImg.style.display = 'none';
                }
                
                overlay.classList.add('visible');
                isSpinning = false;
                button.disabled = false;
            }, spinDuration * 1000);
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeMovieNotification();
            }
        });
        
        function getCurrentRotation(element) {
            const style = window.getComputedStyle(element);
            const matrix = style.transform || style.webkitTransform || style.mozTransform;
            if (matrix === 'none') return 0;
            const values = matrix.split('(')[1].split(')')[0].split(',');
            const a = values[0];
            const b = values[1];
            const angle = Math.round(Math.atan2(b, a) * (180/Math.PI));
            return angle < 0 ? angle + 360 : angle;
        }
        
        
        loadMovies();
        setInterval(loadMovies, 30000);
    </script>
</body>
</html>
"""

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
