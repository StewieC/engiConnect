from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),           # Tasks as main homepage
    path('accounts/', include('accounts.urls')),
]