import json
import os

COUNTER_FILE = "invoice_counter.json"

def get_next_invoice_number():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            json.dump({"last_invoice": 1000}, f)

    with open(COUNTER_FILE, "r") as f:
        data = json.load(f)

    last = data.get("last_invoice", 1000)
    next_invoice = last + 1

    with open(COUNTER_FILE, "w") as f:
        json.dump({"last_invoice": next_invoice}, f)

    return next_invoice
