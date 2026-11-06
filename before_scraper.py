"""The old way: scrape About pages and guess with regex."""
import re

import requests
from bs4 import BeautifulSoup

PAGES = {
    "Notion": "https://www.notion.so/about",
    "Stripe": "https://stripe.com/about",
}


def find(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def scrape(company, url):
    try:
        html = requests.get(url, timeout=15).text
    except requests.RequestException:
        html = ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ")
    h1 = soup.find("h1")
    return {
        "company": company,
        "headcount": find(r"[\d,]+\+? employees", text),
        "funding": find(r"Series [A-Z]", text),
        "main_product": h1.get_text(strip=True) if h1 else None,
        "competitors": None,  # not on the page, so we can't get it
    }


if __name__ == "__main__":
    for company, url in PAGES.items():
        print(f"\n== {company} ==")
        for field, value in scrape(company, url).items():
            print(f"  {field:<13} {value}")
