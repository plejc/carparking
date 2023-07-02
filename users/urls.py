from django.urls import path
from . import views



urlpatterns = [
    path("userlogin/", views.LoginView.as_view()),
    path("logout/", views.LogOutView.as_view()),
    path("signup-view/", views.SignUpView.as_view(), name="signup"),
]