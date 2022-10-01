from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from authentication.views import CreateUserView, LogoutAndBlacklistRefreshTokenForUserView, GetUserView

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('user/get/', GetUserView.as_view(), name='user_view'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
]