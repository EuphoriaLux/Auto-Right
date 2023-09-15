from django.urls import path, re_path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),       # Login page
    path('logout/', views.logout_view, name='logout'),    # Logout action
    path('profile/', views.profile, name='profile'),      # User profile page
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Edit profile page
    path('onboarding_step1/', views.onboarding_step1, name='onboarding_step1'),
    path('onboarding_step2/', views.onboarding_step2, name='onboarding_step2'),
    path('onboarding_step3/', views.onboarding_step3, name='onboarding_step3'),
    path('send_email/', views.send_email_view, name='send_email'),

]
