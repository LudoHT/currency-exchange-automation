from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

API_KEY = os.getenv("OPEN_EXCHANGE_RATES_API_KEY")

TEMPLATE_FILE = DATA_DIR / "2026 Exchange Rates_Example.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "exchange_rates_output.xlsx"

BASE_CURRENCY = "USD"

CURRENCIES = [
    "AED", "AUD", "CAD", "CHF", "DKK", "EUR", "GBP", "HUF",
    "JPY", "NOK", "NZD", "RUB", "SEK", "SGD", "ZAR",
    "INR", "KRW", "MYR", "HKD"
]
