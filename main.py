from playwright.sync_api import sync_playwright
from notifier import send_message
import json

def get_price(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".product-new-price", timeout=60000)

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