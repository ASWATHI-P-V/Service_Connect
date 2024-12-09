from rest_framework import serializers
from accounts.models import Franchise_Type, ServiceProvider, BlockedUser,Dealer

class FranchiseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise_Type
        fields = ['id', 'name', 'details', 'amount', 'currency']

class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = ['id', 'blocking_user', 'blocked_user', 'is_blocked', 'created_at']
        read_only_fields = ['id', 'created_at']

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ['id', 'custom_id', 'user', 'franchisee']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'custom_id', 'user', 'dealer', 'franchisee']
