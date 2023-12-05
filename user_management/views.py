from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utils import send_test_email  # Assuming the send_test_email is in utils.py
from .forms import *
from company_requests.models import CompanyRequest
from django.utils.translation import gettext as _


# Registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to the profile page if user is already authenticated
    
    if request.method == "POST":
        print("POST request received")  # Debugging print statement
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging print statement
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            print("Form is not valid")  # Debugging print statement
            print(form.errors)  # Print form errors
    else:
        form = RegistrationForm()
    return render(request, 'user_management/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            # Invalid login
            pass  # Handle invalid login here
    return render(request, 'user_management/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    total_requests = CompanyRequest.objects.filter(user=request.user).count()
    pending_requests = CompanyRequest.objects.filter(user=request.user, status='pending').count()
    completed_requests = CompanyRequest.objects.filter(user=request.user, status='completed').count()
    rejected_requests = CompanyRequest.objects.filter(user=request.user, status='rejected').count()

    context = {
        'user': request.user,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'completed_requests': completed_requests,
        'rejected_requests': rejected_requests
    }

    return render(request, 'user_management/profile.html', context)

# Edit profile view
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'user_management/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    edit_form = None
    if request.method == "POST":
        edit_form = EditProfileForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile')
    else:
        edit_form = EditProfileForm(instance=request.user)

    return render(request, 'user_management/profile.html', {'edit_form': edit_form})

# views.py
def onboarding_step1(request):
    if request.method == 'POST':
        form = OnboardingStep1Form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.has_completed_step1 = True
            request.user.save()
            return redirect('onboarding_step2')
    else:
        form = OnboardingStep1Form(instance=request.user)
    
    return render(request, 'user_management/onboarding_step1.html', {'form': form})

def onboarding_step2(request):
    if request.method == 'POST':
        form = OnboardingStep2Form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.has_completed_step2 = True
            request.user.save()
            return redirect('onboarding_step3')
    else:
        form = OnboardingStep2Form(instance=request.user)
        
    return render(request, 'user_management/onboarding_step2.html', {'message': _('Welcome to step 2!')})

def onboarding_step3(request):
    if request.method == 'POST':
        form = OnboardingStep3Form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.has_completed_step3 = True
            request.user.save()
            return redirect('profile')
    else:
        form = OnboardingStep3Form(instance=request.user)
        
    return render(request, 'user_management/onboarding_step3.html')

def send_email_view(request):
    send_test_email()
    return HttpResponse('Email sent!')