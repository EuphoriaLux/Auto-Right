from django.shortcuts import render, redirect
from .models import Company, CompanyRequest, CompanyGroup, Category, Risk, AuthorizationScope, UserAuthorization
from user_management.models import CustomUser
from django.db.models import Count, Prefetch
from .forms import CompanyRequestForm
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.template.loader import select_template
from django.http import HttpResponseBadRequest
from django.contrib import messages 

def create_company_request(request):
    disabled_categories = []
    if request.method == 'POST':
        post_data = request.POST.copy()
        categories_str = post_data.get('categories', '')
        if categories_str:
            categories_list = list(map(int, categories_str.split(',')))
            post_data.setlist('categories', categories_list)
        
        form = CompanyRequestForm(post_data)

        if form.is_valid():
            print("Form is valid.")

            selected_scopes = request.POST.getlist('selected_scopes')
            
            print(f"Selected scopes: {selected_scopes}")  # Debug line 1
            
            for scope_id in selected_scopes:
                if scope_id:
                    try:
                        int_scope_id = int(scope_id)
                    except ValueError:
                        print(f"Invalid scope ID: {scope_id}")
                        continue

                    print(f"Processing scope ID: {int_scope_id}")  # Debug line 2
                    
                    try:
                        scope = AuthorizationScope.objects.get(id=int_scope_id)
                        
                        user_auth, created = UserAuthorization.objects.get_or_create(
                            user=request.user,
                            scope=scope
                        )
                        print(f"UserAuthorization for scope {scope_id}. Created: {created}")  # Debug line 4

                    except AuthorizationScope.DoesNotExist:
                        print(f"Exception when creating UserAuthorization: Invalid scope ID {scope_id}")
                    except Exception as e:  # Debug line 5
                        print(f"Unexpected error when processing scope ID {int_scope_id}: {str(e)}")

            # Create a CompanyRequest for each company in the selected categories
            selected_categories = form.cleaned_data.get('categories')
            for category in selected_categories:
                for group in category.company_groups.all():
                    for company in group.companies.all():
                        CompanyRequest.objects.create(
                            user=request.user,
                            company=company,
                            content=post_data.get('content', ''),  # Remove or comment out this line
                            request_type=post_data.get('request_type', 'data_suppression')
                        )

            messages.success(request, "Company request(s) created successfully.")
            return redirect('summary_by_category')
        else:
            print("Form is invalid.")
            messages.error(request, "Form is invalid. Please check the fields.")
            print(form.errors)

       
    # Find categories that have existing CompanyRequest and disable them
    existing_requests = CompanyRequest.objects.filter(user=request.user).values_list('company__groups__category', flat=True)
    for category_id in existing_requests:
        disabled_categories.append(category_id)

    form = CompanyRequestForm()
    return render(request, 'company_requests/request_companies_by_category.html', {'form': form, 'disabled_categories': disabled_categories})

def companies_by_category(request):
    categories = Category.objects.all().prefetch_related('company_groups__companies')
    
    context = {
        'categories': categories
    }
    return render(request, 'company_requests/companies_by_category.html', context)

#Main List View User
def summary_by_category(request):
    company_requests = CompanyRequest.objects.filter(user=request.user)
    
    categories = Category.objects.annotate(
        company_count=Count('company_groups__companies', distinct=True),
        request_count=Count('company_groups__companies__companyrequest', distinct=True)
    ).prefetch_related(
        Prefetch('company_groups__companies__companyrequest_set', queryset=company_requests, to_attr='user_requests'),
        'company_groups__companies',
        'risk'  
    )
    
    for category in categories:
        for group in category.company_groups.all():
            for company in group.companies.all():
                company.latest_request_status = company.get_last_request_status(request.user)
               

    user_details = CustomUser.objects.filter(email=request.user.email).first()
    context = {
        'categories': categories,
        'user_details': user_details,
    }
    return render(request, 'company_requests/summary_by_category.html', context)

# Updated Function
def get_authorization_scope(category_id, request_type):
    try:
        authorization_scopes = AuthorizationScope.objects.filter(
            category_id=category_id, 
            request_type=request_type
        )
        if authorization_scopes.exists():
            return authorization_scopes.first().name
        else:
            print("No authorization scope found for this category and request type.")
            return None
    except Exception as e:
        print(f"Exception in get_authorization_scope: {type(e).__name__}, {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# views.py
def get_authorization_form(request):

    try:
        category_ids_str = request.GET.get('category_ids', None)
        request_type = request.GET.get('request_type', None)
        
        if not category_ids_str:
            return HttpResponseBadRequest('Invalid category_ids')

        # Handle empty request_type
        if not request_type:
            # Set request_type to the first available type for the given category
            # If no type is available, return a suitable message or HTTP response.
            available_types = AuthorizationScope.objects.filter(
                category_id__in=category_ids_str.split(',')).values_list('request_type', flat=True).distinct()
            if available_types:
                request_type = available_types[0]
            else:
                return HttpResponseBadRequest('No request type available for the given category')

        authorization_scopes = AuthorizationScope.objects.filter(
            category_id__in=category_ids_str.split(','),
            request_type=request_type
        )
        if not authorization_scopes.exists():
            return HttpResponseBadRequest('Invalid authorization scope')


        # Get the user details
        user_details = CustomUser.objects.filter(email=request.user.email).first()

        form_html = render_to_string(
            'company_requests/authorization_form.html',
            {'scopes': authorization_scopes, 'user_details': user_details}  # Pass user_details to the template
        )
        return HttpResponse(form_html)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def create_company_request2(request):
    disabled_categories = []
    if request.method == 'POST':
        post_data = request.POST.copy()
        categories_str = post_data.get('categories', '')
        if categories_str:
            categories_list = list(map(int, categories_str.split(',')))
            post_data.setlist('categories', categories_list)
        
        form = CompanyRequestForm(post_data)

        if form.is_valid():
            print("Form is valid.")

            selected_scopes = request.POST.getlist('selected_scopes')
            
            print(f"Selected scopes: {selected_scopes}")  # Debug line 1
            
            for scope_id in selected_scopes:
                if scope_id:
                    try:
                        int_scope_id = int(scope_id)
                    except ValueError:
                        print(f"Invalid scope ID: {scope_id}")
                        continue

                    print(f"Processing scope ID: {int_scope_id}")  # Debug line 2
                    
                    try:
                        scope = AuthorizationScope.objects.get(id=int_scope_id)
                        
                        user_auth, created = UserAuthorization.objects.get_or_create(
                            user=request.user,
                            scope=scope
                        )
                        print(f"UserAuthorization for scope {scope_id}. Created: {created}")  # Debug line 4

                    except AuthorizationScope.DoesNotExist:
                        print(f"Exception when creating UserAuthorization: Invalid scope ID {scope_id}")
                    except Exception as e:  # Debug line 5
                        print(f"Unexpected error when processing scope ID {int_scope_id}: {str(e)}")

            # Create a CompanyRequest for each company in the selected categories
            selected_categories = form.cleaned_data.get('categories')
            for category in selected_categories:
                for group in category.company_groups.all():
                    for company in group.companies.all():
                        CompanyRequest.objects.create(
                            user=request.user,
                            company=company,
                            content=post_data.get('content', ''),  # Remove or comment out this line
                            request_type=post_data.get('request_type', 'data_suppression')
                        )

            messages.success(request, "Company request(s) created successfully.")
            return redirect('summary_by_category')
        else:
            print("Form is invalid.")
            messages.error(request, "Form is invalid. Please check the fields.")
            print(form.errors)

       
    # Find categories that have existing CompanyRequest and disable them
    existing_requests = CompanyRequest.objects.filter(user=request.user).values_list('company__groups__category', flat=True)
    for category_id in existing_requests:
        disabled_categories.append(category_id)

    form = CompanyRequestForm()
    return render(request, 'company_requests/request_2.html', {'form': form, 'disabled_categories': disabled_categories})
