from django.urls import path
from .views import *

app_name = 'Showroom'

urlpatterns = [
    path('api/listings/me/', ApplicationListingView.as_view(), name='user-listings'),
    path('api/listings/<int:pk>/', ApplicationListingDetailView.as_view(), name='listing-detailview'),
    path('api/listings/search/', ApplicationListingSearchView.as_view(), name='listing-search'),
    path('api/listings/', AllApplicationListingView.as_view(), name='listing-all'),
]

