# Olostep demo
Company enrichment with the Olostep Scrape and Answers APIs.

**Why this matters:** Turns a company name into structured funding and headcount data in one call.

## Sample output
From `company_profile("Stripe")`:

```json
{
  "company": "Stripe",
  "funding_stage": "Series I",
  "headcount": "16,622 (as of September 30, 2026)"
}
```

Sources: [Tracxn](https://tracxn.com/d/companies/stripe/__uahG_IGnVgsUsOG-f8otYHLkOkliWg7YFhJ5ZkNIkpI)

## Run it
1. `pip install -r requirements.txt`
2. Create a `.env` file containing `OLOSTEP_API_KEY=your_key`
3. `python demo.py`
