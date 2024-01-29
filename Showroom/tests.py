from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from .models import *


# Create your tests here.
class ApplicationListingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)        
        self.category = ApplicationListingCategory.objects.create(name="Test Category", image="test_image.jpg")
        self.listing_request = ApplicationListingRequest.objects.create(
            user=self.user,
            email="test@example.com",
            listing_category=self.category,
            id_type="NIN",
            listing_type="Test Listing Type",
            is_approved=False
        )
        self.application_listing = ApplicationListing.objects.create(
            vendor=self.user,
            category=self.category,
            listing_request=self.listing_request,
            name="Test Listing",
            description="Test Description",
            country="Test Country",
            province="Test Province",
            city="Test City",
            phone_number="1234567890",
            physical_address="Test Address",
            need_investor=True,
            need_market=False
        )

    def test_application_listing(self):
        url = reverse('Showroom:listing-all')
        response = self.client.get(url)

        self.assertEqual(str(self.application_listing), "Test Listing")
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data['data'][0]['name'], 'Test Listing')

    def tearDown(self):
        User.objects.all().delete()
        ApplicationListingCategory.objects.all().delete()
        ApplicationListingRequest.objects.all().delete()
        ApplicationListing.objects.all().delete()    