from rest_framework import serializers
from accounts.models import Dealer, User, State, District, Country_Codes, PaymentRequest
from accounts.serializers import StateSerializer, DistrictSerializer, CountryCodesSerializer

class UserSerializer(serializers.ModelSerializer):
    
    country_code = serializers.StringRelatedField(read_only=True)
    state = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    
    country_code_id = serializers.PrimaryKeyRelatedField(
        queryset=Country_Codes.objects.all(),
        source='country_code',
        write_only=True
    )
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        source='state',
        write_only=True
    )
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        source='district',
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'address', 'landmark', 'place', 'pin_code',
            'country_code', 'state', 'district',  
            'country_code_id', 'state_id', 'district_id',  
            'email', 'phone_number', 'watsapp'
        ]

class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Dealer
        fields = ['id', 'profile_image','verificationid_number', 'verification_id', 'id_copy','status', 'user', 'franchisee']  # Include franchisee

    def create(self, validated_data):
        
        user_data = validated_data.pop('user')
        franchisee = validated_data.pop('franchisee', None)  

        
        user = User.objects.create(**user_data)

        
        dealer = Dealer.objects.create(user=user, franchisee=franchisee, **validated_data)

        return dealer


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = '__all__'


