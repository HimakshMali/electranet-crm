from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crm.models import Leads,Employee, activity_feed


class RegisterForm(UserCreationForm):

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    # 🔥 NEW FIELDS
    project_name = forms.CharField(max_length=100, required=False)
    invitation_code = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'project_name',
            'invitation_code',
            'password1',
            'password2',
        ]

class EmployeeCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    base_salary = forms.DecimalField(max_digits=10, decimal_places=2)
    joined_since = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    role = forms.ChoiceField(choices=Employee.ROLE_CHOICES)

    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
class EmployeeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = ['base_salary', 'joined_since', 'role', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
class LeadForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = ['name', 'source', 'status', 'email', 'phone']



class InvoiceForm(forms.Form):
    # Customer Details
    customer_name = forms.CharField(max_length=200)
    customer_address = forms.CharField(widget=forms.Textarea)
    customer_phone = forms.CharField(max_length=15)
    customer_email = forms.EmailField()
    customer_gstin = forms.CharField(max_length=20, required=False)
    delivery_address = forms.CharField(widget=forms.Textarea, required=False)

    # Invoice Details
    invoice_number = forms.CharField(max_length=50)
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    vehicle = forms.CharField(max_length=100, required=False)

    # NOTE:
    # Product fields will NOT be defined here because they are multiple (dynamic)


class acticitefeedform(forms.ModelForm):
    class Meta:
        model = activity_feed
        fields = ["title", "description"]