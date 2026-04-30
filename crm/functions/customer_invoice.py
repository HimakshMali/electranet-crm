from io import BytesIO
import os
from num2words import num2words

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


LOGO_PATH = "crm/functions/logo.png"
SIGN_PATH = "crm/functions/sig.png"

# --- Premium Corporate Color Palette ---
CORPORATE_NAVY = colors.HexColor("#0F172A")
BRAND_BLUE = colors.HexColor("#1D4ED8")
SOFT_BLUE_BG = colors.HexColor("#F1F5F9")
BORDER_COLOR = colors.HexColor("#E2E8F0")
TEXT_MAIN = colors.HexColor("#334155")
WHITE = colors.white

PASTEL_GREY = colors.HexColor("#F8FAFC")
PASTEL_GREEN = colors.HexColor("#F0FDF4")
PASTEL_RED = colors.HexColor("#FEF2F2")

GREEN_TEXT = colors.HexColor("#166534")
RED_TEXT = colors.HexColor("#991B1B")
NAVY_TEXT = colors.HexColor("#0F172A")


styles = getSampleStyleSheet()


def safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0


def safe_text(value):
    return "" if value is None else str(value)


def money(value):
    return f"{safe_float(value):,.2f}"


def get_image(path, width, height):
    if path and os.path.exists(path):
        img = Image(path)
        img.drawWidth = width
        img.drawHeight = height
        return img
    return ""


def generate_customer_invoice_pdf(data):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,

        # ✅ Reduced page margins slightly to create more usable space
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm
    )

    PAGE_W = A4[0] - 28 * mm
    elements = []

    customer = data.get("customer", {})
    invoice = data.get("invoice", {})
    payment = data.get("payment", {})
    products = data.get("products", [])

    copy_type = safe_text(invoice.get("copy_type", "Original"))

    # ======================================================
    # COMPACT TYPOGRAPHY
    # ======================================================

    normal = ParagraphStyle(
        "normal",
        parent=styles["Normal"],
        fontSize=7.2,
        leading=8.6,
        textColor=TEXT_MAIN,
    )

    normal_right = ParagraphStyle(
        "normal_right",
        parent=normal,
        alignment=TA_RIGHT,
    )

    bold_title = ParagraphStyle(
        "bold_title",
        parent=normal,
        fontSize=8,
        leading=9.2,
        fontName="Helvetica-Bold",
        textColor=CORPORATE_NAVY,
    )

    invoice_header = ParagraphStyle(
        "invoice_header",
        parent=styles["Normal"],
        fontSize=16,
        leading=18,
        fontName="Helvetica-Bold",
        textColor=BRAND_BLUE,
        alignment=TA_RIGHT,
        spaceAfter=0,
    )

    copy_type_style = ParagraphStyle(
        "copy_type_style",
        parent=styles["Normal"],
        fontSize=7,
        leading=8,
        fontName="Helvetica",
        textColor=TEXT_MAIN,
        alignment=TA_RIGHT,
    )

    table_header = ParagraphStyle(
        "table_header",
        parent=styles["Normal"],
        fontSize=7.2,
        leading=8.4,
        fontName="Helvetica-Bold",
        textColor=WHITE,
        alignment=TA_CENTER,
    )

    wrap = ParagraphStyle(
        "wrap",
        parent=styles["Normal"],
        fontSize=7.2,
        leading=8.5,
        wordWrap="CJK",
        textColor=TEXT_MAIN,
    )

    amount_cell_style = ParagraphStyle(
        "amount_cell_style",
        parent=styles["Normal"],
        fontSize=7.2,
        leading=8.5,
        textColor=TEXT_MAIN,
        alignment=TA_RIGHT,
    )

    amount_cell_bold = ParagraphStyle(
        "amount_cell_bold",
        parent=amount_cell_style,
        fontName="Helvetica-Bold",
        textColor=CORPORATE_NAVY,
    )

    center_small = ParagraphStyle(
        "center_small",
        parent=normal,
        alignment=TA_CENTER,
    )

    # ======================================================
    # TOP HEADER: LOGO & INVOICE TITLE
    # ======================================================

    logo = get_image(LOGO_PATH, 38 * mm, 13.4 * mm)

    header_table = Table([
        [
            logo,
            [
                Paragraph("INVOICE", invoice_header),
                Paragraph(f"({copy_type.upper()})", copy_type_style)
            ]
        ]
    ], colWidths=[PAGE_W / 2, PAGE_W / 2])

    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),

        # ✅ Reduced from 10
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(header_table)

    # ✅ Reduced from Spacer(1, 5)
    elements.append(Spacer(1, 2))

    # ======================================================
    # CLEAN, OPEN-GRID DETAILS SECTION
    # ======================================================

    col_1 = Table([
        [Paragraph("<b>ELECTRANET POWER PVT LTD</b>", bold_title)],
        [Paragraph("27/1 Onkar Nagar, Dhar", normal)],
        [Paragraph("GSTIN: 23AAHCE4008N1ZO", normal)],
        [Paragraph("Phone: 9993828779", normal)],

        # ✅ Reduced internal gap
        [Spacer(1, 3)],

        [Paragraph("<font color='#1D4ED8'><b>BILLED TO</b></font>", bold_title)],
        [Paragraph(f"<b>{safe_text(customer.get('name'))}</b>", normal)],
        [Paragraph(safe_text(customer.get("address")), normal)],
        [Paragraph(f"Phone: {safe_text(customer.get('phone'))} | Email: {safe_text(customer.get('email'))}", normal)],
        [Paragraph(f"GSTIN: {safe_text(customer.get('gstin'))}", normal)],
    ], colWidths=[PAGE_W * 0.5])

    col_2 = Table([
        [Paragraph("<b>Invoice Details</b>", bold_title)],
        [Paragraph(f"<b>Invoice No:</b> {safe_text(invoice.get('number'))}", normal)],
        [Paragraph(f"<b>Date:</b> {safe_text(invoice.get('date'))}", normal)],
        [Paragraph(f"<b>Vehicle:</b> {safe_text(invoice.get('vehicle'))}", normal)],

        # ✅ Reduced internal gap
        [Spacer(1, 3)],

        [Paragraph("<font color='#1D4ED8'><b>DELIVERY & BANK DETAILS</b></font>", bold_title)],
        [Paragraph(f"<b>Delivery:</b> {safe_text(customer.get('delivery'))}", normal)],

        # ✅ Reduced internal gap
        [Spacer(1, 2)],

        [Paragraph("<b>Bank:</b> State Bank of India", normal)],
        [Paragraph("<b>A/C No:</b> 20511247609 | <b>IFSC:</b> SBIN0003417", normal)],
        [Paragraph("<b>Branch:</b> Raghunathpura Dhar", normal)],
    ], colWidths=[PAGE_W * 0.5])

    details_table = Table(
        [[col_1, col_2]],
        colWidths=[PAGE_W * 0.5, PAGE_W * 0.5],
    )

    details_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, -1), 1.2, CORPORATE_NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, CORPORATE_NAVY),

        # ✅ Reduced from 12
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
    ]))

    elements.append(details_table)

    # ✅ Reduced from 15
    elements.append(Spacer(1, 6))

    # ======================================================
    # PRODUCT TABLE WITH PRECISION WIDTHS
    # ======================================================

    table_data = [[
        Paragraph("No", table_header),
        Paragraph("Particulars", ParagraphStyle("th_left", parent=table_header, alignment=TA_LEFT)),
        Paragraph("HSN", table_header),
        Paragraph("Qty", table_header),
        Paragraph("Rate", ParagraphStyle("th_right", parent=table_header, alignment=TA_RIGHT)),
        Paragraph("CGST", ParagraphStyle("th_right", parent=table_header, alignment=TA_RIGHT)),
        Paragraph("SGST", ParagraphStyle("th_right", parent=table_header, alignment=TA_RIGHT)),
        Paragraph("Total", ParagraphStyle("th_right", parent=table_header, alignment=TA_RIGHT)),
    ]]

    subtotal = 0

    for index, item in enumerate(products, 1):
        name = safe_text(item.get("name"))
        hsn = safe_text(item.get("hsn"))
        qty = safe_float(item.get("qty", 0))
        price = safe_float(item.get("price", 0))
        gst = safe_float(item.get("gst", 0))

        line_total = price * qty
        subtotal += line_total

        gst_multiplier = 1 + (gst / 100)
        base_rate = price / gst_multiplier if gst_multiplier else price

        taxable = base_rate * qty
        gst_amount = line_total - taxable
        cgst = gst_amount / 2
        sgst = gst_amount / 2

        total_with_calc = Paragraph(
            f"""<b>{money(line_total)}</b><br/>
            <font size="5.6" color="#64748B">({money(price)} × {qty:.0f})</font>""",
            amount_cell_bold
        )

        table_data.append([
            Paragraph(str(index), center_small),
            Paragraph(name, wrap),
            Paragraph(hsn, center_small),
            Paragraph(f"{qty:.0f}", center_small),
            Paragraph(money(base_rate), amount_cell_style),
            Paragraph(money(cgst), amount_cell_style),
            Paragraph(money(sgst), amount_cell_style),
            total_with_calc,
        ])

    product_count = len(products)
    minimum_rows = 5

    if product_count < minimum_rows:
        for empty_index in range(product_count + 1, minimum_rows + 1):
            table_data.append([str(empty_index), "", "", "", "", "", "", ""])

    discount = safe_float(invoice.get("discount", 0))
    final_amount = max(subtotal - discount, 0)

    if discount > 0:
        table_data.append([
            "", "", "", "", "", "",
            Paragraph("Subtotal", normal_right),
            Paragraph(money(subtotal), amount_cell_style)
        ])
        table_data.append([
            "", "", "", "", "", "",
            Paragraph("Discount", normal_right),
            Paragraph(money(discount), amount_cell_style)
        ])

    table_data.append([
        "", "", "", "", "", "",
        Paragraph("<b>Grand Total</b>", bold_title),
        Paragraph(f"<b>Rs. {money(final_amount)}</b>", amount_cell_bold)
    ])

    product_table = Table(
        table_data,
        colWidths=[25, 145, 45, 30, 60, 60, 60, 75],
        repeatRows=1,
    )

    product_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CORPORATE_NAVY),

        # ✅ Slightly compact header
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),

        ("LINEBELOW", (0, 1), (-1, -2), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # ✅ Table still readable, but slightly compact
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ("BACKGROUND", (6, -1), (7, -1), SOFT_BLUE_BG),
        ("LINEABOVE", (0, -1), (-1, -1), 1.2, CORPORATE_NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 1.2, CORPORATE_NAVY),
    ]))

    elements.append(product_table)

    # ✅ Reduced from 10
    elements.append(Spacer(1, 5))

    # ======================================================
    # AMOUNT IN WORDS
    # ======================================================

    try:
        words = num2words(round(final_amount), lang="en_IN").title()
        amount_words = f"Rupees {words} Only."
    except Exception:
        amount_words = ""

    words_table = Table(
        [[Paragraph(f"<b>Amount in Words:</b> {amount_words}", normal)]],
        colWidths=[PAGE_W],
    )

    words_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT_BLUE_BG),

        # ✅ Reduced from 8
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(words_table)

    # ✅ Reduced from 15
    elements.append(Spacer(1, 6))

    # ======================================================
    # PAYMENT SUMMARY
    # ======================================================

    billed_amount = safe_float(payment.get("billed_amount", final_amount))
    paid_amount = safe_float(payment.get("paid_amount", 0))

    if "remaining_amount" in payment:
        remaining_amount = safe_float(payment.get("remaining_amount"))
    else:
        remaining_amount = final_amount - paid_amount

    payment_table = Table([
        [
            Paragraph("<b>Ledger Billed Amount</b>", normal),
            Paragraph(
                f"<b>Rs. {money(billed_amount)}</b>",
                ParagraphStyle("p_amt", parent=normal, alignment=TA_RIGHT, textColor=NAVY_TEXT)
            )
        ],
        [
            Paragraph("<b>Amount Paid By Customer</b>", normal),
            Paragraph(
                f"<b>Rs. {money(paid_amount)}</b>",
                ParagraphStyle("p_paid", parent=normal, alignment=TA_RIGHT, textColor=GREEN_TEXT)
            )
        ],
        [
            Paragraph("<b>Remaining Amount</b>", normal),
            Paragraph(
                f"<b>Rs. {money(remaining_amount)}</b>",
                ParagraphStyle("p_rem", parent=normal, alignment=TA_RIGHT, textColor=RED_TEXT)
            )
        ],
    ], colWidths=[PAGE_W * 0.5, PAGE_W * 0.25])

    payment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), PASTEL_GREY),
        ("BACKGROUND", (0, 1), (1, 1), PASTEL_GREEN),
        ("BACKGROUND", (0, 2), (1, 2), PASTEL_RED),
        ("LINEBELOW", (0, 0), (1, 0), 1, WHITE),
        ("LINEBELOW", (0, 1), (1, 1), 1, WHITE),

        # ✅ Reduced from 6
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))

    payment_wrapper = Table(
        [["", payment_table]],
        colWidths=[PAGE_W * 0.25, PAGE_W * 0.75]
    )

    elements.append(payment_wrapper)

    # ✅ Reduced from 20
    elements.append(Spacer(1, 7))

    # ======================================================
    # FOOTER: TERMS, DECLARATION & SIGNATURE
    # ======================================================

    terms = Paragraph(
        """
        <b>Terms & Conditions:</b><br/>
        1. Goods once sold will not be taken back.<br/>
        2. Subject to Dhar and Indore jurisdiction.<br/>
        <b>Declaration:</b><br/>
        We declare that this invoice shows the actual price of the goods/services
        described and that all particulars are true and correct.<br/>
        <b>For Queries Contact:</b>
        Phone: 9993828779 | Email: electranetpvt@gmail.com
        """,
        ParagraphStyle(
            "footer_terms",
            parent=normal,
            fontSize=6.9,
            leading=8,
            textColor=TEXT_MAIN
        )
    )

    # ✅ Slightly smaller signature
    sign = get_image(SIGN_PATH, 27 * mm, 22.5 * mm)

    sign_block = Table([
        [Paragraph(
            "<b>For M/S ELECTRANET POWER PVT LTD</b>",
            ParagraphStyle(
                "for_company",
                parent=normal,
                fontSize=7.2,
                leading=8.5,
                fontName="Helvetica-Bold",
                alignment=TA_CENTER
            )
        )],

        # ✅ Reduced from 4
        [Spacer(1, 1)],

        [sign],
        [Paragraph(
            "Authorized Signatory",
            ParagraphStyle(
                "auth",
                parent=normal,
                fontSize=7,
                leading=8,
                alignment=TA_CENTER
            )
        )],
    ], colWidths=[PAGE_W * 0.4])

    sign_block.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        # ✅ Remove extra internal padding
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    footer_table = Table(
        [[terms, sign_block]],
        colWidths=[PAGE_W * 0.6, PAGE_W * 0.4],
    )

    footer_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, -1), 1, BORDER_COLOR),

        # ✅ Reduced from 12
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(footer_table)

    pdf.build(elements)
    buffer.seek(0)
    return buffer