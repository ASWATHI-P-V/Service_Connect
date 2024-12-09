from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from .models import Country_Codes
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import User, Franchisee, Dealer, ServiceProvider, Customer
from .serializers import (
    UserSerializer, FranchiseeSerializer, DealerSerializer,
    ServiceProviderSerializer, CustomerSerializer, TokenObtainPairSerializer,
    LoginSerializer
)
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# ViewSet for Franchisee model with IsAuthenticated permission
class FranchiseeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.FRANCHISEE:
            return Franchisee.objects.filter(user=user)
        return Franchisee.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FranchiseeSerializer
        return super().get_serializer_class()

# ViewSet for Dealer model with IsAuthenticated permission
class DealerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.DEALER:
            return Dealer.objects.filter(user=user)
        return Dealer.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DealerSerializer
        return super().get_serializer_class()

# ViewSet for ServiceProvider model with IsAuthenticated permission
class ServiceProviderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.SERVICE_PROVIDER:
            return ServiceProvider.objects.filter(user=user)
        return ServiceProvider.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceProviderSerializer
        return super().get_serializer_class()

# ViewSet for Customer model with IsAuthenticated permission
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.CUSTOMER:
            return Customer.objects.filter(user=user)
        return Customer.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        return super().get_serializer_class()

# JWT Login View
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:

                #jwt tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'is_customer': user.is_customer,
                    'is_superuser': user.is_superuser,
                    'is_service_provider': user.is_service_provider,
                    'is_franchisee': user.is_franchisee,
                    'is_dealer': user.is_dealer,
                }

                return Response(response_data, status=200)
            else:
                return Response({"detail": "Invalid email or password."}, status=401)
        else:
            return Response(serializer.errors, status=400)

# JWT Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]  # No authentication required to refresh token

# Home view
def home(request):
    return HttpResponse("Welcome to my Django project!")



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def post(self, request):
        # Check if the user is a franchise
        if not request.user.is_franchisee:
            return Response(
                {"detail": "You are not authorized to view this information."},
                status=status.HTTP_403_FORBIDDEN,
            )

        custom_id = request.data.get('custom_id')

        if not custom_id:
            return Response(
                {"detail": "custom_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get the dealer by custom_id
            dealer = Dealer.objects.get(custom_id=custom_id)

            # Check if the dealer belongs to the logged-in franchise
            if dealer.franchisee.user != request.user:
                return Response(
                    {"detail": "This dealer is not associated with your franchise."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Serialize and return the dealer's details
            serializer = DealerSerializer(dealer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dealer.DoesNotExist:
            return Response(
                {"detail": "Dealer with the given custom_id not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

