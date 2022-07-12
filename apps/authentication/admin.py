from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal Info'), {
         'fields': ('first_name', 'last_name', 'phone', 'image', 'otp')}),
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
        (_('Dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(User, UserAdmin)


# admin.site.unregister(Group)
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     ordering = ('name',)
#     filter_horizontal = ('permissions',)

#     def formfield_for_manytomany(self, db_field, request=None, **kwargs):
#         if db_field.name == 'permissions':
#             qs = kwargs.get('queryset', db_field.remote_field.model.objects)
#             # Avoid a major performance hit resolving permission names which
#             # triggers a content_type load:
#             kwargs['queryset'] = qs.select_related('content_type')
#         return super().formfield_for_manytomany(db_field, request=request, **kwargs)
