from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import ServiceRequest, Franchisee, Invoice, Complaint, Ad_Management, Ad_category, ServiceProvider, Franchise_Type,BlockedUser,Dealer
from adminapp.serializers import (
    UserBookingDetailsSerializer,
    FranchiseBookingDetailsSerializer,
    InvoiceSerializer,
    ComplaintSerializer,
    FranchiseTypeSerializer,
    AdManagementSerializer,
    AdCategorySerializer
)
from django.utils.timezone import now
from django.db.models import Q


class BookingDetailsView(APIView):
    def post(self, request):
        try:
            booking_id = request.data.get('booking_id')
            if not booking_id:
                return Response({"error": "Booking ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            
            booking = ServiceRequest.objects.get(booking_id=booking_id)

            
            user = booking.service_provider

           
            franchises = Franchisee.objects.filter(user=user)

            
            complaints = Complaint.objects.filter(sender=user) | Complaint.objects.filter(receiver=user)

            
            invoices = Invoice.objects.filter(sender=user) | Invoice.objects.filter(receiver=user)

         
            booking_data = UserBookingDetailsSerializer(booking).data
            franchise_data = FranchiseBookingDetailsSerializer(franchises, many=True).data
            complaint_data = ComplaintSerializer(complaints, many=True).data
            invoice_data = InvoiceSerializer(invoices, many=True).data

           
            response_data = {
                "user": {
                    "name": user.full_name,
                    "place": user.place,
                },
                "booking_details": booking_data,
                "franchises": franchise_data,
                "complaints": complaint_data,
                "invoices": invoice_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ServiceRequest.DoesNotExist:
            return Response({"error": "Booking with the provided ID not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FranchiseTypeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        """
        Retrieve a specific franchise type by ID passed in the request body.
        """
        franchise_id = request.data.get('id')  
        if not franchise_id:
            return Response({"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            franchise_type = Franchise_Type.objects.get(id=franchise_id)
        except Franchise_Type.DoesNotExist:
            return Response({"error": "Franchise type not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FranchiseTypeSerializer(franchise_type)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = FranchiseTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FranchiseTypeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Update a franchise type by extracting the ID from the request body.
        """
        franchise_id = request.data.get('id')  
        if not franchise_id:
            return Response({"error": "ID is required to update franchise type."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            franchise_type = Franchise_Type.objects.get(id=franchise_id)
        except Franchise_Type.DoesNotExist:
            return Response({"error": "Franchise type not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FranchiseTypeSerializer(franchise_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AdListView(APIView):
    """
    Fetch ads based on the selected franchise or service provider from the body.
    Provides sorting options for newest and oldest ads.
    """
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

       
        body_data = request.data  
        franchise_id = body_data.get('franchise_id')
        service_provider_id = body_data.get('service_provider_id')
        sort_order = body_data.get('sort', 'newest')

        
        ads = Ad_Management.objects.all()

        if franchise_id:
            ads = ads.filter(ad_user__franchisee__id=franchise_id)
        elif service_provider_id:
            ads = ads.filter(ad_user__service_provider__id=service_provider_id)
        elif user.is_franchisee:
            ads = ads.filter(ad_user__franchisee__user=user)
        elif user.is_service_provider:
            ads = ads.filter(ad_user__service_provider__user=user)
        else:
            return Response(
                {"error": "Please provide valid franchise_id or service_provider_id in the request body."},
                status=status.HTTP_400_BAD_REQUEST
            )

      
        if sort_order == 'newest':
            ads = ads.order_by('-valid_from')
        elif sort_order == 'oldest':
            ads = ads.order_by('valid_from')

        
        serializer = AdManagementSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdCategoryEditView(APIView):
    """
    View for editing ad categories by passing the ID in the request body.
    """
    def put(self, request):
        
        ad_category_id = request.data.get('id')
        if not ad_category_id:
            return Response({"error": "Ad category ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            ad_category = Ad_category.objects.get(pk=ad_category_id)
        except Ad_category.DoesNotExist:
            return Response({"error": "Ad category not found"}, status=status.HTTP_404_NOT_FOUND)

       
        serializer = AdCategorySerializer(ad_category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddNewAdView(APIView):
    """
    View to create a new ad.
    """
    def post(self, request):
        serializer = AdManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



