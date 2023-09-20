from django import forms
from .models import Category, CompanyRequest, AuthorizationScope
from django.core.exceptions import ValidationError

class CompanyRequestForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Handling request types
        available_request_types = [
            (choice[0], choice[1])
            for choice in CompanyRequest.REQUEST_TYPES  # This is your choices field in your model
            if AuthorizationScope.objects.filter(request_type=choice[0]).exists()
        ]

        self.fields['request_type'].choices = available_request_types

        # Setting initial to the first available request type
        if available_request_types:
            self.fields['request_type'].initial = available_request_types[0][0]

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise ValidationError("No categories selected.")
        
        return categories  # Return the list of category objects

    class Meta:
        model = CompanyRequest
        fields = ['request_type']  # Removed 'content' from here
