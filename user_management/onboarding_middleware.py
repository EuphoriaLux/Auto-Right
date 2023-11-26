from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import resolve

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the URL name without the language prefix
        url_name = resolve(request.path_info).url_name

        # Skip middleware for onboarding URLs
        if url_name not in ['onboarding_step1', 'onboarding_step2', 'onboarding_step3']:
            # Only proceed if user is authenticated
            if request.user.is_authenticated:
                # Redirect user to appropriate onboarding step
                if not request.user.has_completed_step1:
                    print(_("Redirecting to step 1")) 
                    return redirect('onboarding_step1')
                elif not request.user.has_completed_step2:
                    print(_("Redirecting to step 2")) 
                    return redirect('onboarding_step2')
                elif not request.user.has_completed_step3:
                    print(_("Redirecting to step 3")) 
                    return redirect('onboarding_step3')

        # Proceed to next middleware or view
        response = self.get_response(request)
        return response
