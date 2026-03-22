from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['email', 'full_name', 'role', 'is_verified', 'is_active', 'date_joined']
    list_filter   = ['role', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'phone']
    ordering      = ['-date_joined']

    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal info',{'fields': ('full_name', 'phone', 'avatar')}),
        ('Role & status',{'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions',  {'fields': ('groups', 'user_permissions')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['date_joined', 'last_login']

    actions = ['verify_engineers', 'deactivate_users']

    def verify_engineers(self, request, queryset):
        updated = queryset.filter(role=User.Role.ENGINEER).update(is_verified=True)
        self.message_user(request, f'{updated} engineer(s) verified.')
    verify_engineers.short_description = 'Verify selected engineers'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'