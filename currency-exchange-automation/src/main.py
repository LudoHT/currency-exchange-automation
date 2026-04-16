import sys
from datetime import date

from config import TEMPLATE_FILE, OUTPUT_FILE, CURRENCIES
from fx_service import fetch_rates_for_month
from excel_writer import write_summary_sheet


def get_previous_month() -> tuple[int, int]:
    today = date.today()
    if today.month == 1:
        return today.year - 1, 12
    return today.year, today.month - 1


def parse_args() -> tuple[int, int]:
    args = sys.argv[1:]

    if len(args) == 0:
        return get_previous_month()

    if len(args) == 2:
        try:
            year = int(args[0])
            month = int(args[1])
        except ValueError:
            print("Error: year and month must be integers. Example: py -3.11 src/main.py 2026 3")
            sys.exit(1)

        if not (2000 <= year <= 2099):
            print(f"Error: year {year} is out of the expected range (2000–2099).")
            sys.exit(1)

        if not (1 <= month <= 12):
            print(f"Error: month {month} is invalid. Must be between 1 and 12.")
            sys.exit(1)

        return year, month

    print("Usage: py -3.11 src/main.py [year month]")
    print("  No arguments  → processes the previous completed month automatically")
    print("  Two arguments → processes the specified year and month")
    print("  Example: py -3.11 src/main.py 2026 3")
    sys.exit(1)


def main():
    year, month = parse_args()
    print(f"Processing exchange rates for {year}-{month:02d}...")

    try:
        fx_data = fetch_rates_for_month(year, month, CURRENCIES)
        write_summary_sheet(TEMPLATE_FILE, OUTPUT_FILE, fx_data)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return

    print(f"Done. Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()