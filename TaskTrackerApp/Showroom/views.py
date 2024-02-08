from rest_framework import viewsets, pagination, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.pagination import PageNumberPagination
from .serializers import ApplicationListingSerializer, ApplicationListingRequestSerializer
from .models import ApplicationListing
from django.db.models import Q
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema



class ApplicationListingView(generics.ListAPIView):
    """
   View for getting authenticated users.
    """
    queryset = ApplicationListing.objects.order_by('-created_at')
    serializer_class = ApplicationListingSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('created_at', 'name')
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(vendor=self.request.user)
        return ApplicationListing.objects.none()

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=HTTP_200_OK)


class ApplicationListingDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a specific Software/Application listing by ID.
    """
    queryset = ApplicationListing.objects.all()
    serializer_class = ApplicationListingSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except ApplicationListing.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": "Listing not found."})

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)


class ApplicationListingSearchView(views.APIView):
    """
    API endpoint for searching Software/Application listings using POST method.
    """
    @swagger_auto_schema(request_body=ApplicationListingSerializer)
    def post(self, request, *args, **kwargs):
        """
        Handles search requests and returns a paginated list of matching listings.
        """
        search_query = request.data.get('search_query', '')
        queryset = ApplicationListing.objects.all()
        print(search_query)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
            serializer = ApplicationListingSerializer(queryset, many=True)
            if serializer.data:

                return Response(serializer.data, status=HTTP_200_OK)

            return Response('No Application Matching Such Query', HTTP_404_NOT_FOUND)

        return Response('please include search_query in your request body', HTTP_400_BAD_REQUEST)
    
class AllApplicationListingView(generics.ListAPIView):
    
    #View for getting all application listing.
    
    queryset = ApplicationListing.objects.order_by('-created_at')
    serializer_class = ApplicationListingSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('created_at', 'name')
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
  
    

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=HTTP_200_OK)    
    
    
    
class ApplicationListingRequestView(APIView):
    """
    Creates a new application listing request.
    
    This view allows authenticated users to submit a request for creating a new
    software/application listing. The request must include all necessary details
    as specified in the ApplicationListingRequestSerializer. Only authenticated
    users can access this endpoint.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=ApplicationListingRequestSerializer)
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST request to create a new application listing request.
        
        Parameters:
        - request (Request): The request object containing all necessary data.
        
        Returns:
        - Response: The serialized application listing request data on success, or
                    error details on failure.
        """
        serializer = ApplicationListingRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
    
class ApplicationListingVendorRequestView(APIView):
    """
    Submits a new vendor application listing request.
    
    This API endpoint enables authenticated vendors to request the addition of a new
    listing under their account. The endpoint expects data conforming to the
    ApplicationListingSerializer structure. It's designed for vendors who wish to expand
    their visibility by adding more software/application listings to the platform.
    Authentication is required to access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApplicationListingSerializer)
    def post(self, request, *args, **kwargs) -> Response:
        """
        Processes POST request to create a vendor-specific application listing.
        
        Parameters:
        - request (Request): The request object, including listing details.
        
        Returns:
        - Response: The serialized application listing data on successful creation,
                    or error information on failure.
        """
        data = request.data.copy()  # Copy the data to add the vendor manually
        data['vendor'] = request.user.pk  # Assume vendor is the current user
        serializer = ApplicationListingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
