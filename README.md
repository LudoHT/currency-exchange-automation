# Currency Exchange Rate Automation

Automates the monthly population of exchange rates into the provided Excel format using the Open Exchange Rates API.

## What it does
- Pulls historical daily exchange rates for the selected month
- Calculates:
  - Period Average = simple average of daily rates in the selected month
  - Spot Rate = exchange rate on the last day of the selected month
- Writes results into the provided Excel template

## Project structure
- `data/` for the provided Excel template
- `output/` for generated files
- `src/` for the Python code

## Setup
1. Create a virtual environment if desired
2. Install dependencies:

```bash
py -3.11 -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`
4. Add your Open Exchange Rates API key:
OPEN_EXCHANGE_RATES_API_KEY=your_api_key_here

## Run
```bash
py -3.11 src/main.py
```
## Output
output/exchange_rates_output.xlsx

## Notes
- Base currency is USD
- Output values are formatted to 5 decimal places
- Currency list can be updated in `src/config.py`
- The input Excel template is located at `data/2026 Exchange Rates_Example.xlsx`
