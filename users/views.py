from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, LoginSerializer, JWTTokenSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer



class LoginView(generics.GenericAPIView):
     serializer_class = LoginSerializer

     def post(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data)   
          if serializer.is_valid():
               user = serializer.validated_data
               refresh = RefreshToken.for_user(user)
               return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)

               })
          return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
