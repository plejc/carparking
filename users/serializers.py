from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField, ValidationError
from .models import User
from rest_framework import status
from utils.constants import validate_backend_user


class LoginSerializer(Serializer):
    '''
    serializer for login (only for backend users, not for anyother)

    '''
    email = EmailField(required=True)
    password = CharField(required=True)

    def validate(self, data):
        if not(data.get("email").strip()):
            raise ValidationError({
                "status":False,
                "message":"Please provide a valid email",
                "status_code":status.HTTP_400_BAD_REQUEST
            })
        if not data.get("password") or data.get("password").isspace():
            raise ValidationError({
                'status': False,
                'message':"Provide a valid password",
                'code': status.HTTP_400_BAD_REQUEST
            })
        try:
            user = User.objects.filter(email=data.get('email').lower().strip()).last()
            if not user:
                raise ValidationError({
                    'status': False,
                    'message': "User is trying to login with unknonw credentials",
                    'code': status.HTTP_400_BAD_REQUEST
                    })
        except User.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': "No record found",
                'code': status.HTTP_400_BAD_REQUEST
            })
        data.update(user=user)
        return data
    


class UserRegistrationSerializer(ModelSerializer):

    '''
    serializer for user registration.

    '''
    class Meta:
        model = User
        fields = ['uid', 'first_name', 'middle_name',
        'last_name', 'email', 'phone']

    def validate(self, data):
        validation_result = validate_backend_user(data)
        if not validation_result['status']:
            raise ValidationError({
            'status': False,
            'message': validation_result['message'],
            'code': validation_result['code']
            })
        return validation_result['data']

    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
        except Exception:
            raise ValidationError({
                "status":False,
                "message":"User can't be created",
                "code":status.HTTP_400_BAD_REQUEST
            })
        user.set_password(validated_data['password'])
        user.save()
        # Token.objects.create(user=user)
        return user