# admin.py
from django.contrib import admin
from .models import AuthorizationScope, Category, CompanyGroup, Company, CompanyRequest, Risk, CategoryRisk

class AuthorizationScopeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category']
    search_fields = ['name', 'description']
    list_filter = ['category']


# UserAuthorization Admin
class UserAuthorizationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scope']
    search_fields = ['user__email', 'scope__name']
    list_filter = ['user', 'scope']


class RiskAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category', 'description']  # Added 'get_category'
    search_fields = ['name', 'description']
    
    def get_category(self, obj):
        return obj.category.name if obj.category else "N/A"
    get_category.short_description = 'Category'


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    filter_horizontal = ('risk',) 

# CompanyGroup Admin
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['category']

# Company Admin
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['legal_name', 'commercial_name', 'address', 'company_number', 'email', 'created_at', 'updated_at']
    search_fields = ['legal_name', 'commercial_name', 'email']

# CompanyRequest Admin
class CompanyRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'request_date', 'request_type', 'status', 'created_at', 'updated_at']
    search_fields = ['user__email', 'company__legal_name', 'request_type']
    list_filter = ['request_date', 'company', 'status', 'request_type']
    list_editable = ['status']


class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1

class CategoryRiskAdmin(admin.ModelAdmin):
    inlines = [RiskInline]
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']

# Registering models with their respective admin classes
admin.site.register(Risk, RiskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CompanyGroup, CompanyGroupAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyRequest, CompanyRequestAdmin)
admin.site.register(CategoryRisk, CategoryRiskAdmin)
admin.site.register(AuthorizationScope, AuthorizationScopeAdmin)  # Registering AuthorizationScope
