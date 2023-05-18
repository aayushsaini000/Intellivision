from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from . serializer import UserSerializer
from rest_framework.authtoken.models import Token
from . models import User



class SignUpAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, created = User.objects.get_or_create(
            email=serializer.validated_data["email"]
        )
        if created:
            instance.set_password(serializer.validated_data["password"])
            instance.save()
            return Response({'message': 'Signup successful.'})
        return Response(
            {
                'message': 'Email already exists.'
            }, status=400
        )


class LoginAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )
        if user:
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
