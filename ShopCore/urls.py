from django.urls import path
from . import views
from .views import (
    BaseView,
    CategoryDetail,
    ProductDetail,
    ContactUsView,
    SearchView,
    AboutView,
    ProfileView,
    OrderView,
    CheckoutView,







)


urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('contact_us/', ContactUsView.as_view(), name='contact'),
    path('search/', SearchView.as_view(), name='search_result'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('add_product/<str:slug>', views.addProduct, name='add_product'),
    path('cart/detail/', OrderView.as_view(), name='detail'),
    path('remove_product/<str:slug>', views.removeProduct, name='remove_product'),
    path('remove-single-product/<str:slug>', views.removeSingleProduct, name='remove_single_product'),
    path('checkout/order_detail/', CheckoutView.as_view(), name='checkout'),
    path('profile-edit/', views.profileup, name='profile_edit')
]