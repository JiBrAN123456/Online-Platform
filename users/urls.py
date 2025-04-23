from django.urls import path, include
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/', include('social_django.urls', namespace='social')),
    #path('auth/', include('rest_framework_social_oauth2.urls')),  # OAuth2 endpoints
]
