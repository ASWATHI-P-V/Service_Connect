from rest_framework import serializers
from .models import User, ServiceProvider, Country_Codes, State, District, Franchisee, Dealer, Customer, OTP, Service_Type, Collar, Subcategory, ServiceRegister, PaymentRequest, CustomerReview
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CountryCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country_Codes
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')

class FranchiseeSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = Franchisee
        fields = '__all__'

class DealerSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)
    franchisee = FranchiseeSerializer(read_only=True)

    class Meta:
        model = Dealer
        fields = '__all__'

class ServiceProviderSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)
    dealer = DealerSerializer(read_only=True)

    class Meta:
        model = ServiceProvider
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Type
        fields = '__all__'

class CollarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collar
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer(read_only=True)
    collar = CollarSerializer(read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'

class ServiceRegisterSerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderSerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)

    class Meta:
        model = ServiceRegister
        fields = '__all__'

class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = '__all__'

class CustomerReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    service_provider = ServiceProviderSerializer(read_only=True)

    class Meta:
        model = CustomerReview
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    user_id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
        })
        return data