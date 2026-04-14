from rest_framework import serializers
from product.models import Car,CarImage,Booking

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = ['id','car_name','brand','model','price_per_day','car_thumbnail','description','pickup_location','dropoff_location','offer','fine_per_day','final_price','discount','images','is_available','owner_name','controle','seated_capacity']
        read_only_fields = ['user'] 

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
    

    def validate_seated_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError("Seated capacity must be greater than 0")
        return value    

    def get_is_available(self, obj):
        return "Available" if obj.is_available else "Booked"

    def get_discount(self, obj):
        return obj.discount()    
 
class BookingSerializer(serializers.ModelSerializer):
    final_booking_price = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['id','car','user','start_date','end_date','total_price','final_booking_price']

    def validate(self, attrs):
        car = attrs['car']
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        if car.is_available(start_date, end_date):
            raise serializers.ValidationError("Car is not available for the selected dates")
        return attrs

    def get_final_booking_price(self, obj):
        return obj.total_price()    

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)    