from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models
from core.email import Email


def verify(modeladmin, request, queryset):
    """Mark promoters as 'verified'."""
    queryset.update(is_verified=True)
    email_addresses = list(queryset.values_list('email', flat=True))
    Email('verified_promoter', email_addresses).send()

verify.short_description = "Mark promoters as 'verified'"


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'name', 'slug', 'credit']
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_artist', 'is_promoter',
        'is_temporary'
    ]
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Account Info'), {'fields': ('name', 'slug', 'credit', 'stripe_account_id', 'stripe_customer_id')}),
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
                    'is_artist',
                    'is_promoter',
                    'is_temporary',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Image'), {'fields': ('image',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)
        }),
    )


class ArtistAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = [
        'id', 'name', 'email', 'total_events', 'total_points', 'slug', 'credit'
    ]

    def total_events(self, obj):
        return obj.total_events()

    def total_points(self, obj):
        return obj.total_points()


class PromoterAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'email', 'is_verified', 'slug', 'credit']
    actions = [verify]


class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_date', 'created_time', 'sender', 'subject']


class ReadFlagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'message', 'opened', 'recipient']


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'name', 'start_date', 'start_time',
        'end_date', 'end_time', 'venue', 'promoter'
    ]


class TallyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'slug', 'artist', 'event']


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'slug', 'event', 'name', 'price', 'tickets_remaining'
    ]


class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'code', 'created_date', 'created_time', 'owner', 'ticket_type',
        'vote'
    ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Promoter, PromoterAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.ReadFlag, ReadFlagAdmin)
admin.site.register(models.Venue)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Tally, TallyAdmin)
admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.TicketType, TicketTypeAdmin)
