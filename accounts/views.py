from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View

from .forms import LoginForm, ClientRegisterForm, EngineerRegisterForm, ProfileUpdateForm
from .models import User
from .decorators import role_required


# ── Auth views ──────────────────────────────────────────────────────────────

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(request.user.get_dashboard_url())
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name.split()[0]}!')
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else user.get_dashboard_url())
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('accounts:login')


class RegisterChoiceView(View):
    """Landing page to pick: register as client or as engineer."""
    template_name = 'accounts/register_choice.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(request.user.get_dashboard_url())
        return render(request, self.template_name)


class ClientRegisterView(View):
    template_name = 'accounts/register_client.html'

    def get(self, request):
        form = ClientRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to EngiConnect, {user.full_name.split()[0]}! Your client account is ready.')
            return redirect('accounts:client_dashboard')
        return render(request, self.template_name, {'form': form})


class EngineerRegisterView(View):
    template_name = 'accounts/register_engineer.html'

    def get(self, request):
        form = EngineerRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EngineerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.info(
                request,
                'Account created! Your engineer profile is pending verification. '
                'You will be notified once approved.'
            )
            return redirect('accounts:engineer_dashboard')
        return render(request, self.template_name, {'form': form})


# ── Dashboard redirect ───────────────────────────────────────────────────────

@login_required
def dashboard_redirect(request):
    return redirect(request.user.get_dashboard_url())


# ── Role dashboards (placeholders — filled in by future apps) ────────────────

@login_required
@role_required(User.Role.CLIENT)
def client_dashboard(request):
    context = {
        'page_title': 'Client Dashboard',
        'stats': [
            {'label': 'Active projects',  'value': 0, 'icon': 'folder'},
            {'label': 'Pending quotes',   'value': 0, 'icon': 'file-text'},
            {'label': 'Completed jobs',   'value': 0, 'icon': 'check-circle'},
        ]
    }
    return render(request, 'accounts/dashboard_client.html', context)


@login_required
@role_required(User.Role.ENGINEER)
def engineer_dashboard(request):
    context = {
        'page_title': 'Engineer Dashboard',
        'is_verified': request.user.is_verified,
        'stats': [
            {'label': 'Open contracts',   'value': 0, 'icon': 'briefcase'},
            {'label': 'In progress',      'value': 0, 'icon': 'activity'},
            {'label': 'Completed',        'value': 0, 'icon': 'check-circle'},
        ]
    }
    return render(request, 'accounts/dashboard_engineer.html', context)


@login_required
@role_required(User.Role.IN_HOUSE)
def inhouse_dashboard(request):
    context = {
        'page_title': 'Team Dashboard',
        'stats': [
            {'label': 'Assigned jobs',    'value': 0, 'icon': 'clipboard'},
            {'label': 'In progress',      'value': 0, 'icon': 'activity'},
            {'label': 'Completed',        'value': 0, 'icon': 'check-circle'},
        ]
    }
    return render(request, 'accounts/dashboard_inhouse.html', context)


@login_required
@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    total_users     = User.objects.count()
    pending_engineers = User.objects.filter(role=User.Role.ENGINEER, is_verified=False).count()
    context = {
        'page_title': 'Admin Dashboard',
        'stats': [
            {'label': 'Total users',          'value': total_users,         'icon': 'users'},
            {'label': 'Pending verifications','value': pending_engineers,   'icon': 'shield'},
            {'label': 'Active jobs',          'value': 0,                   'icon': 'briefcase'},
        ]
    }
    return render(request, 'accounts/dashboard_admin.html', context)



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})