from django.contrib import admin
from product.models import Car,CustomUser

@admin.register(Car)
class Caradmin(admin.ModelAdmin):
  list_display=('car_name','brand','model','price_per_day','car_thumbnail','description','pickup_location','dropoff_location','offer','fine_per_day','discount','is_available','owner_name','controle','seated_capacity')