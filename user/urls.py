from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('forgot-password/', views.RestorePassword.as_view(), name='restore password'),
    path('set-password/', views.ChangePassword.as_view(), name='change password'),
]