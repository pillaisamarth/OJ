from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers import CustomUserSerializer
# Create your views here.


class CreateUserView(APIView):
    
    def post(self, request):
        serializer=CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            if user:
                json=serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            print(token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        loggedUser = request.user        
        data = {
            'username' : loggedUser.username,
            'email' : loggedUser.email,
            'rating': loggedUser.rating,
        }

        return Response(data)

