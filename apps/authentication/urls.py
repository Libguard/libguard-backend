from django.urls import path
from .views import RegisterView, LoginView, RefreshView, GoogleLoginView, GoogleCallbackView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('refresh/', RefreshView.as_view(), name='auth_refresh'),
    path('google/', GoogleLoginView.as_view(), name='auth_google'),
    path('google/callback/', GoogleCallbackView.as_view(), name='auth_google_callback')
]