from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    RegisterView,
    LoginView,
    )


urlpatterns = [
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('activate-profile/<uidb64>/<token>', views.activate_profile, name='activate'),
]