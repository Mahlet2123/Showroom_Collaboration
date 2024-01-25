from django.db import models
from django.contrib.auth.models import User

class ApplicationListingCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='application_listing_category_images')
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationListing(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ApplicationListingCategory, on_delete=models.CASCADE)
    request_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)
    need_investor = models.BooleanField()
    need_market = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationListingRequest(models.Model):
    listing_category = models.ForeignKey(ApplicationListingCategory, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=255, choices=[('listing_type_1', 'Listing Type 1'), ('listing_type_2', 'Listing Type 2')])
    id_front = models.FileField(upload_to='application_listing_request_id_front')
    id_back = models.FileField(upload_to='application_listing_request_id_back')
    listing_type = models.TextField()
    is_approved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationListingImage(models.Model):
    image = models.FileField(upload_to='application_listing_images')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationListingFile(models.Model):
    file = models.FileField(upload_to='application_listing_files')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationListingReview(models.Model):
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
