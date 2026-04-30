from django.db import transaction
from decimal import Decimal
from crm.models import Invoice, InvoiceItem, Customer, Products

def create_full_invoice(user, customer_id, invoice_data, items_data):
    """
    Handles the business logic of saving an invoice and its line items.
    Ensures everything is saved cleanly in a single database transaction.
    """
    customer = Customer.objects.get(id=customer_id)
    
    with transaction.atomic():
        # 1. Create the base invoice
        invoice = Invoice.objects.create(
            customer=customer,
            created_by=user,
            invoice_number=invoice_data['number'],
            invoice_date=invoice_data['date'],
            discount=Decimal(invoice_data.get('discount', 0)),
            vehicle=invoice_data.get('vehicle', ''),
            total_amount=0  # Will calculate dynamically below
        )

        sub_total = Decimal('0.00')

        # 2. Create the items
        for item in items_data:
            qty = Decimal(item['quantity'])
            price = Decimal(item['unit_price'])
            line_total = qty * price

            product_obj = None
            if item.get('product_id'):
                product_obj = Products.objects.get(id=item['product_id'])

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product_obj,
                product_name=item['name'],
                hsn_code=item.get('hsn_code', ''),
                quantity=qty,
                unit_price=price,
                gst_rate=Decimal(item.get('gst_rate', 0)),
                total=line_total
            )

            sub_total += line_total

        # 3. Calculate and update final total
        invoice.total_amount = sub_total - invoice.discount
        invoice.save()

    return invoice