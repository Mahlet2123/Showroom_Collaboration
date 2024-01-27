from django.contrib import admin
from .models import *

admin.site.register(ApplicationListing)
admin.site.register(ApplicationListingCategory)
admin.site.register(ApplicationListingRequest)
admin.site.register(ApplicationListingReview)
admin.site.register(ApplicationListingImage)
admin.site.register(ApplicationListingFile)
admin.site.register(ApplicationListingRating)