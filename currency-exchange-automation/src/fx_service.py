from datetime import date
from calendar import monthrange

def get_month_date_range(year: int, month: int):
    start = date(year, month, 1)
    end = date(year, month, monthrange(year, month)[1])
    return start, end

def calculate_period_average_and_spot(rates_by_day: dict):
    values = list(rates_by_day.values())
    if not values:
        raise ValueError("No rates found for month")
    period_average = sum(values) / len(values)
    spot_rate = values[-1]
    return round(period_average, 5), round(spot_rate, 5)

def fetch_rates_for_month(year: int, month: int, currencies: list[str]) -> dict:
    '''
    Placeholder until API key is added.
    Return format:
    {
        "AED": {"period_average": 3.67251, "spot_rate": 3.67243},
        ...
    }
    '''
    raise NotImplementedError("Add Open Exchange Rates API logic once key is available.")
