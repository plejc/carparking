from django.db import models
from uuid import uuid4
from users.models import User


class AddressArea(models.Model):

    '''model to store address and area for a location.'''
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    address_name = models.CharField(max_length=50, blank=False, null=False)
    range_radius = models.IntegerField()

    def __str__(self) :
        return self.address_name
    
class Radius(models.Model):

    '''
    
    models to store the range of radius.

    '''
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    range = models.IntegerField()

class ParkingSpot(models.Model):

    ''' models to store parking spot in a specific area,
        there can be many parking spot in an address, there will be a foreign type
        relationship with addressarea.
    '''
    uid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    lat = models.FloatField()
    long = models.FloatField()
    address = models.ForeignKey(AddressArea, on_delete=models.DO_NOTHING, related_name='%(class)s_address_id')
    radius = models.ForeignKey(Radius,on_delete=models.DO_NOTHING, blank=True, null=True)
    hourly_charge = models.FloatField(blank=True, null=True)
    is_reserved = models.BooleanField(default=False)
    

class RequestedParking(models.Model):
    '''
    models to store all the requested parking spot by the users.

    '''
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_booked_by')
    booked_on = models.DateTimeField(auto_now_add=True)
    hours_for = models.IntegerField()
    payable_amount = models.FloatField(blank=True, null=True)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.DO_NOTHING, related_name='%(class)s_parking_spot')


