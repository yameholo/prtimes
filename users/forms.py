from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import User


class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].widget.attrs.pop('autofocus', None)
        # self.fields['screen_name'].widget.attrs.update({'autofocus': True})
        # self.fields['name'].widget.attrs.update({'autofocus': True})
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'

    error_messages = {
        'password_mismatch': _("パスワードが一致していません"),
    }

    password1 = forms.CharField(
        label=_("パスワード"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("パスワード(確認用)"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("同じパスワードを入力してください。"),
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'screen_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    password = forms.CharField(
        label=_("パスワード"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'screen_name', 'password')


class MyUserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'screen_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'


class MyPasswordChangeForm(PasswordChangeForm):

    error_messages = {
        'password_mismatch': _("パスワードが一致しません。"),
        'password_incorrect': _("現在のパスワードが違います。正しいパスワードを入力してください。"),
    }
    new_password1 = forms.CharField(
        label=_("新しいパスワード"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("新しいパスワード(確認用)"),
        strip=False,
        widget=forms.PasswordInput,
    )
    old_password = forms.CharField(
        label=_("現在のパスワード"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'


class MyPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'


class MySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form__input'
