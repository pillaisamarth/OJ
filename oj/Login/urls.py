from django.urls import path, include
from . import views

urlpatterns = [
    path('loginpage/', views.login, name = "login"),
]