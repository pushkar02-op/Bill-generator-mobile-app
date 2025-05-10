from datetime import datetime
from pathlib import Path
import pandas as pd

def extract_po_and_date_from_filename(filename: str):
    """
    Extract PO number and delivery date from a structured filename.
    Example: '15467510000244_20250422_055526.xlsx' -> ('15467510000244', '22-04-2025')
    """
    name = Path(filename).stem
    parts = name.split("_")

    if len(parts) >= 2:
        po_number = parts[0]
        try:
            delivery_date = datetime.strptime(parts[1], "%Y%m%d").strftime("%d-%m-%Y")
        except ValueError:
            delivery_date = "Invalid Date"
    else:
        po_number = "N/A"
        delivery_date = "N/A"

    return po_number, delivery_date


def get_latest_excel_file(folder_path: str = "data/") -> Path:
    """
    Return the Path of the latest Excel file in the specified folder.
    """
    folder = Path(folder_path)
    excel_files = list(folder.glob("*.xlsx")) + list(folder.glob("*.xls"))

    if not excel_files:
        raise FileNotFoundError(f"No Excel files found in {folder_path}")

    latest_file = max(excel_files, key=lambda f: f.stat().st_mtime)
    return latest_file


def load_latest_excel_with_metadata(folder_path: str = "data/"):
    """
    Loads the latest Excel file and returns both DataFrame and extracted metadata.
    Returns:
        df (pd.DataFrame): Loaded Excel data.
        file_path (str): Full path of the loaded file.
        po_number (str): Extracted PO number from filename.
        delivery_date (str): Extracted Delivery Date from filename.
    """
    latest_file = get_latest_excel_file(folder_path)
    df = pd.read_excel(latest_file)

    po_number, delivery_date = extract_po_and_date_from_filename(latest_file.name)

    return df, str(latest_file), po_number, delivery_date
