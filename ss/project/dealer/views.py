from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Dealer, Franchisee, PaymentRequest
from .serializers import DealerSerializer,UserSerializer, PaymentRequestSerializer
from rest_framework.parsers import MultiPartParser, FormParser , JSONParser

class DealerDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    
    def post(self, request):
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
            dealer = Dealer.objects.get(custom_id=custom_id)
            if dealer.franchisee.user != request.user:
                return Response(
                    {"detail": "This dealer is not associated with your franchise."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = DealerSerializer(dealer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dealer.DoesNotExist:
            return Response(
                {"detail": "Dealer with the given custom_id not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    
    def put(self, request):
        if not request.user.is_franchisee:
            return Response(
                {"detail": "You are not authorized to update this information."},
                status=status.HTTP_403_FORBIDDEN,
            )

        custom_id = request.data.get('custom_id')
        if not custom_id:
            return Response(
                {"detail": "custom_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            dealer = Dealer.objects.get(custom_id=custom_id)

            
            if dealer.franchisee.user != request.user:
                return Response(
                    {"detail": "This dealer is not associated with your franchise."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            
            serializer = DealerSerializer(dealer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Dealer.DoesNotExist:
            return Response(
                {"detail": "Dealer with the given custom_id not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


    def get(self, request):
        if not request.user.is_franchisee:
            return Response(
                {"detail": "You are not authorized to search for dealers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        custom_id = data.get('custom_id', None)

        if not custom_id:
            return Response(
                {"detail": "custom_id is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        
        try:
            dealer = Dealer.objects.get(custom_id=custom_id)

            
            if dealer.franchisee.user != request.user:
                return Response(
                    {"detail": "This dealer is not associated with your franchise."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            
            serializer = DealerSerializer(dealer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Dealer.DoesNotExist:
            return Response(
                {"detail": "Dealer with the given custom_id not found."},
                status=status.HTTP_404_NOT_FOUND,
            )



class AddDealerView(APIView):
    def post(self, request):
        serializer = DealerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                'message': 'Dealer added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error while adding dealer',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class PaymentRequestListCreateView(APIView):
    def get(self, request):
        """Retrieve all payment requests"""
        payment_requests = PaymentRequest.objects.all()
        serializer = PaymentRequestSerializer(payment_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new payment request"""
        serializer = PaymentRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
