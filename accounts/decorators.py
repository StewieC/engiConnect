from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Restrict a view to users whose role is in the given list.
    Usage:
        @role_required(User.Role.CLIENT)
        @role_required(User.Role.ADMIN, User.Role.IN_HOUSE)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access that page.')
                return redirect(request.user.get_dashboard_url())
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def engineer_verified_required(view_func):
    """
    Extra guard: engineer must be verified before accessing certain views.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_verified:
            messages.warning(request, 'Your engineer account is pending verification.')
            return redirect('accounts:engineer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper