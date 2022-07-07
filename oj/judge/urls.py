from django.urls import path, include
from . import views

urlpatterns = [
    path('problemlist/', views.problemlist, name="problemlist"),
    path('problemdetail/<int:id>', views.problemdetail, name="problemdetail"),
    path('submit/', views.submit, name="submit"), 
    path('submissions/<int:id>', views.submissions, name="submissions"),
    path('submission/<int:id>', views.submission, name="submission")
]