import time
from django.conf import settings

def cache_buster(request):
    """
    Context processor para adicionar timestamp em desenvolvimento
    """
    return {
        'current_timestamp': int(time.time()) if settings.DEBUG else '',
        'is_development': settings.DEBUG,
    }