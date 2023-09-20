from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.summary_by_category, name='summary_by_category'),
    path('create_company_request/', views.create_company_request, name='create_company_request'),
    path('companies-by-category/', views.companies_by_category, name='companies_by_category'),  # New URL pattern
    path('get_authorization_form/', views.get_authorization_form, name='get_authorization_form'),
]
