from django.urls import path, include
from .views import ApplicationListingView, ApplicationListingDetailView, ApplicationListingSearchView

urlpatterns = [
    path('api/me/listings/', ApplicationListingView.as_view(), name='user-listings'),
    path('api/listings/<int:pk>/', ApplicationListingDetailView.as_view(), name='listing-detailview'),
    path('api/listings/search/', ApplicationListingSearchView.as_view(), name='listing-search'),
]

