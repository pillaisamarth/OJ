from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

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


class DummyView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)