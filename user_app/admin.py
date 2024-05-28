from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import CustomUser,Customers
CustomUser = get_user_model()
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_admin', 'is_staff', 'is_superuser', 'permissions'),
        }),
    )
    list_display = ('email', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

class CustomersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customers._meta.fields]
# admin.site.register(CustomUser, UserAdmin)
admin.site.register(Permission)
admin.site.register(Customers, CustomersAdmin)

