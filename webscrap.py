import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ---------------------------------------------------------
# Step 1: Fetch webpage data (uses the `requests` library)
# ---------------------------------------------------------
def fetch_page(url):
    """Download the raw HTML of a webpage using requests, with
    browser-like headers so the server treats us like a normal browser
    instead of blocking us as a bot."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    print(f"[requests] Sending GET request to: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # raises an error for 404 / 500 / etc.
    print(f"[requests] Response status code: {response.status_code}")
    return response.text


# ---------------------------------------------------------
# Step 2: Extract product title, price, and image URL
# (uses the `BeautifulSoup` library to parse the HTML)
# ---------------------------------------------------------
def extract_product_details(html, base_url):
    """Parse the HTML and pull out the product's title, price, and image URL."""
    print("[BeautifulSoup] Parsing HTML content...")
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("div", class_="product_main").h1.text.strip()

    price_text = soup.find("p", class_="price_color").text.strip()
    price = float(price_text.replace("£", "").replace("Â", ""))

    image_tag = soup.find("div", class_="item active").img
    image_url = urljoin(base_url, image_tag["src"])

    print(f"[BeautifulSoup] Found <title> tag: {soup.title.text.strip()}")
    print(f"[BeautifulSoup] Extracted product title, price, image tag successfully")

    return {"title": title, "price": price, "image_url": image_url}


# ---------------------------------------------------------
# Step 3: Download product image
# ---------------------------------------------------------
def download_image(image_url, folder, filename):
    """Download an image from image_url and save it locally."""
    os.makedirs(folder, exist_ok=True)
    img_data = requests.get(image_url, timeout=10).content
    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as f:
        f.write(img_data)
    return filepath


# ---------------------------------------------------------
# Step 4: Compare product price with target price
# ---------------------------------------------------------
def compare_price(actual_price, target_price):
    """Return a message stating whether the product is within budget."""
    if actual_price <= target_price:
        return f"Within budget! (£{actual_price} <= £{target_price})"
    else:
        return f"Over budget! (£{actual_price} > £{target_price})"


# ---------------------------------------------------------
# Step 5: Handle multiple product URLs
# ---------------------------------------------------------
def main():
    product_urls = [
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "http://books.toscrape.com/catalogue/soumission_998/index.html",
    ]

    target_price = 30.0
    save_folder = "downloaded_images"

    print("=" * 50)
    print("PRODUCT WEB SCRAPING RESULTS")
    print("=" * 50)

    for idx, url in enumerate(product_urls, start=1):
        print(f"\n--- Product {idx} ---")
        print(f"URL: {url}")
        try:
            html = fetch_page(url)
            details = extract_product_details(html, url)

            print(f"Title      : {details['title']}")
            print(f"Price      : £{details['price']}")
            print(f"Image URL  : {details['image_url']}")

            filename = f"product_{idx}.jpg"
            saved_path = download_image(details["image_url"], save_folder, filename)
            print(f"Image saved to: {saved_path}")

            print("Price Check:", compare_price(details["price"], target_price))

        except requests.exceptions.RequestException as e:
            print(f"Network/HTTP error while processing {url}: {e}")
        except AttributeError as e:
            print(f"Could not find expected HTML elements on {url}: {e}")
        except Exception as e:
            print(f"Unexpected error while processing {url}: {e}")

    print("\n" + "=" * 50)
    print("DONE")
    print("=" * 50)


if __name__ == "__main__":
    main()
