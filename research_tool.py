"""The Olostep way: company names in, structured data out."""
import csv
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.olostep.com/v1"
HEADERS = {
    "Authorization": f"Bearer {os.environ['OLOSTEP_API_KEY']}",
    "Content-Type": "application/json",
}

SCHEMA = {
    "company": "",
    "funding_stage": "",
    "total_funding": "",
    "headcount": "",
    "main_product": "",
    "top_competitors": [],
}


def research(company):
    task = (
        f"Research the company {company}: its latest funding stage, total funding "
        "raised, current headcount, main product, and its top 3 competitors."
    )
    response = requests.post(
        f"{BASE_URL}/answers",
        headers=HEADERS,
        json={"task": task, "json": SCHEMA},
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()["result"]["json_content"]
    return json.loads(data) if isinstance(data, str) else data


def load_companies(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def print_block(row):
    print(f"\n== {row['company']} ==")
    for field, value in row.items():
        if field != "company":
            print(f"  {field:<16} {value}")


def save_csv(rows, path="results.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(SCHEMA))
        writer.writeheader()
        writer.writerows(rows)


def to_row(company, data):
    row = {field: data.get(field) or "" for field in SCHEMA}
    row["company"] = row["company"] or company
    if isinstance(row["top_competitors"], list):
        row["top_competitors"] = ", ".join(row["top_competitors"])
    return row


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "companies.txt"
    start = time.time()
    rows = []

    for company in load_companies(path):
        try:
            row = to_row(company, research(company))
        except Exception as error:  # one bad company shouldn't stop the run
            print(f"\n== {company} ==\n  failed: {error}")
            continue
        print_block(row)
        rows.append(row)

    save_csv(rows)
    print(f"\nSaved {len(rows)} companies to results.csv")
    print(f"Total time: {time.time() - start:.1f}s")
