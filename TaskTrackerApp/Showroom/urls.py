from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/me/listings/', ApplicationListingView.as_view(), name='user-listings'),
    path('api/listings/<int:pk>/', ApplicationListingDetailView.as_view(), name='listing-detailview'),
    path('api/listings/search/', ApplicationListingSearchView.as_view(), name='listing-search'),
    path('api/listings/', AllApplicationListingView.as_view(), name='listing-all'),
    path('api/listings/request/', ApplicationListingRequestView.as_view(), name='listing-request'),
    path('api/listings/vendor/request/', ApplicationListingVendorRequestView.as_view(), name='vendor-listing-request'),

]

