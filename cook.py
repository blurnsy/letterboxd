import time
import json
from seleniumbase import SB

def save_session(sb, filename='session_cookies.json'):
    cookies = sb.driver.get_cookies()
    with open(filename, 'w') as f:
        json.dump(cookies, f)

def load_session(sb, filename='session_cookies.json'):
    try:
        with open(filename, 'r') as f:
            cookies = json.load(f)

        # You MUST already be on the correct domain before adding cookies!
        for cookie in cookies:
            sb.driver.add_cookie(cookie)

        sb.refresh()  # much safer than open()
        return True
    except FileNotFoundError:
        return False

url = "https://letterboxd.com/"

with SB(uc=True, locale="en", guest=True) as sb:
    sb.open(url)                       # <-- REQUIRED BASE LOAD

    if not load_session(sb):
        sb.click('a[href="/sign-in/"]')
        sb.wait_for_element('#username')
        sb.type('#username', 'blurnsy')
        sb.type('#password', 'roxfUn-momzu7-fidmiz')
        sb.click('input[type="submit"]')
        sb.wait_for_element('a[href="/films/popular/this/week/"]')
        save_session(sb)

    sb.click('a[href="/films/popular/this/week/"]')
    sb.wait_for_element('ul.poster-list li.posteritem')

    films = sb.execute_script("""
        const posters = document.querySelectorAll('li.posteritem');
        return Array.from(posters).map(poster => ({
            name: poster.querySelector('span.frame-title')?.textContent || '',
            score: poster.getAttribute('data-average-rating') || ''
        }));
    """)

    for film in films:
        print("Name: {film.name}, Score: {film.score}")

    time.sleep(100)