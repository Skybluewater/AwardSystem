from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('reset/', ChangePasswordLogin.as_view(), name="change_pass_login"),
    path('name/', ChangePasswordUnLoginName.as_view(), name="change_pass_anonymous_name"),
    re_path('pass/(?P<token>.*)$', ChangePasswordUnLoginToken.as_view(), name="change_pass_anonymous_pass")
]
