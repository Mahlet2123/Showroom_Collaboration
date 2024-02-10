from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from Showroom.models import *


# Create your tests here.
class ApplicationListingCreateTest(TestCase):
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
        
    def test_application_listing_create(self):
        url = reverse('create-listing')
        data = {
            "name": "Test Listing",
            "description": "Test Description",
            "country": "Test Country",
            "province": "Test Province",
            "city": "Test City",
            "phone_number": "1234567890",
            "physical_address": "Test Address",
            "need_investor": True,
            "need_market": True,
            "category": self.category.id,
            "listing_request": self.listing_request.id
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        User.objects.all().delete()
        ApplicationListingCategory.objects.all().delete()
        ApplicationListingRequest.objects.all().delete()
        ApplicationListing.objects.all().delete() 


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
        url = reverse('listing-all')
        response = self.client.get(url)

        self.assertEqual(str(self.application_listing), "Test Listing")
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data['data'][0]['name'], 'Test Listing')

    def tearDown(self):
        User.objects.all().delete()
        ApplicationListingCategory.objects.all().delete()
        ApplicationListingRequest.objects.all().delete()
        ApplicationListing.objects.all().delete()

class ApplicationListingAPITests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = ApplicationListingCategory.objects.create(name="Test Category")
        self.client = APIClient()

    def test_application_listing_request_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('listing-request')
        data = {
            "email": "test@example.com",
            "listing_category": self.category.id,
            "id_type": "NIN",
            "listing_type": "Software",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_application_listing_request_unauthorized(self):
        url = reverse('listing-request')
        data = {
            "email": "test@example.com",
            "listing_category": self.category.id,
            "id_type": "NIN",
            "listing_type": "Software",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_application_listing_vendor_request_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('vendor-listing-request')
        data = {
            "name": "Test Listing",
            "description": "A test listing",
            "country": "Country",
            "province": "Province",
            "city": "City",
            "phone_number": "1234567890",
            "physical_address": "123 Test St",
            "need_investor": False,
            "need_market": False,
            "category": self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_application_listing_vendor_request_unauthorized(self):
        url = reverse('vendor-listing-request')
        data = {
            "name": "Test Listing",
            "description": "A test listing",
            "country": "Country",
            "province": "Province",
            "city": "City",
            "phone_number": "1234567890",
            "physical_address": "123 Test St",
            "need_investor": False,
            "need_market": False,
            "category": self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

