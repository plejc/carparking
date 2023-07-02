from rest_framework.serializers import ModelSerializer,ValidationError
from .models import AddressArea, ParkingSpot,Radius,RequestedParking
from users.models import User
from rest_framework import status




class RadiusSerializer(ModelSerializer):

    ''' serializer for stoing radius ==='''

    class Meta:
        model = Radius

        fields = ['uid','range']

class AddressSerializer(ModelSerializer):
    '''
    serializers for storing .....address

    '''
    class Meta:
        model = AddressArea

        fields = ['uid', 'address_name']

class ParkingSpotSerializer(ModelSerializer):

    '''serializer for getting parkingspot object...'''
    address = AddressSerializer()
    radius = RadiusSerializer()
    class Meta:
        model = ParkingSpot
        fields = ['uid','lat', 'long', 'address','radius','is_reserved']

class RequestedParkingSerializer(ModelSerializer):
    '''
    serializer to store requested parking for a specific user.

    '''
    class Meta:
        model = RequestedParking
        fields = ['uid','user','booked_on','hours_for','payable_amount','parking_spot']
    
    def validate(self, data):
        # print("the coming data is the following =====", data)
        return data
    def create(self, validated_data):
        # print("the coming validated data for create view is the following =====user", validated_data['user'])
        try:
            parking_spot_instance = ParkingSpot.objects.filter(uid = validated_data.get('parking_spot')).last()
            if not parking_spot_instance:
                raise ValidationError({
                    "status":False,
                    "message":"Parking psot doesn't exist anymore",
                    "code":status.HTTP_400_BAD_REQUEST,
                    "status_code":40005
                })
                
        except Exception:
            raise ValidationError({
                    "status":False,
                    "message":"Parking psot doesn't exist anymore",
                    "code":status.HTTP_400_BAD_REQUEST,
                    "status_code":40005
                })
        # print("the coming parking spot instance =====", parking_spot_instance.is_reserved)
        parking_spot_instance.is_reserved = True
        parking_spot_instance.save()
        validated_data['payable_amount'] = parking_spot_instance.hourly_charge*validated_data.get("hours_for")
        # print("the validated data ====", validated_data)
        validated_data.update(parking_spot=parking_spot_instance)
        try:
            user_instance = User.objects.filter(uid = validated_data['user']).last()
            if not user_instance:
                raise ValidationError({
                    "status":False,
                    "message":"User doesn't exists",
                    "code":status.HTTP_400_BAD_REQUEST
                })
        except User.DoesNotExist:
            raise ValidationError({
                "status":False,
                "message":"User record doesn't found",
                "code":status.HTTP_400_BAD_REQUEST
            })
        validated_data.update(user=user_instance)
        print("The validated data =======final==", validated_data)
        try:
            parking_spot = RequestedParking.objects.create(**validated_data)
        except Exception:
            raise ValidationError({
                "status":False,
                "message":"Freinds can't be created",
                "code":status.HTTP_400_BAD_REQUEST
            })        
        return parking_spot.uid