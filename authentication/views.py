from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from ShopCore.models import Category, User
from .models import User
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from ProvodkaShop.settings import EMAIL_HOST_USER, EMAIL_FROM_USER
from validate_email import validate_email
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Активируйте свою учётную запись'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject=email_subject, body=email_body, from_email=EMAIL_FROM_USER, to=[user.email])
    EmailThread(email).start()


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'authentication/registration.html', context)

    def post(self, request, *args, **kwargs):

        if request.method == "POST":
            context = {'has_error': False, 'data': request.POST}
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            passwordrep = request.POST.get('password2')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            if len(password) < 6:
                messages.add_message(request, messages.ERROR, 'Пароль должен быть больше чем 6 символов')
                context['has_error'] = True

            if password != passwordrep:
                messages.add_message(request, messages.ERROR, 'Введённые пароли не совпдают')
                context['has_error'] = True

            if not validate_email(email):
                messages.add_message(request, messages.ERROR, 'Введите корректный EMAIL')
                context['has_error'] = True

            if not username:
                messages.add_message(request, messages.ERROR, 'Введите логин')
                context['has_error'] = True

            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'Этот логин уже занят')
                context['has_error'] = True

            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Этот EMAIL занят')
                context['has_error'] = True

            if User.objects.filter(address=address).exists():
                messages.add_message(request, messages.ERROR, 'Аккаунт с таким адресом уже существует')
                context['has_error'] = True

            if User.objects.filter(phone=phone).exists():
                messages.add_message(request, messages.ERROR, 'Аккаунт с таким номером телефона уже существует')
                context['has_error'] = True

            if context['has_error']:
                categories = Category.objects.all()
                context = {'categories': categories}
                return render(request, 'authentication/registration.html', context)

            user = User.objects.create_user(username=username, email=email, first_name=name, last_name=surname,
                                            address=address, phone=phone)
            user.set_password(password)
            user.save()

            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'Аккаунт создан, для активации аккаунта перейдите по ссылке, которая придёт вам на '
                                 'электронную почту!')
            return redirect('login')

        return render(request, 'authentication/registration.html')


class LoginView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'authentication/login.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            categories = Category.objects.all()
            context = {'data': request.POST,
                       'categories': categories}
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                     'Ваша электронная почта не активирована, пожалуйста проверьте вашу почту.')
                return render(request, 'authentication/login.html', context)

            if not user:
                messages.add_message(request, messages.ERROR, 'Неверные учётные данные')
                return render(request, 'authentication/login.html', context)
            login(request, user)

            return redirect(reverse('home'))

        return render(request, 'authentication/login.html')


def activate_profile(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:

        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Электронная почта подтверждена, теперь вы можете войти в аккаунт!')
        return redirect(reverse('login'))
    return render(request, 'authentication/activate-failed.html', {'user': user})