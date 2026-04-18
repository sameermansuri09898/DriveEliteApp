from django.db import models
from django.conf import settings
from Account.models import CustomUser
# Create your models here.
from django.contrib.auth.models import User

class Car(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    car_name = models.CharField(max_length=100)
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
    seated_capacity = models.IntegerField(default=0)
    controle = models.CharField(max_length=100)  
    owner_name = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return f"{self.car_name} - {self.brand} - {self.model}"

    def perday_offer_price(self):
      return self.price_per_day - (self.price_per_day * self.offer / 100)

    def is_available(self):
      return self.is_available

    def discount(self):
      return self.price_per_day - self.perday_offer_price()

    # for multiple images
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car.name}"

class CarCart(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
  car=models.ForeignKey(Car, on_delete=models.CASCADE,null=True)
  total_price=models.FloatField(default=0)
  days=models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  total_price=models.FloatField(default=0)



  def __str__(self):
    return f"{self.car.name} - {self.user.username} - {self.total_price} - {self.days}"  

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=100, default='pending')
    payment_status = models.CharField(max_length=100, default='pending')
    Razorpay_order_id = models.CharField(max_length=100, default='pending')
    Razorpay_payment_id = models.CharField(max_length=100, default='pending')
    Razorpay_payment_signature = models.CharField(max_length=100, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car.name} - {self.user.username} - {self.start_date} - {self.end_date}"


    