import io
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter
import pandas as pd

DIVISIONS = [
    "Denver", "Haggen", "Intermountain", "Jewel-Osco", "MidAtlantic",
    "NorCal", "Portland", "Seattle", "Shaws", "SoCal", "Southern",
    "Southwest", "United"
]
TYPES = ["SYSTEM", "OPS", "PE"]

# ── Styles ─────────────────────────────────────────────────────────────────
HDR_FILL   = PatternFill("solid", fgColor="4F46E5")   # indigo
HDR_FONT   = Font(bold=True, color="FFFFFF", size=10)
SUB_FILL   = PatternFill("solid", fgColor="E0E7FF")   # light indigo
SUB_FONT   = Font(bold=True, color="1E1B4B", size=10)
BOLD_FONT  = Font(bold=True, size=10)
NORM_FONT  = Font(size=10)
WRAP_ALIGN = Alignment(wrap_text=True, vertical="top")
CTR_ALIGN  = Alignment(horizontal="center", vertical="center")
TOP_LEFT   = Alignment(vertical="top")

def _thin_border():
    s = Side(border_style="thin", color="D1D5DB")
    return Border(left=s, right=s, top=s, bottom=s)

def _apply_header(ws, row_num, values, fill, font):
    for col, val in enumerate(values, 1):
        c = ws.cell(row=row_num, column=col, value=val)
        c.fill   = fill
        c.font   = font
        c.border = _thin_border()
        c.alignment = CTR_ALIGN

def _auto_width(ws, min_w=8, max_w=40):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        best = min_w
        for cell in col:
            if cell.value:
                lines = str(cell.value).split("\n")
                best = max(best, max(len(l) for l in lines))
        ws.column_dimensions[col_letter].width = min(best + 2, max_w)

def _freeze(ws, cell="B3"):
    ws.freeze_panes = cell


# ── Tab builders ────────────────────────────────────────────────────────────

def write_inc(wb: Workbook, inc: pd.DataFrame):
    ws = wb.create_sheet("INC")
    cols = list(inc.columns)
    _apply_header(ws, 1, cols, HDR_FILL, HDR_FONT)
    for r_idx, row in enumerate(inc.itertuples(index=False), 2):
        for c_idx, val in enumerate(row, 1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.font      = NORM_FONT
            c.border    = _thin_border()
            c.alignment = WRAP_ALIGN
    _auto_width(ws)
    _freeze(ws, "A2")
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}1"


def _write_category_sheet(wb: Workbook, sheet_name: str, df: pd.DataFrame, value_col: str = "count"):
    """
    Shared layout for Acupick, Acupick Incident Categories, and Ops Issues.
    value_col: 'count' writes numbers; 'caller' writes caller strings.
    """
    ws = wb.create_sheet(sheet_name)

    # Row 1: section label
    ws.cell(row=1, column=1, value="")
    ws.cell(row=1, column=2, value="Operations Issue").font = BOLD_FONT
    ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=2 + len(DIVISIONS))

    # Row 2: column headers
    headers = ["", "Category"] + DIVISIONS + ["Total"]
    _apply_header(ws, 2, headers, SUB_FILL, SUB_FONT)

    # Data rows
    for r_idx, row in enumerate(df.itertuples(index=False), 3):
        # Code cell
        code_cell = ws.cell(row=r_idx, column=1, value=row.Code)
        code_cell.font      = BOLD_FONT
        code_cell.border    = _thin_border()
        code_cell.alignment = CTR_ALIGN

        # Category label
        lbl = ws.cell(row=r_idx, column=2, value=row.Category)
        lbl.font      = NORM_FONT
        lbl.border    = _thin_border()
        lbl.alignment = WRAP_ALIGN

        # Division values
        for c_idx, div in enumerate(DIVISIONS, 3):
            val = getattr(row, div, 0)
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font      = NORM_FONT
            cell.border    = _thin_border()
            cell.alignment = WRAP_ALIGN if value_col == "caller" else CTR_ALIGN

        # Total
        tot = ws.cell(row=r_idx, column=3 + len(DIVISIONS), value=row.Total)
        tot.font      = BOLD_FONT
        tot.border    = _thin_border()
        tot.alignment = CTR_ALIGN

    _auto_width(ws)
    _freeze(ws, "C3")


def write_acupick_categories(wb: Workbook, df: pd.DataFrame):
    _write_category_sheet(wb, "Acupick Incident Categories", df, value_col="count")


def write_acupick(wb: Workbook, df: pd.DataFrame):
    _write_category_sheet(wb, "Acupick", df, value_col="count")


def write_ops_issues(wb: Workbook, df: pd.DataFrame):
    _write_category_sheet(wb, "Ops Issues", df, value_col="caller")


def write_summary(wb: Workbook, summary: dict):
    ws        = wb.create_sheet("Summary")
    date_from = summary["date_from"]
    date_to   = summary["date_to"]
    daily     = summary["daily"]
    totals    = summary["totals"]
    TYPES     = ["SYSTEM", "OPS", "PE"]

    row_num = 1

    # ── Totals section ───────────────────────────────────────────────
    ws.cell(row=row_num, column=1, value=f"{date_from} to {date_to}").font = BOLD_FONT
    for c_idx, hdr in enumerate(TYPES + ["Total"], 2):
        cell = ws.cell(row=row_num, column=c_idx, value=hdr)
        cell.fill = HDR_FILL; cell.font = HDR_FONT
        cell.border = _thin_border(); cell.alignment = CTR_ALIGN
    row_num += 1

    for r in totals:
        ws.cell(row=row_num, column=1, value=r["Configuration Item"]).font = NORM_FONT
        ws.cell(row=row_num, column=1).border = _thin_border()
        for c_idx, t in enumerate(TYPES + ["Total"], 2):
            cell = ws.cell(row=row_num, column=c_idx, value=r.get(t, 0))
            cell.font = BOLD_FONT if t == "Total" else NORM_FONT
            cell.border = _thin_border(); cell.alignment = CTR_ALIGN
        row_num += 1

    row_num += 1  # blank separator

    # ── Per-day sections ─────────────────────────────────────────────
    for day_block in daily:
        # Day header row
        ws.cell(row=row_num, column=1, value=day_block["date"]).font = BOLD_FONT
        ws.cell(row=row_num, column=1).fill = SUB_FILL
        for c_idx, hdr in enumerate(TYPES, 2):
            cell = ws.cell(row=row_num, column=c_idx, value=hdr)
            cell.fill = SUB_FILL; cell.font = SUB_FONT
            cell.border = _thin_border(); cell.alignment = CTR_ALIGN
        row_num += 1

        for r in day_block["data"]:
            ws.cell(row=row_num, column=1, value=r["Configuration Item"]).font = NORM_FONT
            ws.cell(row=row_num, column=1).border = _thin_border()
            for c_idx, t in enumerate(TYPES, 2):
                cell = ws.cell(row=row_num, column=c_idx, value=r.get(t, 0))
                cell.font = NORM_FONT; cell.border = _thin_border(); cell.alignment = CTR_ALIGN
            row_num += 1

        row_num += 1  # blank separator between days

    _auto_width(ws)
    _freeze(ws, "B2")


# ── Main entry point ─────────────────────────────────────────────────────────

def build_workbook(processed: dict) -> bytes:
    wb = Workbook()
    wb.remove(wb.active)          # remove default empty sheet

    # Build in desired tab order
    write_ops_issues(wb, processed["ops_issues"])
    write_summary(wb, processed["summary"])
    write_acupick_categories(wb, processed["categories"])
    write_inc(wb, processed["inc"])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()