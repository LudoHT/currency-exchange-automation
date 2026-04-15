from openpyxl import load_workbook

RATE_NUMBER_FORMAT = "0.00000"

def _find_cell(ws, value: str):
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == value:
                return cell
    return None

def _find_cell_containing(ws, value: str):
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and value in cell.value:
                return cell
    return None

def _find_rates_sheet(wb):
    for ws in wb.worksheets:
        if _find_cell(ws, "Period Average") and _find_cell(ws, "Spot Rate/Date"):
            return ws
    raise ValueError("Could not find worksheet with Period Average and Spot Rate/Date tables.")

def _write_rate_table(ws, header_text: str, data_key: str, fx_data: dict) -> set:
    header_cell = _find_cell(ws, header_text)
    if header_cell is None:
        raise ValueError(f"Could not find {header_text} table in workbook.")

    currency_column = header_cell.column
    value_column = currency_column + 1
    updated = set()

    for row in range(header_cell.row + 1, ws.max_row + 1):
        currency = ws.cell(row=row, column=currency_column).value
        if currency in fx_data:
            value_cell = ws.cell(row=row, column=value_column)
            value_cell.value = fx_data[currency][data_key]
            value_cell.number_format = RATE_NUMBER_FORMAT
            updated.add(currency)

    if not updated:
        raise ValueError(f"No currencies were updated in the {header_text} table.")

    return updated

def _write_salesforce_table(ws, fx_data: dict):
    header_cell = _find_cell_containing(ws, "SalesForce Update")
    if header_cell is None:
        return

    currency_column = header_cell.column - 1
    value_column = header_cell.column

    for row in range(header_cell.row + 1, ws.max_row + 1):
        currency = ws.cell(row=row, column=currency_column).value
        if currency in fx_data:
            value_cell = ws.cell(row=row, column=value_column)
            value_cell.value = fx_data[currency]["spot_rate"]
            value_cell.number_format = RATE_NUMBER_FORMAT

def write_summary_sheet(template_path, output_path, fx_data: dict):
    wb = load_workbook(template_path)
    ws = _find_rates_sheet(wb)

    _write_rate_table(ws, "Period Average", "period_average", fx_data)
    _write_rate_table(ws, "Spot Rate/Date", "spot_rate", fx_data)
    _write_salesforce_table(ws, fx_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
