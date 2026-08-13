from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font


def export_to_excel(rows: list[dict], path: str = "prices.xlsx") -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Цены"

    headers = ["Предмет", "Мин. цена", "Медиана", "Продаж за сутки"]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in rows:
        ws.append([
            row["name"],
            row["lowest"],
            row["median"],
            row["volume"],
        ])

    for row in ws.iter_rows(min_row=2, min_col=2, max_col=3):
        for cell in row:
            cell.number_format = "#,##0.00"

    for row in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for cell in row:
            cell.number_format = "#,##0"

    ws.column_dimensions["A"].width = 50
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 18

    ws.freeze_panes = "A2"

    wb.save(path)
    print(f"Файл сохранён: {path}")