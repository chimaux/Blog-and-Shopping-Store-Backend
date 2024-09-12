from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# from django.contrib.auth.models import User
from myusers.models import CustomUser
from .serializers import UserSerializer
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
def login(request):
    try:
        user = CustomUser.objects.get(email=request.data['email'])
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)

        

       
    if not user.check_password(request.data['password']):
        return Response({"error:":"Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
    
    refresh = RefreshToken.for_user(user)  # Generate tokens using SimpleJWT

    # Serialize the user data (you can customize what fields to return)
    serializer = UserSerializer(instance=user)

    # Return the access token, refresh token, and serialized user data
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": serializer.data
    })
    # token, created = Token.objects.get_or_create(user=user)
    # serializer = UserSerializer(instance=user)
    # return Response({"token": token.key, "user": serializer.data})


login_view = login


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Log the error message
            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


signup_view = signup


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


test_token_view = test_token
