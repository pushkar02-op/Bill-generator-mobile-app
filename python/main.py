# main.py
from datetime import datetime
import json
import pandas as pd
from pathlib import Path

from bill.excel_custom_generator import generate_excel_bill
from utils.invoice_tracker import get_next_invoice_number
from scripts.load_product_data import extract_po_and_date_from_filename  

def transform_data_for_bill(df):
    # … your existing transform_data_for_bill unchanged …
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce", downcast="integer").fillna(0).astype(int)
    df["Landing Rate"] = pd.to_numeric(df["Landing Rate"], errors="coerce", downcast="float").fillna(0.0).astype(float)
    df["Item Code"]    = pd.to_numeric(df["Item Code"],    errors="coerce", downcast="integer").fillna(0).astype(int)
    df["HSN Code"]     = pd.to_numeric(df["HSN Code"],     errors="coerce", downcast="integer").fillna(0).astype(int)
    df["Product Description"] = df["Product Description"].astype(str).fillna("")
    df["Grammage"]              = df["Grammage"].astype(str).fillna("")
    df = df.dropna(subset=["Quantity","Landing Rate","Item Code","HSN Code","Product Description","Grammage"])
    items = []
    for _, row in df.iterrows():
        qty, rate = row["Quantity"], row["Landing Rate"]
        total = round(qty * rate, 2)
        items.append([
            row["Item Code"], row["HSN Code"],
            row["Product Description"].strip(), row["Grammage"].strip(),
            qty, rate, total,
            0.00, 0.0,
            0.00, 0.0,
            total
        ])
    return items[:-3] if len(items) >= 3 else items

def load_metadata(metadata_file="metadata.json"):
    return json.loads(Path(metadata_file).read_text())

def main():
    metadata = load_metadata("metadata.json")
    base_source = Path("data")
    base_target = Path("output")
    base_target.mkdir(parents=True, exist_ok=True)
    
    places = [key for key in metadata.keys() if key not in ["invoice_no", "GST", "PO", "delivery_date", "vendor_code"]]


    # iterate places defined in metadata
    for place in places:
        src_dir = base_source / place
        tgt_dir = base_target / place
        tgt_dir.mkdir(parents=True, exist_ok=True)

        # process each excel in the place’s source folder
        for file_path in sorted(src_dir.glob("*.xls*")):
            # 1) extract PO & date
            po, raw_date = extract_po_and_date_from_filename(file_path.name)
            # parse to datetime so formatting consistent
            try:
                dt = datetime.strptime(raw_date, "%d-%m-%Y")
                delivery_date = dt.strftime("%d-%m-%Y")
                file_date_part = dt.strftime("%Y-%m-%d")
            except:
                delivery_date, file_date_part = raw_date, raw_date

            # 2) read df and transform
            df = pd.read_excel(file_path)
            items = transform_data_for_bill(df)

            # 3) assemble metadata for this run
            run_meta = {
                **metadata,  # common fields: vendor_code, GST, etc.
                "PO": po,
                "delivery_date": delivery_date,
                "invoice_no": str(get_next_invoice_number()),
                "bill_to": metadata[place]["bill_to"],
                "place_of_supply": metadata[place]["place_of_supply"],
                "site_code": metadata[place]["site_code"],
                "items": items
            }

            # 4) build output filename
            out_fname = f"{place}_{file_date_part}_{po}.xlsx"
            out_path = tgt_dir / out_fname

            # 5) generate
            generate_excel_bill(run_meta, filename=str(out_path))
            print(f"Generated: {out_path}")

if __name__ == "__main__":
    main()
