from django.db import models
from helpers.models import TimestampsModel
from django.contrib.auth.models import User

class ApplicationListingCategory(TimestampsModel):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='application_listing_category_images')

    def __str__(self):
        return self.name

class ApplicationListing(TimestampsModel):
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

class ApplicationListingRequest(TimestampsModel):
    listing_category = models.ForeignKey(ApplicationListingCategory, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=255, choices=[('listing_type_1', 'Listing Type 1'), ('listing_type_2', 'Listing Type 2')])
    id_front = models.FileField(upload_to='application_listing_request_id_front')
    id_back = models.FileField(upload_to='application_listing_request_id_back')
    listing_type = models.TextField()
    is_approved = models.BooleanField()

class ApplicationListingImage(TimestampsModel):
    image = models.FileField(upload_to='application_listing_images')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)

class ApplicationListingFile(TimestampsModel):
    file = models.FileField(upload_to='application_listing_files')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)

class ApplicationListingReview(TimestampsModel):
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
