from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserLoginSerializer
from rest_framework import generics, response, status
from .models import Player, Team, User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token



# Create your views here.

class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return response.Response(
                    {"message": "Success", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as err:
                return response.Response(
                    {"message!": str(err)}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(
                {"message!": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
            

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    return response.Response(
                        data={
                            "token": token.key,
                            "success": "You've successfully Logged in",
                        },
                        status=status.HTTP_200_OK,
                    )

            except User.DoesNotExist:
                return response.Response(
                    data={
                        "message": "error",
                        "data": "Ensure email and password are correct and you have verified your account",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)