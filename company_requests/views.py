from django.shortcuts import render, redirect
from .models import Company, CompanyRequest, CompanyGroup, Category, Risk, AuthorizationScope, UserAuthorization
from user_management.models import CustomUser
from django.db.models import Count
from .forms import CompanyRequestForm
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.template.loader import select_template



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

#Main Request View User
def create_company_request(request):


    if request.method == 'POST':
        form = CompanyRequestForm(request.POST)
        
        if form.is_valid():
            try:
                # ... (existing logic to save CompanyRequest)
                
                # Logic to save UserAuthorization
                selected_scopes = request.POST.getlist('scopes')  # The selected AuthorizationScope ids
                
                for scope_id in selected_scopes:
                    scope = AuthorizationScope.objects.get(id=scope_id)
                    UserAuthorization.objects.create(
                        user=request.user,
                        scope=scope
                    )

                return redirect('profile')  # Redirect to the profile page

            except ValidationError:
                print("Invalid category IDs or scope IDs")
        
    else:
        form = CompanyRequestForm()

    return render(request, 'company_requests/request_companies_by_category.html', {'form': form})

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


from django.http import HttpResponseBadRequest


# views.py

def get_authorization_form(request):
    try:
        category_ids_str = request.GET.get('category_ids', None)
        request_type = request.GET.get('request_type', None)
        
        if not category_ids_str or not request_type:
            return HttpResponseBadRequest('Invalid category_ids or request_type')

        category_ids = list(map(int, category_ids_str.split(',')))

        authorization_scopes = AuthorizationScope.objects.filter(
            category_id__in=category_ids,
            request_type=request_type
        )
        if not authorization_scopes.exists():
            return HttpResponseBadRequest('Invalid authorization scope')

        form_html = render_to_string(
            'company_requests/authorization_form.html',
            {'scopes': authorization_scopes}
        )
        return HttpResponse(form_html)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
