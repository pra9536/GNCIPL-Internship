import re
import json
import time
import math
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "cache-control": "max-age=0",
    "connection": "keep-alive",
    "host": "www.flipkart.com",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-full-version": '"134.0.6998.178"',
    "sec-ch-ua-full-version-list": '"Chromium";v="134.0.6998.178", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.178"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"10.0.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def convert_to_review_url(product_url: str) -> str:
    parsed = urlparse(product_url)
    query = parse_qs(parsed.query)
    pid = query.get("pid", [""])[0]
    lid = query.get("lid", [f"LST{pid}XXXXXX"])[0]

    # Extract product path and replace /p/ with /product-reviews/
    path = parsed.path
    if "/p/" not in path:
        raise ValueError("Invalid Flipkart product URL")
    review_path = path.replace("/p/", "/product-reviews/")

    # Build query
    q = {"pid": pid, "marketplace": "FLIPKART"}
    if lid:
        q["lid"] = lid

    review_url = urlunparse((parsed.scheme, parsed.netloc, review_path, "", urlencode(q), ""))
    return review_url

def make_session(cookie: str = "", use_proxy: bool = False, proxy_username: str = "", proxy_password: str = "") -> requests.Session:
    s = requests.Session()
    headers = DEFAULT_HEADERS.copy()
    if cookie:
        headers["cookie"] = cookie
    s.headers.update(headers)
    if use_proxy and proxy_username and proxy_password:
        proxy = f"http://{proxy_username}-rotate:{proxy_password}@p.webshare.io:80/"
        s.proxies.update({"http": proxy, "https": proxy})
    return s

def parse_reviews_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    review_divs = soup.find_all("div", class_="cPHDOP col-12-12")
    ratings, comments = [], []
    for review in review_divs:
        rating_tag = review.select_one("div.XQDdHH")
        rating = rating_tag.get_text(strip=True) if rating_tag else None
        comment_tag = review.select_one("div.ZmyHeo div div")
        comment = comment_tag.get_text(separator=" ", strip=True) if comment_tag else None
        if rating and comment:
            ratings.append(rating)
            comments.append(comment)
    return ratings, comments

def scrape_reviews(product_url: str, cookie: str = "", pages: int = 5,
                   use_proxy: bool = False, proxy_username: str = "", proxy_password: str = "") -> pd.DataFrame:
    review_url_base = convert_to_review_url(product_url)
    session = make_session(cookie=cookie, use_proxy=use_proxy, proxy_username=proxy_username, proxy_password=proxy_password)

    all_ratings, all_comments = [], []
    for i in range(1, int(pages) + 1):
        # ensure we set the "page" query param correctly each iteration
        parsed = urlparse(review_url_base)
        q = parse_qs(parsed.query)
        q["page"] = [str(i)]
        page_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", urlencode({k:v[0] for k,v in q.items()}), ""))

        resp = session.get(page_url, timeout=20)
        if resp.status_code != 200:
            # Stop early if blocked or error to avoid bans
            break
        ratings, comments = parse_reviews_from_html(resp.text)
        # If we got nothing, likely end of pages or blocked
        if not ratings:
            if i == 1:
                # still return empty df but don't crash
                break
            else:
                # assume no more pages
                break
        all_ratings.extend(ratings)
        all_comments.extend(comments)
        time.sleep(1)  # polite delay

    df = pd.DataFrame({"score": all_ratings, "text": all_comments})
    return df
