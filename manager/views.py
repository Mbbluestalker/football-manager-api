from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework import generics, response, status

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