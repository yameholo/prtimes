from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import User


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'email', 'screen_name')}),
        (_('権限'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                              'groups', 'user_permissions')}),
        (_('メタ情報'), {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'screen_name', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'last_login', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('-created_at',)


admin.site.register(User, MyUserAdmin)
