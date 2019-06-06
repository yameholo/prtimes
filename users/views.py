from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from config import settings

from .forms import LoginForm, MyUserCreationForm, MyUserUpdateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .tokens import account_activation_token

User = get_user_model()


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('box:home')


class MyLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'users:login'

    def get_next_page(self):
        next_page = super().get_next_page()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'ログアウトしました。',
        )
        return next_page


class MyUserCreateView(CreateView):
    template_name = 'users/signup.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'user': user,
            'user_id': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        }

        subject_template = get_template('users/mail/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('users/mail/create/message.txt')
        message = message_template.render(context)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        return redirect('users:signup_done')


class MySignupDoneView(TemplateView):
    template_name = 'users/signup_done.html'


def activate(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('users:login'))
    else:
        return HttpResponse('Activation link is invalid!')


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.id == self.kwargs['pk'] or user.is_superuser


class MyUserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    form_class = MyUserUpdateForm
    template_name = 'users/update.html'

    # def get_success_url(self):
    #     return reverse('sg:suggestions', args=(self.request.user.id,))


class MyPasswordChangeView(PasswordChangeView):

    form_class = MyPasswordChangeForm
    template_name = 'users/password_change.html'

    # def get_success_url(self):
    #     return reverse('sg:suggestions', args=(self.request.user.id,))


class MyUserDeleteView(OnlyYouMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy('users:login')


class MyPasswordResetView(PasswordResetView):

    subject_template_name = 'users/mail/password_reset/subject.txt'
    email_template_name = 'users/mail/password_reset/message.txt'
    template_name = 'users/password_reset.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:login')
    template_name = 'users/password_reset_confirm.html'
    form_class = MySetPasswordForm
