from django.urls import path, include
from . import views

urlpatterns = [
    path('problemlist/', views.ProblemList.as_view(), name="problemlist"),
    path('problemdetail/<int:id>', views.ProblemDetail.as_view(), name="problemdetail"),
    path('submissions/<int:id>', views.submissions, name="submissions"),
    path('submission/<int:id>', views.submission, name="submission"),
    path('submit/', views.Submit.as_view(), name="submit"),
    path('uploadTestCase/', views.uploadTestCase, name='upload-test-case')
]