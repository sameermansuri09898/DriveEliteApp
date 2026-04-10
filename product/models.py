from django.db import models
from django.conf import settings
# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price_per_day = models.IntegerField()
    car_thumbnail = models.ImageField(upload_to='car_thumbnail/',null=True,blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    offer = models.FloatField(default=0)
    fine_per_day = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.name} - {self.brand} - {self.model}"

    def perday_offer_price(self):
      return self.price_per_day - (self.price_per_day * self.offer / 100)

    


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car.name}"



# class Booking(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     total_price = models.FloatField(default=0)
#     status = models.CharField(max_length=100, default='pending')
#     payment_status = models.CharField(max_length=100, default='pending')
#     payment_id = models.CharField(max_length=100, default='pending')
#     payment_signature = models.CharField(max_length=100, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f"{self.car.name} - {self.user.username} - {self.start_date} - {self.end_date}"