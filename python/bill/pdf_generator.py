# bill/pdf_generator.py
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import  ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def generate_pdf_bill(data: dict, filename: str):
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4), rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
    story = []

    page_width = landscape(A4)[0] - 10 - 10
    
    # === HEADER (Green Box Equivalent) ===
    header1 = ParagraphStyle(
        "Header1", fontName="Helvetica-BoldOblique",
        fontSize=15, leading=18, alignment=1  # center
    )
    headerN = ParagraphStyle(
        "HeaderN", fontName="Helvetica-BoldOblique",
        fontSize=12, leading=14, alignment=1
    )
    
    header_data = [
        [Paragraph("TAX INVOICE",                 header1)],
        [Paragraph("A.G AGRO",                    headerN)],
        [Paragraph("TEGHRA,BEGUSARAI-851133",      headerN)],
        [Paragraph("10HVGPD2399M1ZC",             headerN)],
    ]

    tbl = Table(
        header_data,
        colWidths=[page_width],
        rowHeights=[36, 14, 14, 14],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#92D050")),
            ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            # no box/border so it matches Excel’s merged cell exactly
        ]
    )

    story.append(tbl)
    

    # === BILL TO / SUPPLY / DETAILS SECTION (Blue Box Equivalent) ===
    # compute widths: each spans 4 Excel columns out of 12
    col_width = page_width / 3

    # a simple bold-italic style
    hdr_style = ParagraphStyle(
        "SectionHeader",
        fontName="Helvetica-BoldOblique",
        fontSize=10,
        alignment=0,  # left
        leading=12
    )

    bill_todata = [
        [
            Paragraph("BILL TO",          hdr_style),
            Paragraph("PLACE OF SUPPLY",  hdr_style),
            Paragraph("BILL DETAILS:",    hdr_style),
        ]
    ]

    tbl = Table(
        bill_todata,
        colWidths=[col_width, col_width, col_width],
        rowHeights=[12],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFC000")),
            ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]
    )

    story.append(tbl)
    
    page_width = landscape(A4)[0] - 20
    col_width = page_width / 3

    # style for the text
    content_style = ParagraphStyle(
        "Content",
        fontName="Helvetica-BoldOblique",
        fontSize=9,
        leading=11,
        alignment=0,      # left
    )
    # prepare the three pieces of content
    bill_to = Paragraph(data["bill_to"].replace("\n", "<br/>"), content_style)
    place_of_supply = Paragraph(data["place_of_supply"].replace("\n", "<br/>"), content_style)
    bill_details = Paragraph(
        f"<b><i>INVOICE NO:</i></b> {data['invoice_no']}<br/>"
        f"<b><i>DELIVERY DATE:</i></b> {data['delivery_date']}<br/>"
        f"<b><i>VENDOR CODE:</i></b> {data['vendor_code']}<br/>"
        f"<b><i>SITE CODE:</i></b> {data['site_code']}",
        content_style
    )

    # 2 rows, but we merge each column over both rows
    table_data = [
        [bill_to, place_of_supply, bill_details],
        ["",       "",              ""           ]
    ]

    tbl = Table(
        table_data,
        colWidths=[col_width]*3,
        rowHeights=[36, 36],
        style=[
            # blue fill over entire block
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#D9E1F2")),
            # span each cell over both rows
            ("SPAN", (0,0), (0,1)),
            ("SPAN", (1,0), (1,1)),
            ("SPAN", (2,0), (2,1)),
            # top alignment within each cell
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            # small padding so text isn't jammed at the very top-left
            ("LEFTPADDING",  (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
        ]
    )

    story.append(tbl)
    # === GST and PO
    half = page_width / 2

    # Build a one-row, two-column table with the right styling
    gst_po = Table(
        [[f"GST: {data['GST']}", f"PO-{data['PO']}"]],
        colWidths=[half, half],
        rowHeights=[12],     # exactly the 12-pt height you set in Excel
        style=[
            # Exact same light blue fill
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#D9E1F2')),
            # Center horizontally & vertically
            ('ALIGN',   (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',  (0, 0), (-1, -1), 'MIDDLE'),
            # Wrapped text (though these are short)
            ('WORDWRAP', (0, 0), (-1, -1), True),
            # Bold + italic font at size 9
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-BoldOblique'),
            # Small inner padding to match Excel cell padding
            ('TOPPADDING',    (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING',   (0, 0), (-1, -1), 4),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
        ]
    )

    story.append(gst_po)

    # 1) Build the table data
    headers = [
        "ARTICLE CODE","HSN CODE","Article Description","Grammage","Quantity",
        "Rate","Taxable Value","SGST Rate","SGST Amount","CGST Rate","CGST Amount","Total Amount"
    ]
    table_data = [headers]
    for item in data["items"]:
        # Format numbers as strings matching Excel formatting
        row = []
        for idx, val in enumerate(item):
            if idx in (0,1):          # integer codes
                row.append(f"{int(val)}")
            elif idx in (4,5,6,8,10,11):  # currency columns
                row.append(f"{val:,.2f}")
            elif idx in (7,9):        # percentage columns
                row.append(f"{val:.2%}")
            else:
                row.append(str(val))
        table_data.append(row)

    # 2) Compute column widths (you can adjust these ratios)
    #    Sum of ratios = 12 units
    ratios = [1,1,3,1.8,0.8,0.8,1.2,1,1,1,1,1.2]
    total_units = sum(ratios)
    page_width = landscape(A4)[0] - 20  # margins=10+10
    col_widths = [page_width * r/total_units for r in ratios]

    # 3) Create the Table
    tbl = Table(table_data,
                colWidths=col_widths,
                rowHeights=[23] + [None]*(len(table_data)-1),
                repeatRows=1)

    # 4) Style it to match Excel exactly
    style = TableStyle()

    # — Header row styling —
    style.add('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FFC000'))
    style.add('TEXTCOLOR',  (0,0), (-1,0), colors.black)
    style.add('FONTNAME',   (0,0), (-1,0), 'Helvetica-BoldOblique')  # bold+italic
    style.add('FONTSIZE',   (0,0), (-1,0), 7)
    style.add('ALIGN',      (0,0), (-1,0), 'CENTER')
    style.add('VALIGN',     (0,0), (-1,0), 'MIDDLE')
    style.add('FONTSIZE', (0, 1), (-1, -1), 8) 


    # — Borders around every cell —
    style.add('GRID',       (0,0), (-1,-1), 0.5, colors.black)

    # — Data rows styling: alternating fill + alignment + wrap —
    for row_idx in range(1, len(table_data)):
        fill_color = colors.HexColor('#FFF2CC') if (row_idx % 2)==1 else colors.white
        style.add('BACKGROUND', (0,row_idx), (-1,row_idx), fill_color)
        style.add('VALIGN',     (0,row_idx), (-1,row_idx), 'TOP')
        style.add('WORDWRAP',   (0,row_idx), (-1,row_idx), True)
        # Right-align numeric columns
        for col_idx in (0,1):
            style.add('ALIGN', (col_idx, row_idx), (col_idx, row_idx), 'CENTER')
        for col_idx in (4,5,6,7,8,9,10,11):
            style.add('ALIGN', (col_idx, row_idx), (col_idx, row_idx), 'RIGHT')

    tbl.setStyle(style)

    # 5) Add to your story
    story.append(tbl)
    
    sum_cols = [5, 7, 8, 9, 10, 11, 12]
    # data["items"] is a list of rows, each row being a list of 12 values
    subtotals = {}
    for col in sum_cols:
        # Python indexes from 0
        idx = col - 1
        subtotals[col] = sum(row[idx] for row in data["items"])

    # 2. build the PDF row data (12 cells)
    row_data = []
    for col in range(1, 13):
        if col == 1:
            row_data.append("Sub Total")
        elif col in sum_cols:
            val = subtotals[col]
            if col in (8, 10):
                # SGST / CGST percent columns
                row_data.append(f"{val:.2%}")
            else:
                row_data.append(f"{val:,.2f}")
        else:
            row_data.append("")

    # 3. create a one-row Table with the same column widths as your main table
    subtotal_table = Table([row_data], colWidths=col_widths)

    # 4. style it to match Excel's footer
    subtotal_table.setStyle(TableStyle([
        # thin borders around every cell
        ('GRID',       (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME',   (0,0), (-1,-1),   'Helvetica-Bold'),
        # right-align the label and the numeric columns
        ('ALIGN',      (0,0), (0,0),   'RIGHT'),
        ('ALIGN',      (4,0), (4,0),   'RIGHT'),  # Quantity
        ('ALIGN',      (6,0), (6,0),   'RIGHT'),  # Taxable Value
        ('ALIGN',      (7,0), (7,0),   'RIGHT'),  # SGST Rate
        ('ALIGN',      (8,0), (8,0),   'RIGHT'),  # SGST Amount
        ('ALIGN',      (9,0), (9,0),   'RIGHT'),  # CGST Rate
        ('ALIGN',      (10,0),(10,0),  'RIGHT'),  # CGST Amount
        ('ALIGN',      (11,0),(11,0),  'RIGHT'),  # Total Amount
        # you can shrink the font slightly if you like
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        # optionally highlight the label cell background
        ('BACKGROUND',(0,0),(0,0),colors.whitesmoke),
    ]))

    story.append(subtotal_table)
    
        # === FOOTER: Misc. Charges & Grand Total ===
    misc_style = ParagraphStyle(
        name="Misc",
        fontSize=9,
        leading=11,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName="Helvetica-BoldOblique",
    )
    grand_style = ParagraphStyle(
        name="Grand",
        fontSize=9,
        leading=11,
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName="Helvetica-BoldOblique",
    )

    story.append(Paragraph(
        "Misc. Charges (Including Freight, Octroi, Loading, Unloading, etc.)",
        misc_style,
    ))
    story.append(Paragraph(
        "Grand Total (Rounded Off)",
        grand_style,
    ))

    # === Blank Row ===
    story.append(Spacer(1, 12))

    # === THANK YOU ROW ===
    thank_style = ParagraphStyle(
        name="ThankYou",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        fontName="Helvetica-BoldOblique",
        spaceAfter=12,
    )
    story.append(Paragraph("THANK YOU FOR YOUR BUSINESS", thank_style))

    # === Signature Line at bottom-left ===
    sig_style = ParagraphStyle(
        name="Signature",
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
    )
    story.append(Paragraph("Signature", sig_style))

    # === Final PDF generation ===
    doc.build(story)
