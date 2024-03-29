from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, reverse_lazy, PasswordResetConfirmView
from django.contrib.auth import login
from .forms import UserRegisterForm, UserForgotPasswordForm, UserSetNewPasswordForm
from django.views.generic import UpdateView, CreateView, TemplateView
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
import secrets
import string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.requests import RequestSite
from django.template.loader import render_to_string
from django.views.generic.edit import FormView


class UserRegisterView(CreateView):
    """Класс региcтрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались. Проверьте почту для активации!'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = default_token_generator.make_token(user)
        activation_url = reverse_lazy(
            'users:email_verified', kwargs={'token': user.token}
        )
        user.save()

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: http://localhost:8000/{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        return redirect('users:email_confirmation_sent')


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'


class UserLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('/catalog')


class UserConfirmEmailView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return redirect('users:email_confirmation_failed')

        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')


class EmailConfirmationSentView(TemplateView):
    """Письмо подтверждения отправлено"""
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmView(TemplateView):
    """Электронная почта подтверждена"""
    template_name = 'registration/email_verified.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    """Ошибка подтверждения по электронной почте"""
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


def generate_random_password(length=12):
    """Генерация случайного пароля"""
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(secrets.choice(characters) for _ in range(length))
    return new_password


class UserForgotPasswordView(PasswordResetView):
    """Востановление пароля"""
    model = User
    form_class = UserForgotPasswordForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('users:login')
    email_template_name = 'registration/password_reset_mail.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)

        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()

        context = {
            'user': user,
            'new_password': new_password
        }

        email_content = render_to_string(self.email_template_name, context)

        send_mail(
            subject='Восстановление пароля',
            message=email_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super(FormView, self).form_valid(form)
