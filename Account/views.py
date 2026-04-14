from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from Account.Registrationserial import UserRegistrationSerializer, LoginSerializer 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAuthenticated,AllowAny

class RegistrationView(APIView):
  permission_classes=[AllowAny]
  def post(self,request):
    serializer=UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)


class LoginView(APIView):
  permission_classes=[AllowAny]
  def post(self,request):
    serializer=LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=authenticate(username=serializer.validated_data['username'],password=serializer.validated_data['password'])
    if user is not None:
      token=Token.objects.get_or_create(user=user)
      return Response({"token":token[0].key},status=status.HTTP_200_OK)
    return Response({"message":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
  permission_classes=[IsAuthenticated]
  def post(self,request):
    token=Token.objects.get(user=request.user)
    token.delete()
    return Response({"message":"User logged out successfully"},status=status.HTTP_200_OK)