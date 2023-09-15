from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'core/homepage.html')

@login_required
def dashboard(request):
    return render(request, 'user_dashboard.html')
