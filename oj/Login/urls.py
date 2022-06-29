from django.urls import path, include
from . import views

urlpatterns = [
    path('loginpage/', views.login, name = "login"),
    path('problemlist/', views.problemlist, name="problemlist"),
    path('problemdetail/<int:id>', views.problemdetail, name="problemdetail"),
    path('submissions/', views.submit, name="submissions")
]