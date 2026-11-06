# Olostep company research demo
Turn a list of company names into structured data with one API call per company, using Olostep's `/answers` endpoint.

📺 **Video walkthrough:** [YouTube link coming soon](https://youtube.com/your-video-link)

## Before vs after

**Before: `before_scraper.py`** (the old way)
Fetches company "About" pages with `requests` + BeautifulSoup, then guesses with regex: `"employees"` for headcount, `"Series X"` for funding, the first `<h1>` for the product. Competitors are never on the page, so they're always `None`. Pages are JavaScript-heavy, wording changes, and the data is often not there at all, so most fields come back empty:

```
== Notion ==
  company       Notion
  headcount     None
  funding       None
  main_product  About Notion
  competitors   None

== Stripe ==
  company       Stripe
  headcount     None
  funding       None
  main_product  None
  competitors   None
```

**After: `research_tool.py`** (the Olostep way)
Reads company names from `companies.txt`, asks `/answers` a plain-English question with a JSON schema, and gets back clean structured fields, researched across the web with sources. Results print as a table and are saved to `results.csv`.

## Setup
1. `pip install -r requirements.txt`
2. `cp .env.example .env` and put your key in `OLOSTEP_API_KEY`
3. `python research_tool.py` (or `python research_tool.py my_companies.txt`)

## Sample output

```
== Notion ==
  funding_stage    Series D (latest funding round: September 28, 2021)
  total_funding    $418 million
  headcount        3,138 employees (as of October 29, 2026)
  main_product     An AI-powered workspace for team collaboration and productivity, with project management, knowledge bases, document sharing, AI meeting notes, enterprise search, and workflow automation.
  top_competitors  Smartsheet, Anaplan, Pigment

== Stripe ==
  funding_stage    Secondary Market
  total_funding    $9.81 billion
  headcount        Approximately 10,430 employees worldwide as of June 2026
  main_product     Programmable financial infrastructure for accepting payments and managing financial operations
  top_competitors  Checkout.com, Airwallex, PayPal

== Linear ==
  funding_stage    Series C (latest primary funding round; June 2025)
  total_funding    $134.2 million
  headcount        Approximately 112–129 employees
  main_product     A product development system for teams and agents to plan and build products, including issue tracking, project planning, and AI-assisted workflows.
  top_competitors  Jira, Asana, monday.com

== Vercel ==
  funding_stage    Series F (September 2025)
  total_funding    $863 million
  headcount        966 employees as of June 2026 (estimate)
  main_product     A developer cloud platform for building, deploying, and scaling web applications, including AI applications.
  top_competitors  Cloudflare, Railway, Netlify

== Supabase ==
  funding_stage    Undisclosed-stage $150 million funding round (latest)
  total_funding    $1.19 billion
  headcount        Approximately 512 employees (June 2026)
  main_product     An open-source Postgres development platform and backend providing a Postgres database, authentication, APIs, real-time features, functions, storage, and vector embeddings.
  top_competitors  Firebase, Appwrite, Neon

Saved 5 companies to results.csv
Total time: 116.1s
```

## How it works
1. **Describe the task** in plain English: "Research {company}: funding stage, total funding, headcount, main product, top 3 competitors."
2. **Pass a JSON schema** of the fields you want (`company`, `funding_stage`, `total_funding`, `headcount`, `main_product`, `top_competitors`).
3. **Olostep searches the web and fills the schema**, returning JSON you can drop straight into a CSV, spreadsheet, or CRM.

## Use cases
- **Lead enrichment:** add funding, size, and product info to a list of prospects.
- **Competitor research:** map who competes with whom across a market.
- **Market research:** build a quick dataset on every company in a space.

## Also in this repo
`demo.py` is a minimal example of both the `/scrapes` and `/answers` endpoints.
