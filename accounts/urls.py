from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,UserBankAccountUpdateView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='Register'),
    path('login/',UserLoginView.as_view(),name='Login'),
    path('logout/',UserLogoutView.as_view(http_method_names=['get','post']),name='Logout'),
    path('profile/',UserBankAccountUpdateView.as_view(),name='Profile')
]