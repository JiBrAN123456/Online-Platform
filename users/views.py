from django.shortcuts import render
from rest_framework import status, generics , permissions , viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, LoginSerializer, JWTTokenSerializer , UserProfileSerializer, NotificationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .utils import verify_token
from .models import User , LoginHistory , UserActivityLog , Notification
import pyotp
import qrcode
import io
import base64
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from .utils import log_user_activity
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from users.tasks import send_welcome_email

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

               LoginHistory.objects.create(
                    user=user,
                    ip_address = request.META.get("REMOTE_ADDR"),
                    user_agent = request.META.get("HTTP_USER_AGENT", "")
               )
               
               log_user_activity(user , request , "login")



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
                 send_welcome_email.delay(user.id)
                 return Response({"detail" : "Email Verified"})
              return Response({"detail":"Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)  
         


class TwoFactorSetupView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self,request):
          user = request.user

          if not user.otp_secret:
               user.otp_secret = pyotp.random_base32()
               user.save() 

          totp_uri = user.get_totp_uri()


          qr = qrcode.make(totp_uri)
          buffer = io.BytesIO()
          qr.save(buffer, format="PNG")
          qr_base64 = base64.b64encode(buffer.getvalue()).decode()

          return Response({
            "otp_uri": totp_uri,
            "qr_code_base64": qr_base64
          })
     


class TwoFactorVerifyView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          user = request.user
          otp = request.data.get("otp")
          totp = pyotp.TOTP(user.otp_secret)

          if totp.verify(otp):
               user.is_2fa_enabled = True
               user.save()
               return Response({"message": "2FA setup complete"})
          return Response({"error": "Invalid OTP"}, status=400)
     

class PasswordResetRequestView(APIView):
     def post(self,request):
          email = request.data.get("email")
          user = User.objects.filter(email=email).first()

          if user:
               token = default_token_generator.make_token(user)
               reset_url = request.build_absolute_uri(
                    reverse("password rest confirm", kwargs={"uid":user.pk, "token": token})
               )
               send_mail(
                    subject = "Password Reset",
                    message = f"Reset your password : {reset_url}",
                    from_email = "noreply@onlinecourse.com",
                    recipient_list=[email],
               )
          return Response({"message": "If the email exists, reset instructions have been sent."})



class PasswordResetConfirmView(APIView):
     def post(self, request, uid, token):
         user = User.objects.filter(pk=uid).first()
         if user and default_token_generator.check_token(user, token):
              new_password = request.data.get("password") 
              user.set_password(new_password)
              user.save()
              return Response({"message": "Password has been reset successfully"})
         return Response({"error": "Invalid or expired token"}, status=400)
     



class ChangePasswordView(APIView):
     permission_classes = [IsAuthenticated]


     def post(self , request):
         user = request.user
         current = request.data.get("current password") 
         new = request.data.get("new password")

         
         if not user.check_password(current):
            return Response({"error": "Current password is incorrect"}, status=400)

         user.set_password(new)
         user.save()
         return Response({"message": "Password changed successfully"})
     

class UserProfileView(generics.RetrieveUpdateAPIView):
     serializer_class = UserProfileSerializer
     permission_classes = [permissions.IsAuthenticated]


     def get_object(self):
          return self.request.user


class LogoutView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          try:
             refresh_token = request.data.get("refresh_token")
             token = RefreshToken(refresh_token)
             token.blacklist()

             log_user_activity(request.user, request, "logout")

             return Response({"detail": "Sucessfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
          except TokenError as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
          

class NotificationView(viewsets.ModelViewSet):          

     serializer_class = NotificationSerializer
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
          return Notification.objects.filter(user=self.request.user)     
     

     def perform_create(self,serializer):
         serializer.save(use=self.request.user)

     def mark_as_read(self, request):
         notifications = self.get_queryset().filter(is_read=False) 
         notifications.update(is_read= True)
         return Response({"status":"marked as read"}, status=status.HTTP_202_ACCEPTED)    