from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Devi effettuare l'accesso.")
            return redirect('login_client')
        if not hasattr(user, 'client_profile') or user.client_profile.role != 'ADMIN':
            messages.error(request, "Accesso riservato agli amministratori.")
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return _wrapped_view