from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Franchise_Type, ServiceProvider, BlockedUser,Dealer
from .serializers import FranchiseTypeSerializer, BlockedUserSerializer, DealerSerializer, ServiceProviderSerializer


class FranchiseTypeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        """
        Retrieve a specific franchise type by ID passed in the request body.
        """
        franchise_id = request.data.get('id')  # Extract ID from the request body
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
        franchise_id = request.data.get('id')  # ID must be provided in the request body
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


class BlockDealerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Resolve franchisee
            franchise = request.user.franchisee.first()
            if not franchise:
                return Response({"error": "User is not associated with any franchise."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate custom_id
            custom_id = request.data.get('custom_id')
            if not custom_id:
                return Response({"error": "Custom ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the dealer by custom_id
            dealer = Dealer.objects.get(custom_id=custom_id, franchisee=franchise)

            # Check if the dealer is already blocked
            blocked_user, created = BlockedUser.objects.update_or_create(
                blocking_user=request.user,
                blocked_user=dealer.user,
                defaults={'is_blocked': True}
            )

            if not created and blocked_user.is_blocked:
                return Response({"message": "Dealer is already blocked."}, status=status.HTTP_200_OK)

            return Response({"message": "Dealer has been successfully blocked."}, status=status.HTTP_200_OK)

        except Dealer.DoesNotExist:
            return Response({"error": "Dealer with the specified custom_id does not exist under your franchise."}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "Invalid franchise user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlockServiceProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Validate custom_id
            custom_id = request.data.get('custom_id')
            if not custom_id:
                return Response({"error": "Custom ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the service provider by custom_id
            service_provider = ServiceProvider.objects.get(custom_id=custom_id)

            # Check if the service provider is already blocked
            blocked_user, created = BlockedUser.objects.update_or_create(
                blocking_user=request.user,
                blocked_user=service_provider.user,
                defaults={'is_blocked': True}
            )

            if not created and blocked_user.is_blocked:
                return Response({"message": "Service Provider is already blocked."}, status=status.HTTP_200_OK)

            return Response({"message": "Service Provider has been successfully blocked."}, status=status.HTTP_200_OK)

        except ServiceProvider.DoesNotExist:
            return Response({"error": "Service Provider with the specified custom_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
