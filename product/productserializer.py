from rest_framework import serializers
from product.models import Car,CarImage

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    class Meta:
        model = Car
        fields = ['id','name','brand','model','price_per_day','car_thumbnail','description','pickup_location','dropoff_location','offer','fine_per_day','final_price','images','is_available']

    def get_final_price(self, obj):
        return obj.perday_offer_price()

    def validate_offer(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Offer must be between 0 and 100")
        return value    

    def validate_fine_per_day(self, value):
        if value < 0:
            raise serializers.ValidationError("Fine per day must be greater than 0")
        return value    

    def validate_is_available(self, value):
        if value not in [True, False]:
            raise serializers.ValidationError("is_available must be True or False")
        return value    

    def get_availability_status(self, obj):
        return "Available" if obj.is_available else "Booked"

 