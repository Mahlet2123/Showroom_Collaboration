from django.urls import path, include
from .views import ApplicationListingView, ApplicationListingDetailView, ApplicationListingSearchView, AllApplicationListingView

urlpatterns = [
    path('api/me/listings/', ApplicationListingView.as_view(), name='user-listings'),
    path('api/listings/<int:pk>/', ApplicationListingDetailView.as_view(), name='listing-detailview'),
    path('api/listings/search/', ApplicationListingSearchView.as_view(), name='listing-search'),
    path('api/listings/', AllApplicationListingView.as_view(), name='listing-all'),
]

