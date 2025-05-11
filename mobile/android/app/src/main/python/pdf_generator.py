from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf_bill(data: dict, out_path: str) -> str:
    """
    Generates a PDF invoice at out_path, using the same layout as the Excel version.
    Returns the PDF file path.
    """
    # Create PDF document in landscape A4
    doc = SimpleDocTemplate(
        out_path,
        pagesize=landscape(A4),
        leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18
    )
    styles = getSampleStyleSheet()
    story = []

    # 1) Header rows
    header_texts = ["TAX INVOICE", "A.G AGRO", "TEGHRA,BEGUSARAI-851133", data["GST"]]
    for i, txt in enumerate(header_texts):
        style = styles["Heading1"] if i==0 else styles["Heading3"]
        p = Paragraph(txt, style)
        story.append(p)
    story.append(Spacer(1, 12))

    # 2) Bill info table
    info_data = [
        ["BILL TO",           "PLACE OF SUPPLY",       "BILL DETAILS"],
        [
            data["bill_to"],
            data["place_of_supply"],
            (f"INVOICE NO: {data['invoice_no']}<br/>"
             f"DATE: {data['delivery_date']}<br/>"
             f"VENDOR: {data['vendor_code']}<br/>"
             f"SITE CODE: {data['site_code']}")
        ]
    ]
    t = Table(info_data, colWidths=[180,180,300])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.Color(1,0.75,0)),   # orange
        ("TEXTCOLOR",  (0,0), (-1,0), colors.black),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,1), "TOP"),
        ("BOX",        (0,0), (-1,-1), 1, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # 3) Items table
    hdrs = [
        "ARTICLE CODE","HSN CODE","Article Description","Grammage","Quantity",
        "Rate","Taxable Value","SGST Rate","SGST Amount",
        "CGST Rate","CGST Amount","Total Amount"
    ]
    data_rows = [hdrs] + data["items"]
    col_widths = [60, 60, 140, 60, 50, 60, 70, 50, 70, 50, 70, 80]

    tbl = Table(data_rows, colWidths=col_widths, repeatRows=1)
    # Style: header background, stripe rows
    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.Color(1,0.75,0)),   # header
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-BoldOblique"),
        ("FONTSIZE",   (0,0), (-1,0), 10),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.black),
    ])
    # Alternate row shading
    for row_i in range(1, len(data_rows)):
        bg = colors.whitesmoke if row_i%2==0 else colors.lightgrey
        style.add("BACKGROUND", (0,row_i), (-1,row_i), bg)
    tbl.setStyle(style)
    story.append(tbl)

    # 4) Footer: Sub Total
    story.append(Spacer(1,12))
    subtotal = sum(item[6] for item in data["items"])
    foot = Paragraph(f"<b>Sub Total:</b> {subtotal:,.2f}", styles["Normal"])
    story.append(foot)

    doc.build(story)
    return out_path
