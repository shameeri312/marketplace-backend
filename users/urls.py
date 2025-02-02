from django.urls import path
from . import views

app_name = "user_accounts"

urlpatterns = [
    path("profile/", views.UserView.as_view(), name="user"),
    path("sign-up/", views.SignupView.as_view(), name="sign_up"),
]
