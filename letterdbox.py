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
    results: List[Dict[str, Union[str, float]]] = []
    
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
                    'url': link_url
                })
        except Exception:
            continue
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    with open('movies.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n*** Popular This Week on Letterboxd (Sorted by Score) ***\n")
    for film in results:
        print(f"Film: {film['name']}, Audience Score: {film['score']}")
    
    print(f"\nScraped {len(results)} films")
    print(f"Data saved to movies.json")