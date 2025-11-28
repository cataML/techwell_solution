from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            role = None
        
            if hasattr(request.user, 'digital_profile'):
                role = request.user.digital_profile.role
        
            elif hasattr(request.user, 'profile'):
                role = request.user.profile.role

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('no_permission')
        return _wrapped
    return decorator

def login_for(service_login_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return login_required(view_func, login_url=service_login_url)(request, *args, **kwargs)
        return _wrapped_view
    return decorator