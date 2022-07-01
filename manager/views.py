from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserLoginSerializer, EditTeamSerializer
from rest_framework import generics, response, status
from .models import Player, Team, User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404




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
    

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return response.Response(
            data={"success": "You've been logged out"}, status=status.HTTP_200_OK
        )
        
class EditTeamView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EditTeamSerializer
    queryset = Team.objects.all()

    def patch(self, request, *args, **kwargs):
        team = get_object_or_404(Team, user__id=request.user.id)
        serializer = self.serializer_class(Team, data=request.data, partial=True)
        if serializer.is_valid():
            team.name = serializer.validated_data["name"]
            team.country = serializer.validated_data["country"]
            team.save()
            return response.Response(
                self.serializer_class(team).data, status=status.HTTP_202_ACCEPTED
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
