from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    invitation_code = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.role}"
    
class Leads(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=50,default='New')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Display_leads(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=50,default='New')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class Converted_leads(models.Model):
#     closed_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     source = models.CharField(max_length=100)
#     status = models.CharField(max_length=50,default='New')
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     rveneue_from_customer = models.IntegerField()
#     product_bought = models.CharField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     closed_at = models.DateTimeField(auto_now_add = True)

    
#     def __str__(self):
#         return self.name

class Converted_leads(models.Model):
    lead = models.ForeignKey('Leads', on_delete=models.CASCADE, null=True, blank=True)
    closed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    revenue_from_customer = models.IntegerField()
    product_bought = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.name} - Closed"


class Client(models.Model):
    converted_lead = models.OneToOneField(
        Converted_leads,
        on_delete=models.CASCADE,
        related_name="client"
    )

    closed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    billed_amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    def remaining_amount(self):
        return self.billed_amount - self.total_paid()

    def __str__(self):
        return f"{self.converted_lead.lead.name} - Client"


class Payment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - ₹{self.amount}"
# class Products(models.Model):
#     product_name = models.CharField(max_length=200)
#     selling_price = models.IntegerField()
#     inventory = models.IntegerField()   # ✅ FIXED
#     supplier = models.CharField(max_length=200)

#     def stock_value(self):
#         return self.inventory * self.selling_price

#     def __str__(self):
#         return self.product_name
    

class Lost_Leads (models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=50,default='New')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    reason_for_lossing = models.CharField()

    def __str__(self):
        return self.name
    

class LeadActivity(models.Model):
    ACTIVITY_TYPES = [

        ('created', 'Created'),
        ('contacted', 'First Contacted'),
        ('followup', 'Follow Up'),
        ('note', 'Note'),
        ('status_change', 'Status Change'),
        ('closed', 'Closed'),
    ]

    lead = models.ForeignKey('Leads', on_delete = models.CASCADE,related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)

    note = models.TextField(blank=True, null=True)
    activity_time = models.DateTimeField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['activity_time']  # timeline order

    def __str__(self):
        return f"{self.lead.name} - {self.activity_type}"



class Employee(models.Model):
    ROLE_CHOICES = [
        ('sales', 'Sales'),
        ('operations', 'Operations'),
        ('management', 'Management'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    joined_since = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    fathers_name = models.CharField(max_length=150, blank=True, null=True)
    aadhar_no = models.CharField(max_length=15, blank=True, null=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    account_no = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    uan_no = models.CharField(max_length=15, blank=True, null=True)

    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username



class FollowUp(models.Model):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='followups')
    followup_datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['followup_datetime']  # 🔥 important

    def __str__(self):
        return f"{self.lead.name} - {self.followup_datetime}"
    






# ledger and billing 

# class Client(models.Model):
#     converted_lead = models.OneToOneField(
#     Converted_leads,
#     on_delete=models.CASCADE,
#     null=True,
#     blank=True
# )
#     closed_by = models.ForeignKey(
        
#     User,
#     on_delete=models.CASCADE,
#     null=True,
#     blank=True
# )

#     billed_amount = models.IntegerField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def total_paid(self):
#         return sum(p.amount for p in self.payments.all())

#     def balance(self):
#         return self.billed_amount - self.total_paid()

#     def __str__(self):
#         return f"{self.converted_lead.lead.name}"




#     amount = models.IntegerField(default=0)
#     paid_on = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.client} - ₹{self.amount}"
    
    
    
# class Customer(models.Model):
#     name = 

# # gemini code for invoice generator 

# --- 2. Product Model (Updated) ---
class Products(models.Model):
    name = models.CharField(max_length=200)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    unit_price_incl_gst = models.DecimalField(default= 18,max_digits=10, decimal_places=2)
    gst_rate = models.DecimalField(default= 18 ,max_digits=5, decimal_places=2, help_text="GST percentage (e.g., 18.00)")
    
    # Keeping your inventory & supplier fields
    inventory = models.IntegerField(default=0)
    supplier = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

# --- 3. Invoice & Items System ---



class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # newely added 
    billed_amount = models.DecimalField(default= 18,max_digits=10, decimal_places=2),
    paid_amount = models.DecimalField(default= 0,max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_paid(self):
        # Calculates total payments related to this invoice
        paid = self.payments.aggregate(total=Sum('amount_paid'))['total']
        return paid if paid else 0

    @property
    def due_amount(self):
        return self.total_amount - self.total_paid

    @property
    def payment_status(self):
        if self.due_amount <= 0:
            return "Paid"
        elif self.total_paid > 0:
            return "Partial"
        return "Unpaid"

    def __str__(self):
        return f"INV {self.invoice_number} - {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Snapshot fields (IMMUTABLE for historical accuracy)
    product_name = models.CharField(max_length=200)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

# --- 4. Payment Ledger ---
# class Payment(models.Model):
#     PAYMENT_METHODS = (
#         ('cash', 'Cash'),
#         ('bank_transfer', 'Bank Transfer'),
#         ('upi', 'UPI'),
#         ('cheque', 'Cheque'),
#     )

#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
#     recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
#     amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_date = models.DateField()
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
#     reference_id = models.CharField(max_length=100, blank=True, null=True, help_text="Transaction ID or Cheque No.")
    
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.amount_paid} for {self.invoice.invoice_number}"





class activity_feed(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description


class SalaryRecord(models.Model):

    STATUS_CHOICES = [
        ('unpaid' , 'Unpaid'),
        ('paid', 'Paid'),
        ('pending' , 'Pending')
    ]

    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]



    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name  = 'salary_record'
    )

    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    year = models.IntegerField(default=2026)

    base_salary = models.DecimalField(max_digits = 10 , decimal_places=2)
    total_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='unpaid')
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank = True, null = True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-created_at']

    def save(self, *args, **kwargs):
        self.net_salary = self.base_salary + self.total_bonus - self.total_deductions

        if self.status == 'paid' and self.paid_at is None:
            self.paid_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.month} {self.year}"


class SalaryAdjustment(models.Model):
    ADJUSTMENT_CHOICES = [
        ('bonus', 'Bonus'),
        ('deduction', 'Deduction'),
    ]

    salary_record = models.ForeignKey(
        SalaryRecord,
        on_delete=models.CASCADE,
        related_name='adjustments'
    )

    adjustment_type = models.CharField(
        max_length=20,
        choices=ADJUSTMENT_CHOICES
    )

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type} - {self.title} - ₹{self.amount}"
    


class ConvertedLeadItem(models.Model):
    converted_lead = models.ForeignKey(
        Converted_leads,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    unit_price_incl_gst = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    hsn_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"