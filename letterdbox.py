import os
import json
from typing import List, Dict, Union
from dotenv import load_dotenv

LETTERBOXD_BASE_URL = "https://letterboxd.com"

load_dotenv()

def test_scrape_films(sb) -> None:
    url = "https://letterboxd.com/films/popular/this/week/"
    sb.open(url)
    
    sb.click('a[href="/sign-in/"]')
    sb.wait_for_element('#username')
    sb.type('#username', os.getenv('lb_username'))
    sb.type('#password', os.getenv('lb_password'))
    sb.click('input[type="submit"]')
    sb.wait_for_element('ul.poster-list li.posteritem', timeout=10)
    sb.sleep(2)
    
    posters = sb.find_elements('li.posteritem')
    results: List[Dict[str, Union[str, float, List[str]]]] = []
    
    for poster in posters:
        try:
            name_element = poster.find_element('css selector', 'span.frame-title')
            name = name_element.get_attribute('textContent') or name_element.text
            name = name.strip() if name else ''
            score_str = poster.get_attribute('data-average-rating') or ''
            
            image_url = ''
            try:
                img_element = poster.find_element('css selector', 'img.image')
                image_url = img_element.get_attribute('src') or ''
            except Exception:
                pass

            link_url = ''
            try:
                link_element = poster.find_element('css selector', 'a.frame')
                href = link_element.get_attribute('href') or ''
                if href:
                    link_url = href if href.startswith('http') else f"{LETTERBOXD_BASE_URL}{href}"
            except Exception:
                pass
            
            if name:
                try:
                    score = float(score_str) if score_str else 0.0
                except ValueError:
                    score = 0.0
                
                results.append({
                    'name': name,
                    'score': score,
                    'image': image_url,
                    'url': link_url,
                    'description': '',
                    'genres': []
                })
        except Exception:
            continue
    
    # Visit each movie page to get details
    print(f"Found {len(results)} films. Scraping details...")
    
    for i, film in enumerate(results):
        if not film['url']:
            continue
            
        print(f"[{i+1}/{len(results)}] Scraping details for: {film['name']}")
        try:
            sb.open(film['url'])
            
            # Get Description/Synopsis
            # Try common selectors for synopsis
            description = ""
            if sb.is_element_visible('div.truncate p'):
                description = sb.get_text('div.truncate p')
            elif sb.is_element_visible('div.truncate'):
                description = sb.get_text('div.truncate')
            elif sb.is_element_visible('meta[name="description"]'):
                # Fallback to meta description if needed, but visible text is better
                pass
            
            # Get Genres
            genres = []
            if sb.is_element_visible('#tab-genres'):
                genre_elements = sb.find_elements('#tab-genres .text-sluglist a')
                genres = [g.text for g in genre_elements]
            
            film['description'] = description
            film['genres'] = genres
            
            # Polite sleep
            sb.sleep(0.5)
            
        except Exception as e:
            print(f"Error scraping details for {film['name']}: {e}")
            continue

    results.sort(key=lambda x: x['score'], reverse=True)
    
    with open('movies.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n*** Popular This Week on Letterboxd (Sorted by Score) ***\n")
    for film in results:
        print(f"Film: {film['name']}, Audience Score: {film['score']}")
    
    print(f"\nScraped {len(results)} films")
    print(f"Data saved to movies.json")