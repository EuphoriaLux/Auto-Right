from django.shortcuts import redirect

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip middleware for onboarding URLs
        if request.path not in ['/users/onboarding_step1/', '/users/onboarding_step2/', '/users/onboarding_step3/']:
            
            # Only proceed if user is authenticated
            if request.user.is_authenticated:

                # Redirect user to appropriate onboarding step
                if not request.user.has_completed_step1:
                    print("Redirecting to step 1") 
                    return redirect('onboarding_step1')
                elif not request.user.has_completed_step2:
                    print("Redirecting to step 2") 
                    return redirect('onboarding_step2')
                elif not request.user.has_completed_step3:
                    print("Redirecting to step 3") 
                    return redirect('onboarding_step3')

        # Proceed to next middleware or view
        response = self.get_response(request)
        return response
