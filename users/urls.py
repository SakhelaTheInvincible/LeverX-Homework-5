from django.urls import path
from .views import RegistrationView, LoginView, RefreshView, MeView


app_name = "users"

urlpatterns = [
	path("register/", RegistrationView.as_view(), name="register"),
	path("login/", LoginView.as_view(), name="login"),
	path("refresh/", RefreshView.as_view(), name="refresh"),
	path("me/", MeView.as_view(), name="me"),
]

