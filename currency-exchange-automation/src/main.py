from config import TEMPLATE_FILE, OUTPUT_FILE, CURRENCIES
from fx_service import fetch_rates_for_month
from excel_writer import write_summary_sheet

def main():
    year = 2026
    month = 3

    try:
        fx_data = fetch_rates_for_month(year, month, CURRENCIES)
        write_summary_sheet(TEMPLATE_FILE, OUTPUT_FILE, fx_data)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return

    print(f"Done. Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
