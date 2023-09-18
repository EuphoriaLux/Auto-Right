from django.contrib import admin
from .models import AuthorizationScope, Category, CompanyGroup, Company, CompanyRequest, Risk, CategoryRisk, UserAuthorization

# Inline for CategoryRisk -> Risk
class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1

# Inline for Category -> CompanyGroup
class CompanyGroupInline(admin.TabularInline):
    model = CompanyGroup
    extra = 1

# Inline for CompanyGroup -> Company
class CompanyInline(admin.TabularInline):
    model = Company.groups.through
    extra = 1

# AuthorizationScope Admin
class AuthorizationScopeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'request_type', 'category']
    search_fields = ['name', 'description']
    list_filter = ['request_type', 'category']

# UserAuthorization Admin
class UserAuthorizationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scope']
    search_fields = ['user__email', 'scope__name']
    list_filter = ['user', 'scope']

# Risk Admin
class RiskAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category']
    search_fields = ['name', 'description']
    list_filter = ['category']

# CategoryRisk Admin
class CategoryRiskAdmin(admin.ModelAdmin):
    inlines = [RiskInline]
    list_display = ['name', 'description', 'icon_color']
    search_fields = ['name', 'description']
    list_filter = ['name']

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CompanyGroupInline]
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']
    filter_horizontal = ('risk',)

# CompanyGroup Admin
class CompanyGroupAdmin(admin.ModelAdmin):
    inlines = [CompanyInline]
    list_display = ['name', 'description', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['category', 'created_at', 'updated_at']

# Company Admin
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['legal_name', 'commercial_name', 'address', 'company_number', 'email', 'created_at', 'updated_at']
    search_fields = ['legal_name', 'commercial_name', 'email']
    list_filter = ['created_at', 'updated_at']

# CompanyRequest Admin
class CompanyRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'request_date', 'request_type', 'status', 'created_at', 'updated_at']
    search_fields = ['user__email', 'company__legal_name', 'request_type']
    list_filter = ['request_date', 'company', 'status', 'request_type']
    list_editable = ['status']

admin.site.register(Risk, RiskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CompanyGroup, CompanyGroupAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyRequest, CompanyRequestAdmin)
admin.site.register(CategoryRisk, CategoryRiskAdmin)
admin.site.register(AuthorizationScope, AuthorizationScopeAdmin)
admin.site.register(UserAuthorization, UserAuthorizationAdmin)
