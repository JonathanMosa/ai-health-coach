from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .serializers import CheckInSerializer
from .models import CheckIn

class RegisterView(generics.CreateAPIView):
    """Creates a User + linked UserProfile, and returns an auth token."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "token": token.key,
            },
            status=201,
        )

class CheckInListCreateView(generics.ListCreateAPIView):
    """"""
    serializer_class = CheckInSerializer

    def get_queryset(self):
        return CheckIn.objects.filter(user=self.request.user)
        

class CheckInRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = CheckInSerializer
    
    def get_queryset(self):
        return CheckIn.objects.filter(user=self.request.user)