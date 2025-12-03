import pytest
from seleniumbase import SB


def test_pizza_delivery_order(sb):
    sb.open("https://www.dominos.com/?type=order_delivery")
    sb.sleep(3)
    
    sb.type('input[name="streetAddress"]', "2817 Bengal Lane")
    sb.sleep(1)

    sb.type('input[name="zipCode"]', "75023")
    sb.sleep(1)
    
    sb.type('input[name="city"]', "Plano")
    sb.sleep(1)
    
    sb.type('input[name="state"]', "TX")
    sb.sleep(1)
    
    sb.click('button[type="submit"][form="deliveryForm"]')
    sb.sleep(3)
    
    sb.click('button:contains("Confirm Location")')
    sb.sleep(3)
    
    sb.click('[data-testid="BuildYourOwn-img-sm"]')
    sb.sleep(2)
    
    sb.scroll_to('label[for="customizer-Crusts-THIN"]')
    sb.sleep(1)
    sb.js_click('input[id="customizer-Crusts-THIN"], label[for="customizer-Crusts-THIN"]')
    sb.sleep(2)
    
    sb.scroll_to('[data-testid="customizer-VEGEMORE-J-img-sm"]')
    sb.sleep(1)
    sb.js_click('xpath://button[.//img[@data-testid="customizer-VEGEMORE-J-img-sm"]]')
    sb.sleep(2)
    
    sb.scroll_to_bottom()
    sb.sleep(1)
    sb.wait_for_element_visible('xpath://button[contains(text(), "ADD TO CART")]', timeout=10)
    sb.js_click('xpath://button[contains(text(), "ADD TO CART")]')
    sb.sleep(2)