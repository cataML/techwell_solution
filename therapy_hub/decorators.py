from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required

def login_for(service_login_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return login_required(view_func, login_url=service_login_url)(request, *args, **kwargs)
        return _wrapped_view
    return decorator