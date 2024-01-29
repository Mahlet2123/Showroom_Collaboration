from rest_framework import serializers
from .models import ApplicationListing, ApplicationListingCategory, ApplicationListingRequest, User

class ApplicationListingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationListingCategory
        fields = '__all__'

class ApplicationListingRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Use PrimaryKeyRelatedField for efficiency

    class Meta:
        model = ApplicationListingRequest
        fields = '__all__'

class ApplicationListingSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()  # Use SerializerMethodField for custom representation
    vendor = serializers.StringRelatedField()
    listing_request_is_approved = serializers.BooleanField(source='listing_request.is_approved', read_only=True)
    class Meta:
        model = ApplicationListing
        fields = ('id', 'created_at', 'updated_at', 'name', 'description', 'country', 'province', 'city',
                  'phone_number', 'physical_address', 'need_investor', 'need_market', 'vendor',
                  'category', 'listing_request_is_approved')
    def get_category(self, obj):
        return {
            'name': obj.category.name,
            'image': obj.category.image.url  # Assuming you have a URL field for the image
        }
