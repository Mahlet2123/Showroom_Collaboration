from rest_framework import serializers
from .models import ApplicationListing


class ApplicationListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationListing
        fields = '__all__'
