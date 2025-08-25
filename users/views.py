from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


User = get_user_model()


@extend_schema(tags=["Auth"]) 
class RegistrationView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer
	permission_classes = [AllowAny]


@extend_schema(tags=["Auth"]) 
class MeView(generics.RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return self.request.user


@extend_schema(tags=["Auth"]) 
class LoginView(TokenObtainPairView):
	permission_classes = [AllowAny]


@extend_schema(tags=["Auth"]) 
class RefreshView(TokenRefreshView):
	permission_classes = [AllowAny]
