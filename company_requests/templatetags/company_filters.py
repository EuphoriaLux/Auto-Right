from django import template
from company_requests.models import Company

register = template.Library()

@register.filter
def status_to_bootstrap_class(status):
    return {
        'pending': 'bg-warning',
        'approved': 'bg-success',
        'rejected': 'bg-danger',
        'in_progress': 'bg-info',
        'completed': 'bg-primary'
    }.get(status, 'bg-secondary')
