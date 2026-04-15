# Currency Exchange Rate Automation

Automates the monthly population of exchange rates into the provided Excel format.

## What it does
- Pulls exchange rates for a selected month
- Calculates:
  - Period Average = simple average of daily rates in the month
  - Spot Rate = exchange rate on the last day of the month
- Writes results into the provided Excel template

## Project structure
- `data/` for the Excel template they provided
- `output/` for generated files
- `src/` for the Python code

## Setup
1. Create a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`
4. Add your Open Exchange Rates API key

## Run
```bash
python src/main.py
```

## Notes
- Base currency is USD
- Output values are formatted to 5 decimal places
- Currency list can be updated in `src/config.py`
- Put the provided Excel file in `data/` and rename it to `2026 Exchange Rates_Example.xlsx`
