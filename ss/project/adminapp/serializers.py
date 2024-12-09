from rest_framework import serializers
from accounts.models import User, Franchisee, ServiceRequest, Invoice, Complaint, Ad_Management, Ad_category, Franchise_Type, ServiceProvider, BlockedUser,Dealer

# Serializer for User's Booking Details
class UserBookingDetailsSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name")
    service_provider_name = serializers.CharField(source="service_provider.full_name")
    service_title = serializers.CharField(source="title")   # Assuming `service` has a `title` field

    class Meta:
        model = ServiceRequest
        fields = [
            "booking_id",
            "customer_name",
            "service_provider_name",
            "service_title",
            "work_status",
            "availability_from",
            "availability_to",
            "additional_notes",
            "image",
            "request_date",
        ]
# Serializer for Franchise Booking Details
class FranchiseBookingDetailsSerializer(serializers.ModelSerializer):
    scheduled_date = serializers.DateTimeField(source="valid_from")
    scheduled_time = serializers.DateTimeField(source="valid_up_to")

    class Meta:
        model = Franchisee
        fields = ["custom_id", "community_name", "scheduled_date", "scheduled_time"]

# Serializer for Invoice Details
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["invoice_number", "invoice_type", "description", "total_amount", "payment_status", "invoice_date"]

# Serializer for Complaints
class ComplaintSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name")
    receiver_name = serializers.CharField(source="receiver.full_name")

    class Meta:
        model = Complaint
        fields = ["id", "subject", "description", "status", "sender_name", "receiver_name"]

class ServiceRequestSerializer(serializers.ModelSerializer):
    booking_id = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = ['booking_id', 'customer', 'service_provider', 'service', 'work_status', 'request_date']

    def get_booking_id(self, obj):
        # Generate booking_id if it doesn't exist
        if not obj.booking_id:
            return f"BKID{str(obj.id).zfill(6)}"
        return obj.booking_id

class FranchiseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise_Type
        fields = ['id', 'name', 'details', 'amount', 'currency']

class AdManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad_Management
        fields = '__all__'

class AdCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad_category
        fields = '__all__'



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
