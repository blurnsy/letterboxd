import time
from seleniumbase import SB

start_time = time.time()
url = "https://www.target.com/"
with SB(uc=True, locale="en", guest=True) as sb:
    sb.open(url)
    sb.maximize_window()
    sb.sleep(2.4)
    sb.click("#search")
    sb.sleep(2.1)
    search = "Airpods"
    required_text = "Apple"
    sb.type("#search", search)
    sb.click('[data-test="@web/Search/SearchButton"]')
    sb.remove_elements('[data-component-id^="STORY-"]')
    sb.wait_for_element('div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]', timeout=10)
    sb.sleep(1)

    print('*** Target Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.find_elements('div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')
    for item in items:
        if required_text in item.text:
            item.flash(color="FF5F1F")
            description = item.querySelector(
                '[data-test="product-title"]'
            )
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector(
                    '[data-test="current-price"]'
                )
                if price:
                    price_text = price.text
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\n*** Total execution time: {elapsed_time:.2f} seconds ***")