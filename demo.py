import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.olostep.com/v1"
HEADERS = {
    "Authorization": f"Bearer {os.environ['OLOSTEP_API_KEY']}",
    "Content-Type": "application/json",
}


def scrape(url):
    response = requests.post(
        f"{BASE_URL}/scrapes",
        headers=HEADERS,
        json={"url_to_scrape": url, "formats": ["markdown"]},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["result"]["markdown_content"]


def company_profile(company):
    response = requests.post(
        f"{BASE_URL}/answers",
        headers=HEADERS,
        json={
            "task": f"What is the latest funding stage and current headcount of {company}?",
            "json": {"company": "", "funding_stage": "", "headcount": ""},
        },
        timeout=120,
    )
    response.raise_for_status()
    result = response.json()["result"]
    return json.loads(result["json_content"]), result["sources"]


if __name__ == "__main__":
    print("--- Scrape ---")
    print(scrape("https://www.olostep.com/pricing")[:500])

    print("\n--- Answers ---")
    profile, sources = company_profile("Stripe")
    print(json.dumps(profile, indent=2))
    print("Sources:", sources)
