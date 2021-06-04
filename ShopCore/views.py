from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.db.models import Q
from django.contrib import messages
from .models import Category, Product, Commentary, OrderProduct, Order, Payment
from .forms import ContactForm, SubscribeForm, CommentaryForm, UserUpdateForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from ProvodkaShop.settings import EMAIL_HOST_USER, EMAIL_FROM_USER
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
import stripe
from django.conf import settings


class BaseView(View):
    def get(self, request, *args, **kwargs):
        form = SubscribeForm()
        categories = Category.objects.all()
        products = Product.objects.filter(is_active=True)
        context = {
                'categories': categories,
                'products': products,
                'form': form,
        }
        return render(request, 'base.html', context)

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST or None)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.email = form.cleaned_data['email']
            sub.save()
        categories = Category.objects.all()
        products = Product.objects.filter(is_active=True)
        messages.success(request, 'Спасибо за подписку! Теперь вы будете вкурсе о всех новинках!')
        context = {
            'form': form,
            'categories': categories,
            'products': products,
        }
        return render(request, 'base.html', context)


class AboutView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        comments = Commentary.objects.filter(active=True)
        form = CommentaryForm()
        context = {
                'categories': categories,
                'products': products,
                'form': form,
                'comments': comments,
        }
        return render(request, 'about.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentaryForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.email = form.cleaned_data['email']
            comment.name = form.cleaned_data['name']
            comment.body = form.cleaned_data['body']
            comment.save()
        comments = Commentary.objects.filter(active=True)
        categories = Category.objects.all()
        products = Product.objects.all()
        form = CommentaryForm()
        context = {
            'form': form,
            'categories': categories,
            'products': products,
            'comments': comments
        }
        messages.success(request, 'Спасибо за оставленный комментарий! Ваше мнение очень важно для нас.')
        return render(request, 'about.html', context)


class CategoryDetail(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['categories'] = self.model.objects.all()
        if not query and not self.request.GET:
            context['category_products'] = category.product_set.filter(is_active=True)
            return context
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
            context['category_products'] = products
            return context


class ProductDetail(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_object().category.__class__.objects.all()
        return context


class ContactUsView(View):

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories
        }
        return render(request, 'contactus.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                from_email = form.cleaned_data.get('from_email')
                try:
                    send_mail(subject,
                              message, from_email, [EMAIL_HOST_USER], fail_silently=False)
                    # Защита от уязвимости
                except BadHeaderError:
                    return HttpResponse('Неверный заголовок')
                messages.success(request, 'Спасибо за обращение! В скором времени вам поступит ответ')
                return redirect('contact')
        context = {
            'form': form
        }
        return render(request, 'contactus.html', context)


class SearchView(ListView):

    model = Product
    template_name = 'search_result.html'
    context_object_name = ('products')

    def get_queryset(self):
        return Product.objects.filter(is_active=True, title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        context['categories'] = Category.objects.all()
        return context


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
        context = {
            'categories': categories,
            'orders': orders
        }
        return render(request, 'profile.html', context)


def addProduct(request, slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, slug=slug)
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            user=request.user,
            ordered=False
        )
        order = Order.objects.filter(user=request.user, ordered=False)

        if order.exists():
            order = order[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product.quantity += 1
                order_product.save()
            else:
                order.products.add(order_product)

        else:
            order = Order.objects.create(user=request.user, ordered_date=timezone.now())
            order.products.add(order_product)
        return redirect('detail')
    else:
        messages.add_message(request, messages.ERROR, 'Для того чтобы делать покупки вам необходимо авторизироваться в систему')
        return redirect('login')


class OrderView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                categories = Category.objects.all()
                context = {
                    'order': order,
                    'categories': categories
                }
                return render(request, 'cart/detail.html', context)
            except ObjectDoesNotExist:
                return render(request, 'cart/detail.html')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Для того чтобы делать покупки вам необходимо авторизироваться в систему')
            return redirect('login')


@login_required
def removeProduct(request,slug):
    product = get_object_or_404(Product, slug=slug)
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            return redirect('detail')
    return redirect('product_detail', slug=slug)


@login_required
def removeSingleProduct(request,slug):
    product = get_object_or_404(Product, slug=slug)
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
                order_product.delete()
            return redirect('detail')
        return redirect('product_detail', slug=slug)


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            try:
                order = Order.objects.get(user=request.user, ordered=False)
            except Order.DoesNotExist:
                order = None
            user_data = User.objects.get(id=request.user.id)
            context = {
                'categories': categories,
                'order': order,
                'user_data': user_data
            }
            return render(request, 'checkout/order_detail.html', context)
        else:
            messages.add_message(request, messages.ERROR,
                                 'Для того чтобы делать покупки вам необходимо авторизироваться в систему')
            return redirect('login')

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        order_products = order.products.all()
        amount = order.get_total()
        product_list = []
        for order_product in order_products:
            a = 'Товар: '
            b = ', в количестве: '
            c = ' единиц'
            product_list.append(a + (str(order_product.product) + b + str(order_product.quantity)) + c)
        description = ' '.join(product_list)
        charge = stripe.Charge.create(
             amount=int(amount * 100),
             currency='RUB',
             description=description,
             source=token
        )

        payment = Payment(user=request.user)
        payment.stripe_charge_id = charge['id']
        payment.amount = amount
        payment.save()

        order_products.update(ordered=True)
        for product in order_products:
            product.save()

        order.ordered = True
        order.status = 'payed'
        order.payment = payment
        order.ordered_date = timezone.now()
        order.save()
        messages.add_message(request, messages.SUCCESS,
                             'Спасибо за совершённый заказ! '
                             'Как только заказ будет готов в'
                             ' вашем личном кабинете изменится статус, и мы вас оповестим SMS-сообщением')
        return redirect('profile')


@login_required
def profileup(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.add_message(request, messages.SUCCESS,  f'Ваша информация была обновлена')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'profile_edit.html', context)





