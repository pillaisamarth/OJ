from django.urls import path, include
from . import views

urlpatterns = [
    path('problemlist/', views.problemlist, name="problemlist"),
    path('problemdetail/<int:id>', views.problemdetail, name="problemdetail"),
    path('submissions/<int:id>', views.submissions, name="submissions"),
    path('submission/<int:id>', views.submission, name="submission"),
    path('submit/', views.submitFile, name="submitFile"),
    path('uploadTestCase/', views.uploadTestCase, name='upload-test-case')
]