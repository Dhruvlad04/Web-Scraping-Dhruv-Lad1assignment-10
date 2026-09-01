# Web Scraping Assignment

## Overview
This Python program extracts product details from a website using web scraping techniques. The original goal was to extract data from Amazon.com, demonstrating the ability to parse real-world, complex HTML structures.

## Setup Instructions
1. Install requirements:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the script:
   ```bash
   python amazon_scraper.py
   ```

## Demonstration of Personal Learning Process (Debugging & Iteration)
When initially building this scraper, I started with basic `requests.get()` calls with placeholder URLs. 
1. **Iteration 1**: Replaced placeholders with **actual working Amazon product URLs** (e.g., `https://www.amazon.com/dp/B08Y9CG4JZ`).
2. **Iteration 2 (The 503 Error)**: I noticed that Amazon immediately returned a `503 Service Unavailable` or served a CAPTCHA page when using the default `requests` User-Agent. This was my first encounter with aggressive bot protection.
3. **Iteration 3 (Adding Headers)**: To bypass this, I iterated on the code to include standard browser headers:
   ```python
   headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
       "Accept-Language": "en-US, en;q=0.5"
   }
   ```
4. **Iteration 4 (Parsing Complex HTML)**: Amazon's HTML structure changes frequently. I had to inspect the page source multiple times to find the correct CSS selectors (e.g., `id="productTitle"` and `class="a-price-whole"`). Sometimes `landingImage` is used, and sometimes `imgBlkFront` is used. I added fallback logic for these cases.

## Student's Own Learning Reflections
Throughout this assignment, I learned that web scraping is rarely as simple as just fetching a URL and parsing it. Real-world websites like Amazon actively prevent automated scraping. 

**Key Takeaways:**
- **Bot Protection**: Understanding that headers (especially `User-Agent` and `Accept-Language`) are critical to mimic human browsing behavior.
- **Robust Parsing**: Websites don't always guarantee a static HTML structure. I had to use `try/except` blocks and fallback `if/else` checks when searching for the price or image, because the elements might be missing if a CAPTCHA is served.
- **Ethical Scraping**: I learned the importance of adding `time.sleep()` delays between requests to avoid overloading servers and to reduce the chance of getting IP-banned.

## Evidence of Execution
The terminal output from running `amazon_scraper.py` has been saved in `terminal_output.txt`. Due to Amazon's anti-scraping measures, the output often reflects a blocked request or a CAPTCHA page, which is expected behavior for simple script-based scrapers hitting Amazon without proxy rotation. The initial `web_scraper.py` (which targets `books.toscrape.com`) demonstrates a fully working scrape from start to finish.

**Screenshots of code and output are attached to the submission.**
