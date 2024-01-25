from django.urls import path, include
from .views import ApplicationListingViewSet, IndividualListingView, ListingSearchView

urlpatterns = [
    path(r'api/me/listings/', ApplicationListingViewSet.as_view({'get': 'list'}), name='user-listings'),
    path(r'api/listings/<pk>/', IndividualListingView.as_view({'get': 'retrieve'}), name='individual-listing'),
    path(r'api/listings/search/', ListingSearchView.as_view({'post': 'list'}), name='listing-search'),
]

