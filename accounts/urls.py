from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('login/',    views.LoginView.as_view(),    name='login'),
    path('logout/',   views.LogoutView.as_view(),   name='logout'),

    # Registration
    path('register/',          views.RegisterChoiceView.as_view(),  name='register'),
    path('register/client/',   views.ClientRegisterView.as_view(),  name='register_client'),
    path('register/engineer/', views.EngineerRegisterView.as_view(),name='register_engineer'),

    # Dashboard router
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    # Role dashboards
    path('dashboard/client/',   views.client_dashboard,   name='client_dashboard'),
    path('dashboard/engineer/', views.engineer_dashboard, name='engineer_dashboard'),
    path('dashboard/inhouse/',  views.inhouse_dashboard,  name='inhouse_dashboard'),
    path('dashboard/admin/',    views.admin_dashboard,    name='admin_dashboard'),

    # Profile
    path('profile/', views.profile, name='profile'),
]