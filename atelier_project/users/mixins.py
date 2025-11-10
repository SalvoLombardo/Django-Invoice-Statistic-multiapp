from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class AdminRequiredMixin:
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'client_profile') or user.client_profile.role != 'ADMIN':
            messages.error(request, "Accesso riservato agli amministratori.")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)