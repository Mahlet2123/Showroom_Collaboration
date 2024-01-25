from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, views
from .serializers import ApplicationListingSerializer
from .models import ApplicationListing

class ApplicationListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and retrieving Software/Application listings.
    """
    queryset = ApplicationListing.objects.all().order_by('-created_at')
    serializer_class = ApplicationListingSerializer
    filter_backends = (OrderingFilter, filters.SearchFilter)
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(vendor=user)
        return None

class IndividualListingView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retrieving a specific Software/Application listing by ID.
    """
    queryset = ApplicationListing.objects.all()
    serializer_class = ApplicationListingSerializer

class ListingSearchView(views.APIView):
    """
    API endpoint for searching Software/Application listings.
    """
    queryset = ApplicationListing.objects.all()
    serializer_class = ApplicationListingSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['created_at', 'name']

