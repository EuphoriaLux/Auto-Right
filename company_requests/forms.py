from django import forms
from .models import Category, CompanyRequest, AuthorizationScope  # Import AuthorizationScope

class CompanyRequestForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].choices = [
            (choice[0], choice[1])
            for choice in CompanyRequest.REQUEST_TYPES  # This is your choices field in your model
            if AuthorizationScope.objects.filter(request_type=choice[0]).exists()
        ]

    class Meta:
        model = CompanyRequest
        fields = ['content', 'request_type']
