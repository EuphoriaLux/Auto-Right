from django.db import models
from user_management.models import CustomUser  
from django.db import models

class Risk(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('CategoryRisk', null=True, blank=True, related_name='risks', on_delete=models.SET_NULL)

    # In your Risk model
    def get_icon_color(self):
        if self.category:
            return self.category.icon_color
        return "#000000"  # Default color if no category is associated

    def __str__(self):
        return self.name

class CategoryRisk(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    icon_color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name

#Company Category =>>> to change into CompanyCategory later on...
class Category(models.Model):
    name = models.CharField(max_length=200)
    risk = models.ManyToManyField(Risk, blank=True, related_name='related_categories')
    description = models.TextField(blank=True, null=True)

    def get_average_compliance_score(self):
        total_score = 0
        total_companies = 0
        for group in self.company_groups.all():
            for company in group.companies.all():
                total_score += company.get_compliance_score()
                total_companies += 1
        return total_score / total_companies if total_companies else 0

    def get_related_risks(self):
        return self.risk.all()

    def get_overall_severity(self):
        return "Medium"

    def get_total_requests_sent(self):
        total_requests = 0
        for group in self.company_groups.all():
            for company in group.companies.all():
                total_requests += company.get_total_requests_count()
        return total_requests

    def get_company_count(self):
        company_count = 0
        for group in self.company_groups.all():
            company_count += group.companies.count()
        return company_count

    def get_last_request_status(self, customUser):
        last_company = self.company_groups.last().companies.last() if self.company_groups.exists() else None
        return last_company.get_last_request_status(customUser) if last_company else "No Request Sent"

    def get_related_scopes(self):
        return self.authorization_scopes.all()
        
    def get_risks_grouped_by_category(self):
        # Get unique CategoryRisk IDs associated with the risks
        category_risk_ids = Risk.objects.filter(related_categories=self).values_list('category', flat=True).distinct()
        
        # Fetch the CategoryRisk objects
        return CategoryRisk.objects.filter(id__in=category_risk_ids)

    def __str__(self):
        return self.name



class CompanyGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="company_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    legal_name = models.CharField(max_length=200, unique=True)
    commercial_name = models.CharField(max_length=200)
    address = models.TextField()
    company_number = models.CharField(max_length=50, unique=True)  # Added uniqueness constraint
    email = models.EmailField(unique=False)  # Removed uniqueness constraint
    groups = models.ManyToManyField(CompanyGroup, blank=True, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_compliance_score(self):
        # Placeholder logic: replace with actual logic to compute the compliance score for this company
        return 85  # 
    
    def get_severity(self):
        # Implement your logic here to determine the severity level for this company.
        # For instance, you can use the compliance score to determine the severity.
        compliance_score = self.get_compliance_score()
        if compliance_score >= 90:
            return "Low"
        elif compliance_score >= 70:
            return "Medium"
        else:
            return "High"

    def get_last_request_status(self, customerUser):
        """Return the status of the latest request made by the user to the company."""
        try:
            request = self.companyrequest_set.filter(user=customerUser).latest('request_date')
            return request.status
        except CompanyRequest.DoesNotExist:
            return 'No Request Sent'

    def get_total_requests_count(self):
        """Return the total number of requests made to the company."""
        return self.companyrequest_set.count()

    def __str__(self):
        return self.legal_name

class CompanyRequest(models.Model):
    REQUEST_STATUS = (
        ('unsubmitted', 'Unsubmitted'),  
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )

    REQUEST_TYPES = (
        ('data_suppression', 'Data Suppression'),
        ('data_retrieval', 'Data Retrieval'),
        ('data_modification', 'Data Modification'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='unsubmitted', db_index=True)  
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES, default='data_suppression', verbose_name="Type of Request")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_request_type_display()} for {self.company.legal_name} by {self.user.email}"

class AuthorizationScope(models.Model):
    REQUEST_TYPES = (
        ('data_suppression', 'Data Suppression'),
        ('data_retrieval', 'Data Retrieval'),
        ('data_modification', 'Data Modification'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES, verbose_name="Type of Request")  # New field
    category = models.ForeignKey('Category', null=True, blank=True, related_name='authorization_scopes', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
class UserAuthorization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scope = models.ForeignKey(AuthorizationScope, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'scope')
