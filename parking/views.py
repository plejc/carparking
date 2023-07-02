from django.shortcuts import render
from .serializers import ParkingSpotSerializer, RequestedParkingSerializer
from .models import ParkingSpot,AddressArea,Radius,RequestedParking
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from utils.constants import ExemptCsrf
from utils.messages import messages_dict
from utils.status_code import status_dict
from utils.constants import IsTokenValidForUser,get_current_user



class ParkingListView(GenericAPIView):
    '''
    api to get all the list of parking spot available ....

    '''
    authentication_classes = (ExemptCsrf,)
    permission_classes = (IsTokenValidForUser,)
    serializer_class = ParkingSpotSerializer


    def post(self,request, *args, **kwargs):
        params = request.data

        if not params.get("address_uid"):
            return Response({
                "status":False,
                "message":messages_dict['select_location_for_seraching'],
                "code":status.HTTP_400_BAD_REQUEST,
                "status_code":status_dict['select_location_code']
            })
        if not params.get("radius_uid"):
            return Response({
                "status":False,
                "message":messages_dict['select_range_radius'],
                "code":status.HTTP_400_BAD_REQUEST,
                "status_code":status_dict['select_radius_code']
            })
        # address_instance = AddressArea.objects.filter(address_name=params.get("address_name")).last()
        # address_uid = address_instance.uid
        # radius_instance = Radius.objects.filter(range = params.get("radius_range")).last()
        # print("the address uid ====", address_uid, radius_instance)
        
        instance = ParkingSpot.objects.filter(address = params.get("address_uid"), radius = params.get("radius_uid"),is_reserved=False)
        response = self.serializer_class(instance, many=True)
        return Response({
            "status":True,
            "message":messages_dict['parking_list_message'],
            "code":status.HTTP_200_OK,
            "status_code":status_dict['parking_spot_list_code'],
            "data":response.data

        })
        

class RequestParkingView(GenericAPIView):
    '''
    api for requesting a parking spot by the users for a number of hours...

    '''
    authentication_classes = (ExemptCsrf,)
    permission_classes = (IsTokenValidForUser,)
    serializer_class = RequestedParkingSerializer

    def post(self, request, *args, **kwargs):
        params = request.data
        token = request.META['HTTP_BEARER']
        login_user_authentication_data = get_current_user(token)
        serializer = self.serializer_class()
        validated_data = serializer.validate(data=params)
        validated_data['user'] = login_user_authentication_data['data']
        print("the validated data ====", validated_data)
        response = serializer.create(validated_data=validated_data)
        #object details
        instance = RequestedParking.objects.filter(uid = response).last()
        instance_response = self.serializer_class(instance)

        #
        return Response({
            "status":True,
            "message":messages_dict['parking_spot_booked_message'],
            "code":status.HTTP_201_CREATED,
            "status_code":status_dict['parking_spot_booked_code'],
            "response":instance_response.data
        })
    
#reservedlist by users
class BookedParkingView(GenericAPIView):

    '''
        all booked parking spot by the users.

    '''
    authentication_classes = (ExemptCsrf,)
    permission_classes = (IsTokenValidForUser,)
    serializer_class = RequestedParkingSerializer

    def post(self, request,*args,**kwargs):
        params = request.data
        token = request.META['HTTP_BEARER']
        login_user_authentication_data = get_current_user(token)
        print("the coming login user athentication is the following =====", login_user_authentication_data)
        response = RequestedParking.objects.filter(user = login_user_authentication_data['data'])
        response_data = self.serializer_class(response, many=True)
        print("the response ===", response)
        return Response({
            "status":True,
            "message":messages_dict['users_reserved_parking_message'],
            "code":status.HTTP_200_OK,
            "status_code":status_dict['users_reserved_parking_code'],
            "data":response_data.data
        })
#reserved parking details view
class BookedParkingDetailView(GenericAPIView):

    '''
        Detail of booked parking spot by the user.

    '''
    authentication_classes = (ExemptCsrf,)
    permission_classes = (IsTokenValidForUser,)
    serializer_class = RequestedParkingSerializer

    def post(self, request,*args,**kwargs):
        params = request.data
        token = request.META['HTTP_BEARER']
        login_user_authentication_data = get_current_user(token)
        if not params.get("parking_uid"):
            return Response({
                "status":False,
                "message":messages_dict['provide_parking_uid_message'],
                "code":status.HTTP_400_BAD_REQUEST,
                "status_code":status_dict['provide_parking_uid_code']
            })
        print("the coming login user athentication is the following =====", login_user_authentication_data)
        response = RequestedParking.objects.filter(user = login_user_authentication_data['data'])
        response_data = self.serializer_class(response, many=True)
        print("the response ===", response)
        return Response({
            "status":True,
            "message":messages_dict['users_reserved_parking_message'],
            "code":status.HTTP_200_OK,
            "status_code":status_dict['users_reserved_parking_code'],
            "data":response_data.data
        })
    