from rest_framework import viewsets, pagination, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from .serializers import ApplicationListingSerializer
from .models import ApplicationListing
from django.db.models import Q


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
