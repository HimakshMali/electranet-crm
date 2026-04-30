from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [


    path('' ,views.home , name='home'),
    path('home/', views.home, name='home'),
     
    
    # path('sign-up/', views.sign_up, name='sign_up'),
    # path('create-post/', views.create_post, name='create_post'),
    # path('create-lead/', views.create_lead, name='create_lead'),

      # ✅ SIGNUP
    path('sign-up/', views.sign_up, name='sign-up'),

    # ✅ LOGIN (IMPORTANT)
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    # ✅ LOGOUT
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    path('add-employee/', views.add_employee, name='add_employee'),
    path('create-lead/', views.create_lead, name='create_lead'),
    path('employees_list/', views.employees_list , name = 'employees_list'),
    path('edit_employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employee_dashboard/<int:id>/', views.employee_dashboard, name='employee_dashboard'),
    # path('converted-leads/', views.converted_leads_list, name='converted_leads'),
    path("converted-leads/", views.converted_leads, name="converted-leads"),
    path('products/', views.products_page, name='products'),
    path('invoice/',  views.create_invoice , name = 'Invoice' ),
    # path('ledger/<int:customer_id>/', views.customer_ledger_view, name='ledger'),
    
    # Also ensure your list view is named correctly if you're linking to it
    path('ledger/', views.ledger_list_view, name='ledger'),
    path('add-followup/', views.add_followup, name='add_followup'),
    path('edit-followup/', views.edit_followup, name='edit_followup'),
    path('delete-followup/', views.delete_followup, name='delete_followup'),
    path('elements/', views.elementshtml, name ='elements'),
    path('lead/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('all-leads/', views.all_leads, name='all_leads'),

    path('clients/', views.clients, name='clients'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path("ledger-dashboard/", views.ledger_dashboard, name="ledger_dashboard"),
    path('create-post/', views.add_activity_feed_post, name='create_post'),
    path('employees/<int:employee_id>/salary/', views.employee_salary, name='employee_salary'),

    path("customer-invoice/<int:converted_lead_id>/",views.customer_invoice, name = 'customer_invoice'),


    path('lead-distribution/', views.lead_distribution, name='lead_distribution'),

    path("dashboard/", views.crm_dashboard, name="dashboard"),

]
