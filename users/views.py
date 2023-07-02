from django.shortcuts import render
from .models import User, UserBlackListedToken
from .serializers import LoginSerializer,UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView,ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework.viewsets import ViewSet,ViewSetMixin,ModelViewSet,ReadOnlyModelViewSet,NoReverseMatch,views,GenericViewSet
from rest_framework.validators import ValidationError,UniqueValidator,DataError
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login
from utils.constants import ExemptCsrf, create_access_token,IsTokenValidForUser,get_current_user
from rest_framework import generics





class LoginView(generics.GenericAPIView):
    '''
    api for login 
    headers: not required.
    auery-parameter:Not required
    '''
    authentication_classes = (ExemptCsrf,)
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        params = request.data
        serializer = self.serializer_class()
        validated_data = serializer.validate(params)
        if not authenticate(email=validated_data.get('email').lower().strip(), password=validated_data.get('password').strip()):
            return Response({
                "status": False,
                "message": "Provide a valid credentials",
                'code': status.HTTP_400_BAD_REQUEST,
                'status_code': status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)
        data = {}
        user = validated_data.get('user')
        try:
            user = User.objects.filter(email = user).last()
        except User.DoesNotExist:
            return Response({
                "status":False,
                "message":"User does not exists",
                "status_code":status.HTTP_400_BAD_REQUEST
            })
        user_uid = user.uid
        data = {}
        data['sub'] = str(user_uid)
        token = create_access_token(data)
        return Response({
            'status': True,
            "message":"Login successfully",
            "status_code":status.HTTP_200_OK,
            "token":token,
            "user_id":user_uid
        })



class LogOutView(APIView):
    '''
    Api for logout
    Headers : Bearer(required)
    Query-parameter : Not required
    '''
    authentication_classes = (ExemptCsrf,)
    permission_classes = (IsTokenValidForUser,)

    def post(self, request, *args, **kwargs):
        token = request.META['HTTP_BEARER']
        check_authentication = get_current_user(token)
        user = User.objects.get(id=check_authentication['data'])
        UserBlackListedToken.objects.update_or_create(token=token, user=user)
        return Response({
            "status": True,
            "message": "Logout successfully",
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

#register new user


class SignUpView(GenericAPIView):
    '''
    onboarding new user into the accounts.

    '''
    authentication_classes = (ExemptCsrf,)
    serializer_class = UserRegistrationSerializer

    def post(self, request,*args,**kwargs):
        params = request.data
        serializer = self.serializer_class()
        validated_data = serializer.validate(params)
        # print("THE validated data is the following ===========", validated_data)
        onboard_user = serializer.create(validated_data)
        # print("THE onboard user with new credentials ==========", onboard_user)
        return Response({
            "status":True,
            "message":"User created successfully",
            "status_code":status.HTTP_201_CREATED
        })