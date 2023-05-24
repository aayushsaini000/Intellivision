from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from . serializer import (
    UserSerializer, RestorePasswordSerializer,
    ChangePasswordSerializer, PasswordSerializer 
)
from rest_framework.authtoken.models import Token
from . models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .custom_token import account_activation_token
from django.shortcuts import render



class SignUpAPIView(generics.CreateAPIView):
    """
    Admin Signup
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(
            email=serializer.validated_data["email"]
        ).exists():
            return Response(
                {
                    'message': 'Email already exists.'
                }, status=400
            )
        
        User.objects.create_superuser(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response({'message': 'Signup successful.'})


class LoginAPIView(generics.CreateAPIView):
    """
    Admin Login
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )
        if user and user.is_superuser:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'message': 'Login successful.'
                }
            )
        return Response(
            {
                'message': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED
        )


class RestorePassword(APIView):
    """
    Restore password
    """
    def post(self, request):
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = get_object_or_404(User, email=email)
        URI = request.build_absolute_uri()
        BASE_URL = URI.split("auth")[0]
        try:
            send_mail(
                "Change your password",
                None, None, [email],
                html_message=render_to_string(
                    "mail_change_password.html",
                    {
                        "domain": BASE_URL,
                        "reset_link": (
                            f"{BASE_URL}auth/confirm-password/?"
                            f"uid={urlsafe_base64_encode(force_bytes(user.pk))}"
                            f"&token={account_activation_token.make_token(user)}/"
                        ),
                    }
                )
            )
            return Response(
                {
                    "message": "You will receive an email shortly"
                }
            )
        except Exception:
            return Response(
                {
                    "message": "Something went wrong, Please try again later"
                },
                status=400
            )



class ChangePassword(APIView):
    """
    Change password
    """
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data["password"]
        uid = serializer.data["uid"]
        token = serializer.data["token"]
        uid = force_str(urlsafe_base64_decode(uid))
        if uid.isnumeric():
            user = get_object_or_404(User, pk=uid)
            if account_activation_token.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response(
                    {
                        "message": "Password changed successfully!"
                    }
                )
        return Response(
            {
                "message": "Access denied"
            },
            status=400
        )


class SetNewPassword(APIView):
    """
    Set New password
    """
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, pk=request.user.id)
        new_password = request.data.get("password")
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})


def template_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # Perform validation and save to the database (e.g., using Django's ORM)
        return render(request, 'confirm_password.html', {'success_message': 'Your password reset successfully'})
    return render(request, 'confirm_password.html')