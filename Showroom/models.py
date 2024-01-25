from django.db import models
from helpers.models import TimestampsModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class ApplicationListingCategory(TimestampsModel):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='application_listing_category_images')

    def __str__(self):
        return self.name
    
class ApplicationListingRequest(TimestampsModel):

    ID_TYPE_CHOICES = [
        ('NIN', 'NIN'),
        ("Driver's License", "Driver's License"),
        ("Voter's Card", "Voter's Card")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    listing_category = models.ForeignKey(ApplicationListingCategory, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=30, choices=ID_TYPE_CHOICES)
    id_front = models.FileField(upload_to='listings/vendors/id_files', null=True, blank=True)
    id_back = models.FileField(upload_to='listings/vendors/id_files', null=True, blank=True)
    listing_type = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Business Listing Vendor: ' + self.email.__str__()    

class ApplicationListing(TimestampsModel):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ApplicationListingCategory, on_delete=models.CASCADE)
    listing_request = models.OneToOneField(ApplicationListingRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)
    need_investor = models.BooleanField()
    need_market = models.BooleanField()

    def __str__(self, *args, **kwargs):
        return self.name

class ApplicationListingImage(TimestampsModel):
    image = models.FileField(upload_to='application_listing_images')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.listing.name}"

class ApplicationListingFile(TimestampsModel):
    file = models.FileField(upload_to='application_listing_files')
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"File for {self.listing.name}"

class ApplicationListingRating(TimestampsModel):
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

class ApplicationListingReview(TimestampsModel):
    listing = models.ForeignKey(ApplicationListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.listing.name}"    
