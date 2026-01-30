#!/usr/bin/env python3
"""
PDF to Excel Converter

Extracts tables from PDF files and converts them to Excel format.

Dependencies:
    pip install pdfplumber pandas openpyxl

Usage:
    python pdf_to_excel.py input.pdf [output.xlsx]

Examples:
    python pdf_to_excel.py report.pdf
    python pdf_to_excel.py report.pdf output.xlsx
"""

import sys
import os
import pdfplumber
from openpyxl import Workbook


def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF file."""
    all_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_tables = page.extract_tables()
            for table_idx, table in enumerate(page_tables):
                if table:
                    for row in table:
                        all_rows.append(row)

    return all_rows


def convert_pdf_to_excel(pdf_path, excel_path=None, skip_rows=0):
    """
    Convert PDF file to Excel spreadsheet.

    Args:
        pdf_path: Path to input PDF file
        excel_path: Path to output Excel file (optional)
        skip_rows: Number of rows to skip from the beginning (default 0)

    Returns:
        Path to created Excel file
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if excel_path is None:
        excel_path = os.path.splitext(pdf_path)[0] + ".xlsx"

    all_rows = extract_tables_from_pdf(pdf_path)

    if not all_rows:
        print(f"Warning: No tables found in {pdf_path}")
        return None

    if skip_rows > 0:
        all_rows = all_rows[skip_rows:]

    wb = Workbook()
    ws = wb.active
    ws.title = "Tables"

    for row_idx, row in enumerate(all_rows, start=1):
        for col_idx, value in enumerate(row, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    wb.save(excel_path)

    print(f"Converted {pdf_path} -> {excel_path}")
    print(f"Extracted {len(all_rows)} total rows")

    return excel_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_excel.py <input.pdf> [output.xlsx]")
        print("\nExample:")
        print("  python pdf_to_excel.py report.pdf")
        print("  python pdf_to_excel.py report.pdf output.xlsx")
        sys.exit(1)

    pdf_path = sys.argv[1]
    excel_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = convert_pdf_to_excel(pdf_path, excel_path)
        if result:
            print("Conversion completed successfully!")
        else:
            print("No tables found in PDF.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
