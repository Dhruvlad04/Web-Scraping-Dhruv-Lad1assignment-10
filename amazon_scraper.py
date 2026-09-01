import os
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0 Safari/537.36"
}

PRODUCT_URLS = [
    "https://www.amazon.in/dp/B071Z8M4KX",
    "https://www.amazon.in/dp/B074ZF7PVZ",
    "https://www.amazon.in/dp/B07JQKQ91F",
]

IMAGE_FOLDER = "product_images"

def get_text(soup, selector):
    tag = soup.select_one(selector)
    if tag:
        return tag.get_text(" ", strip=True)
    return ""

def get_product(url):
    print("\nOpening:", url)

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = get_text(soup, "#productTitle")

    # Amazon may show the price in more than one place.
    price_text = get_text(soup, "span.a-price span.a-offscreen")
    if not price_text:
        price_text = get_text(soup, "#corePriceDisplay_desktop_feature_div span.a-offscreen")

    # Product image can also have more than one attribute.
    image = soup.select_one("#landingImage")
    if image is None:
        image = soup.select_one("#imgTagWrapperId img")

    image_url = ""
    if image:
        image_url = image.get("data-old-hires") or image.get("src") or ""

    if not title:
        raise ValueError("Product title was not found. Amazon may have shown a CAPTCHA page.")

    numbers = re.findall(r"[\d,]+(?:\.\d+)?", price_text)
    if not numbers:
        raise ValueError("Product price was not found.")

    price = float(numbers[0].replace(",", ""))

    return {
        "title": title,
        "price": price,
        "image_url": image_url,
        "url": url
    }

def download_image(image_url, title, number):
    if not image_url:
        print("Image URL not found.")
        return ""

    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title)[:50]
    filename = f"{number}_{safe_title}.jpg"
    path = os.path.join(IMAGE_FOLDER, filename)

    response = requests.get(image_url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)

    return path

def compare_price(price, target):
    if price <= target:
        return "Within target price"
    return "Above target price"

def main():
    print("=" * 60)
    print("AMAZON PRODUCT WEB SCRAPER")
    print("=" * 60)

    target = float(input("Enter target price (Rs): "))

    products = []

    for number, url in enumerate(PRODUCT_URLS, start=1):
        try:
            product = get_product(url)
            products.append(product)

            print("\nProduct", number)
            print("Title     :", product["title"])
            print("Price     : Rs", product["price"])
            print("Image URL :", product["image_url"])

            result = compare_price(product["price"], target)
            print("Target    : Rs", target)
            print("Result    :", result)

            image_path = download_image(
                product["image_url"],
                product["title"],
                number
            )

            if image_path:
                print("Image saved:", image_path)

        except Exception as error:
            print("Could not read this product.")
            print("Reason:", error)

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    if products:
        for product in products:
            result = compare_price(product["price"], target)
            print(f"{product['title']} -> Rs {product['price']} -> {result}")
        print("\nProducts successfully extracted:", len(products))
    else:
        print("No products were extracted.")
        print("If Amazon displayed CAPTCHA, open the URL in a browser and try again later.")

if __name__ == "__main__":
    main()
