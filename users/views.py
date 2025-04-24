from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, LoginSerializer, JWTTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .utils import verify_token
from .models import User

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]



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




class VerifyEmailView(APIView):
     def get(self, request):
         token = request.GET.get("token")
         email = verify_token(token)
         if email:
              user = User.objects.filter(email=email).first()
              if user and not user.is_verified:
                 user.is_verified = True
                 user.save()
                 return Response({"detail" : "Email Verified"})
              return Response({"detail":"Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)  