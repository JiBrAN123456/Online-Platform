from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterView, LoginView , VerifyEmailView ,TwoFactorSetupView, TwoFactorVerifyView,
    PasswordResetRequestView, PasswordResetConfirmView , PasswordResetRequestView,
    ChangePasswordView , UserProfileView , LogoutView, NotificationView)


router = DefaultRouter()
router.register(r'notifications', NotificationView, basename='notification')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/', include('social_django.urls', namespace='social')),
    #path('auth/', include('rest_framework_social_oauth2.urls')),  # OAuth2 endpoints
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("2fa/setup/", TwoFactorSetupView.as_view()),
    path("2fa/verify/", TwoFactorVerifyView.as_view()),
    path("password-reset/request/", PasswordResetRequestView.as_view()),
    path("password-reset/confirm/<int:uid>/<str:token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("change-password/", ChangePasswordView.as_view()),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
