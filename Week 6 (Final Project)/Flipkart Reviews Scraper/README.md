# Flipkart Reviews Scraper – Frontend + Backend

A simple Flask app with a clean web UI to scrape Flipkart product reviews into a CSV.

## Features
- Input Flipkart product URL and optional cookie
- Optional Webshare rotating proxy support
- Choose number of pages to scrape
- Live preview in the browser
- One-click CSV download

> ⚠️ **Respect Flipkart's Terms of Service and local laws.** Use on your own responsibility.

## Quick Start

```bash
# 1) Create & activate a virtualenv (optional but recommended)
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the app
python app.py
```

Open http://localhost:5000 in your browser.

### Cookies
Flipkart often requires a valid session cookie to view reviews at scale. In your browser, copy the `Cookie` header for any request to flipkart.com and paste it into the UI. Keep it private.

### Proxies
If you have a Webshare proxy, tick "Use Webshare Proxy" and enter your credentials (username & password).

### Output
- Saves `flipkart_reviews.csv` in the project root.
- The page shows a preview of the first 100 rows.

## Notes
- The scraper is conservative: if a page returns no reviews or a non-200 status code, it stops to reduce risk of blocks.
- Be polite and avoid heavy scraping.
