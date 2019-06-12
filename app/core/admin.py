from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Contact Info'),
            {
                'fields': (
                    'facebook',
                    'instagram',
                    'phone',
                    'soundcloud',
                    'spotify',
                    'twitter',
                    'website',
                    'youtube',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Artist)
admin.site.register(models.Promoter)
admin.site.register(models.Venue)
admin.site.register(models.Event)
