from playwright.sync_api import sync_playwright
from notifier import send_message
import json

def get_price(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        # selector pentru preț (Amazon)
        price = page.locator(".product-new-price").first.inner_text()

        browser.close()

        price = price.replace("Lei", "").strip()
        price = price.replace(".", "").replace(",", ".")
        return float(price)


def load_products():
    with open("products.json") as f:
        return json.load(f)


def check_prices():
    products = load_products()

    for product in products:
        price = get_price(product["url"])

        print(f"{product['name']}")
        print(f"Current price: {price} RON")
        print(f"Target price: {product['target_price']} RON")
        print("--------------")

        if price <= product["target_price"]:
            print("🔥 PRICE DROP!")
            send_message(f"🔥 Price drop!\n{product['name']}\nPrice: {price} RON\nTarget: {product['target_price']} RON\n{product['url']}")

if __name__ == "__main__":
    check_prices()