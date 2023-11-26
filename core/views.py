from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login  # Required for logging the user in after registration

# Assuming you have a RegistrationForm in your forms.py
from user_management.forms import RegistrationForm  

def index(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to the profile page if user is already authenticated

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Adjust this redirect as needed
    else:
        form = RegistrationForm()

    return render(request, 'core/index.html', {'form': form})
