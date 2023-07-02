from django.contrib import admin
from .models import AddressArea,ParkingSpot, Radius,RequestedParking




admin.site.register(AddressArea)
admin.site.register(ParkingSpot)
admin.site.register(Radius)
admin.site.register(RequestedParking)