from calendar import monthrange
from datetime import date, timedelta

import requests

from config import API_KEY, BASE_CURRENCY

HISTORICAL_RATES_URL = "https://openexchangerates.org/api/historical/{rate_date}.json"
REQUEST_TIMEOUT_SECONDS = 15

def get_month_date_range(year: int, month: int):
    start = date(year, month, 1)
    end = date(year, month, monthrange(year, month)[1])
    return start, end

def calculate_period_average_and_spot(rates_by_day: dict):
    values = [rates_by_day[rate_date] for rate_date in sorted(rates_by_day)]
    if not values:
        raise ValueError("No rates found for month")
    period_average = sum(values) / len(values)
    spot_rate = values[-1]
    return round(period_average, 5), round(spot_rate, 5)

def _get_required_api_key() -> str:
    if not API_KEY or API_KEY.strip() == "your_api_key_here":
        raise RuntimeError(
            "Missing Open Exchange Rates API key. Add "
            "OPEN_EXCHANGE_RATES_API_KEY to your .env file."
        )
    return API_KEY.strip()

def _month_dates(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def _fetch_daily_rates(rate_date: date, currencies: list[str], api_key: str) -> dict:
    params = {
        "app_id": api_key,
        "symbols": ",".join(currencies),
    }

    if BASE_CURRENCY != "USD":
        params["base"] = BASE_CURRENCY

    response = requests.get(
        HISTORICAL_RATES_URL.format(rate_date=rate_date.isoformat()),
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"Open Exchange Rates returned an invalid response for {rate_date}."
        ) from exc

    if response.status_code != 200 or data.get("error"):
        message = data.get("description") or data.get("message") or response.text
        raise RuntimeError(
            f"Open Exchange Rates request failed for {rate_date}: {message}"
        )

    rates = data.get("rates")
    if not isinstance(rates, dict):
        raise RuntimeError(f"Open Exchange Rates response for {rate_date} has no rates.")

    missing_currencies = [currency for currency in currencies if currency not in rates]
    if missing_currencies:
        missing = ", ".join(missing_currencies)
        raise RuntimeError(f"Missing rates for {rate_date}: {missing}")

    return {currency: rates[currency] for currency in currencies}

def fetch_rates_for_month(year: int, month: int, currencies: list[str]) -> dict:
    api_key = _get_required_api_key()
    start_date, end_date = get_month_date_range(year, month)
    rates_by_currency = {currency: {} for currency in currencies}

    for rate_date in _month_dates(start_date, end_date):
        daily_rates = _fetch_daily_rates(rate_date, currencies, api_key)
        for currency, rate in daily_rates.items():
            rates_by_currency[currency][rate_date] = rate

    fx_data = {}
    for currency, rates_by_day in rates_by_currency.items():
        period_average, spot_rate = calculate_period_average_and_spot(rates_by_day)
        fx_data[currency] = {
            "period_average": period_average,
            "spot_rate": spot_rate,
        }

    return fx_data
