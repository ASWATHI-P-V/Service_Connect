from rest_framework import serializers
from accounts.models import Dealer, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'address', 'phone_number', 'email', 'watsapp']


class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for User

    class Meta:
        model = Dealer
        fields = ['id', 'about', 'profile_image', 'user']

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update fields in the Dealer model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update fields in the related User model
        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance
