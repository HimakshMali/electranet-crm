from django.db.models import Sum
from crm.models import Customer, Invoice, Payment

def get_customer_ledger(customer_id):
    """
    Returns a summarized dictionary of a customer's billing history.
    """
    # prefetch_related optimizes the database query so it doesn't query the DB 
    # individually for every single payment on every single invoice.
    customer = Customer.objects.prefetch_related('invoices__payments').get(id=customer_id)
    invoices = customer.invoices.all().order_by('-invoice_date')
    
    total_billed = sum(inv.total_amount for inv in invoices)
    total_paid = sum(inv.total_paid for inv in invoices)
    total_due = total_billed - total_paid

    return {
        'customer': customer,
        'invoices': invoices,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'total_due': total_due
    }

def record_payment(user, invoice_id, amount, date, method, reference):
    invoice = Invoice.objects.get(id=invoice_id)
    
    payment = Payment.objects.create(
        invoice=invoice,
        recorded_by=user,
        amount_paid=amount,
        payment_date=date,
        payment_method=method,
        reference_id=reference
    )
    return payment