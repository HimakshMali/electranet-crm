from io import BytesIO
from num2words import num2words
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import os


# ================= IMAGE PATHS ================= #
# Add your real paths here
LOGO_PATH = "crm/functions/logo.png"
SIGN_PATH = "crm/functions/sig.png"


# ================= COLORS ================= #
BORDER = colors.HexColor("#222222")
LIGHT_GREY = colors.HexColor("#F4F4F4")
DARK = colors.HexColor("#111111")


# ================= STYLES ================= #
styles = getSampleStyleSheet()

normal = ParagraphStyle(
    "normal",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
)

small = ParagraphStyle(
    "small",
    parent=styles["Normal"],
    fontSize=7.5,
    leading=10,
)

bold = ParagraphStyle(
    "bold",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    fontName="Helvetica-Bold",
)

title = ParagraphStyle(
    "title",
    parent=styles["Normal"],
    fontSize=14,
    leading=18,
    alignment=1,
    fontName="Helvetica-Bold",
)

wrap_style = ParagraphStyle(
    "wrap",
    parent=styles["Normal"],
    fontSize=8,
    leading=10,
    wordWrap="CJK",
)


def safe(value, default=""):
    return default if value is None else value


def money(value):
    return f"{float(value):.2f}"


def make_paragraph(text, style=normal):
    return Paragraph(str(safe(text)).replace("\n", "<br/>"), style)


def get_image(path, width, height):
    if path and os.path.exists(path):
        return Image(path, width=width, height=height)
    return ""


# ================= MAIN FUNCTION ================= #

def generate_invoice_pdf(data):
    """
    data = {
        "customer": {
            "name": "",
            "address": "",
            "phone": "",
            "email": "",
            "gstin": "",
            "delivery": ""
        },
        "invoice": {
            "number": "",
            "date": "",
            "vehicle": "",
            "discount": 0,
            "paid_amount": 0,
            "copy_type": "Original"
        },
        "products": [
            {
                "name": "",
                "hsn": "",
                "qty": 1,
                "price": 0,   # GST included selling price
                "gst": 18
            }
        ]
    }
    """

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=22,
        leftMargin=22,
        topMargin=20,
        bottomMargin=20,
    )

    elements = []

    customer = data.get("customer", {})
    invoice = data.get("invoice", {})
    products = data.get("products", [])

    invoice_no = safe(invoice.get("number"))
    invoice_date = safe(invoice.get("date"))
    vehicle = safe(invoice.get("vehicle"))
    copy_type = safe(invoice.get("copy_type"), "Original")

    # ================= TITLE ================= #

    logo = get_image(LOGO_PATH, 28 * mm, 20 * mm)

    company_title = Paragraph(
        """
        <b>M/S ELECTRANET POWER PVT LTD</b><br/>
        <font size="8">27/1 Onkar Nagar, Dhar</font><br/>
        <font size="8">GSTIN: 23AAHCE4008N1ZO | Phone: 9993828779</font>
        """,
        title,
    )

    top_table = Table(
        [[logo, company_title, Paragraph(f"<b>{copy_type.upper()}</b>", bold)]],
        colWidths=[80, 365, 105],
    )

    top_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("ALIGN", (2, 0), (2, 0), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(top_table)

    invoice_heading = Table(
        [[Paragraph("<b>TAX INVOICE</b>", title)]],
        colWidths=[550],
    )
    invoice_heading.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(invoice_heading)

    # ================= COMPANY + INVOICE + BANK ================= #

    left_info = Paragraph(
        f"""
        <b>Invoice No:</b> {invoice_no}<br/>
        <b>Date:</b> {invoice_date}<br/>
        <b>Vehicle:</b> {vehicle}
        """,
        normal,
    )

    bank_info = Paragraph(
        """
        <b>Bank Details:</b><br/>
        Bank: State Bank of India<br/>
        A/C No: 20511247609<br/>
        IFSC: SBIN0003417<br/>
        Branch: Raghunathpura Dhar
        """,
        normal,
    )

    company_invoice_table = Table(
        [[left_info, bank_info]],
        colWidths=[275, 275],
    )

    company_invoice_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(company_invoice_table)

    # ================= CUSTOMER DETAILS ================= #

    customer_details = Paragraph(
        f"""
        <b>BILLED TO</b><br/>
        <b>{safe(customer.get("name"))}</b><br/>
        {safe(customer.get("address"))}<br/>
        Phone: {safe(customer.get("phone"))}<br/>
        Email: {safe(customer.get("email"))}<br/>
        GSTIN: {safe(customer.get("gstin"))}<br/>
        <br/>
        <b>Delivery Address:</b><br/>
        {safe(customer.get("delivery"))}
        """,
        normal,
    )

    customer_table = Table([[customer_details]], colWidths=[550])
    customer_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(customer_table)
    elements.append(Spacer(1, 8))

    # ================= PRODUCT CALCULATION ================= #

    table_data = [[
        "No", "Particulars", "HSN", "Qty", "Rate", "CGST", "SGST", "Total"
    ]]

    total_amount = 0

    for index, item in enumerate(products, start=1):
        name = safe(item.get("name"))
        hsn = safe(item.get("hsn"))
        qty = float(item.get("qty") or 0)
        unit_price = float(item.get("price") or 0)
        gst_rate = float(item.get("gst") or 0)

        gst_multiplier = 1 + (gst_rate / 100)
        base_rate = unit_price / gst_multiplier if gst_multiplier else unit_price

        taxable = base_rate * qty
        line_total = unit_price * qty
        total_gst = line_total - taxable

        cgst = total_gst / 2
        sgst = total_gst / 2

        total_amount += line_total

        table_data.append([
            str(index),
            Paragraph(name, wrap_style),
            hsn,
            f"{qty:.0f}",
            money(base_rate),
            money(cgst),
            money(sgst),
            money(line_total),
        ])

    discount = float(invoice.get("discount") or 0)
    paid_amount = float(invoice.get("paid_amount") or 0)

    sub_total = total_amount
    grand_total = total_amount - discount
    remaining_amount = grand_total - paid_amount

    if discount > 0:
        table_data.append(["", "", "", "", "", "", "Sub Total", money(sub_total)])
        table_data.append(["", "", "", "", "", "", "Discount", money(discount)])

    table_data.append(["", "", "", "", "", "", "Grand Total", money(grand_total) + " Rs"])

    if paid_amount > 0:
        table_data.append(["", "", "", "", "", "", "Paid", money(paid_amount) + " Rs"])
        table_data.append(["", "", "", "", "", "", "Remaining", money(remaining_amount) + " Rs"])

    product_table = Table(
        table_data,
        colWidths=[25, 180, 50, 35, 65, 65, 65, 65],
        repeatRows=1,
    )

    product_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GREY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (6, -1), (7, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(product_table)
    elements.append(Spacer(1, 8))

    # ================= AMOUNT IN WORDS ================= #

    try:
        words = num2words(round(grand_total), lang="en_IN").title()
        amount_words = f"Rupees {words} Only."
    except Exception:
        amount_words = ""

    amount_table = Table(
        [[Paragraph(f"<b>Amount in Words:</b> {amount_words}", normal)]],
        colWidths=[550],
    )

    amount_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(amount_table)
    elements.append(Spacer(1, 8))

    # ================= TERMS + DECLARATION ================= #

    terms = Paragraph(
        """
        <b>Terms & Conditions:</b><br/>
        1. Goods once sold will not be taken back.<br/>
        2. Subject to Dhar and Indore jurisdiction.<br/><br/>

        <b>Declaration:</b><br/>
        We declare that this invoice shows the actual price of the goods/services
        described and that all particulars are true and correct.<br/><br/>

        <b>For Queries Contact:</b><br/>
        Phone: 9993828779<br/>
        Email: electranetpvt@gmail.com
        """,
        small,
    )

    sign = get_image(SIGN_PATH, 38 * mm, 18 * mm)

    sign_block = Table(
        [
            [sign],
            [Paragraph("<b>For M/S ELECTRANET POWER PVT LTD</b>", small)],
            [Spacer(1, 10)],
            [Paragraph("<b>Authorized Signatory</b>", small)],
        ],
        colWidths=[210],
    )

    sign_block.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]))

    footer_table = Table(
        [[terms, sign_block]],
        colWidths=[340, 210],
    )

    footer_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(footer_table)

    # ================= BUILD PDF ================= #

    pdf.build(elements)
    buffer.seek(0)
    return buffer   