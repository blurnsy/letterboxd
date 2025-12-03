from seleniumbase import SB
from typing import List, Dict

url = "https://letterboxd.com"
with SB(uc=True, locale="en", guest=True) as sb:
    sb.open(url)
    sb.click('a[href="/sign-in/"]')
    sb.wait_for_element('#username')
    sb.type('#username', 'blurnsy')
    sb.type('#password', 'roxfUn-momzu7-fidmiz')
    sb.click('input[type="submit"]')
    sb.wait_for_element('a[href="/films/popular/this/week/"]')
    sb.open('https://letterboxd.com/films/popular/this/week/')
    sb.wait_for_element('ul.poster-list li.posteritem', timeout=10)
    sb.sleep(2)
    
    posters = sb.driver.find_elements('css selector', 'li.posteritem')
    print(f"Found {len(posters)} poster elements")
    
    results: List[Dict[str, str]] = []
    
    for poster in posters:
        try:
            name_element = poster.find_element('css selector', 'span.frame-title')
            name = name_element.get_attribute('textContent') or name_element.text
            name = name.strip() if name else ''
            score = poster.get_attribute('data-average-rating') or ''
            
            if name:
                results.append({
                    'name': name,
                    'score': score
                })
                print(f"Name: {name}, Score: {score}")
        except Exception:
            continue
    
    print(f"\nScraped {len(results)} films")