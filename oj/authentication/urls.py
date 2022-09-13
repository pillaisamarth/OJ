from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from authentication.views import CreateUserView, DummyView

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('dummy/', DummyView.as_view(), name='dummy')
]