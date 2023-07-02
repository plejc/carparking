from rest_framework.authentication import SessionAuthentication
from time import time
from rest_framework import status
from datetime import datetime, timedelta
import datetime
from rest_framework.exceptions import APIException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from fastapi import Depends,HTTPException, status
from users.models import UserBlackListedToken,User
from jose import jwt,JWTError
from rest_framework.permissions import BasePermission





def validate_backend_user(data):
    if not data.get('first_name') or str(data.get('first_name')).isspace():
        return{
            'status': False,
            'message': "First name is mandatory field",
            'code': status.HTTP_400_BAD_REQUEST
        }
    else:
        first_name = str(data.get('first_name')).strip()
        if len(first_name) > 50:
            return {
                'status': False,
                'message': "First name can't be more than 50 characters",
                'code': status.HTTP_400_BAD_REQUEST
            }

    if data.get('middle_name') and not str(data.get('middle_name')).isspace():
        middle_name = str(data.get('middle_name')).strip()
        if len(middle_name) > 50:
            return {
                'status': False,
                'message':"Middle name can't be more than 50 characters",
                'code': status.HTTP_400_BAD_REQUEST
            }
        check_numeric = any(chr.isdigit() for chr in middle_name)
        if check_numeric:
            return {
                'status': False,
                'message':"Middle name can't be numeric",
                'code': status.HTTP_400_BAD_REQUEST
            }
    if data.get('last_name') and not str(data.get('last_name')).isspace():
        last_name = str(data.get('last_name')).strip()
        if len(last_name) > 50:
            return {
                'status': False,
                'message': "Last name can't be more than 50 characters",
                'code': status.HTTP_400_BAD_REQUEST
            }
        check_numeric = any(chr.isdigit() for chr in last_name)
        if check_numeric:
            return {
                'status': False,
                'message':"Last name ca't be numeric",
                'code': status.HTTP_400_BAD_REQUEST
            }
    if not data.get('email') or data.get('email').isspace():
        return {
            'status': False,
            'message': "Please provide a valid email",
            'code': status.HTTP_400_BAD_REQUEST
        }
    if User.objects.filter(email=data.get('email').lower().strip()).exists():
            return {
                'status': False,
                'message': "Email can't be duplicate",
                'code': status.HTTP_400_BAD_REQUEST
            }
    if data.get('phone') and not str(data.get('phone')).isspace():
        phone = str(data.get('phone')).strip()
        if not phone.isdigit():
            return {
                'status': False,
                'message': "Invalid phone number",
                'code': status.HTTP_400_BAD_REQUEST
            }
        if not len(phone) == 10:
            return {
                'status': False,
                'message': "Phone can't be more than 10 digits",
                'code': status.HTTP_400_BAD_REQUEST
            }
        if User.objects.filter(phone=phone).exists():
            return {
                'status': False,
                'message': "Phone already exists",
                'code': status.HTTP_400_BAD_REQUEST
            }
    else:
        try:
            data.pop("phone")
        except KeyError:
            pass
    return {
    'status': True,
    'message': "Data validated successfully",
    "data": data
    }

class ExemptCsrf(SessionAuthentication):

    '''
    class for exempting csrf token
    '''

    def enforce_csrf(self, request):

        return




def create_access_token(data: dict):
    '''
    utility function for creating access token at the time of login
    '''
    to_encode = data.copy()
    expiry_minutes = 30
    expire = datetime.datetime.now() + timedelta(minutes=int(expiry_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "ldjsdnsdoidJNIDNIDJDI)@(W$()(@#$))")
    return encoded_jwt


class NeedLogin(APIException):
    '''
    custom execption class for raising error in caseo of unauthorized access
    '''
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'status': False,
                      'message':"Unknow user trying to access",
                      'status_code': status.HTTP_401_UNAUTHORIZED
                      }
    


def verify_token(token: str, credentials_exception):
    '''
    utility function for verifying token (supplied by the user at the time of login)
    '''
    try:
        payload = jwt.decode(token, "ldjsdnsdoidJNIDNIDJDI)@(W$()(@#$))",
                             algorithms="HS256")
        unique_identifier = payload.get("sub")
        print("The unique identified =====", unique_identifier)
        if unique_identifier is None:
            raise credentials_exception
        return {
            "status": True,
            "message": "Authenticated successful",
            "data": unique_identifier
        }
    except JWTError:
        return {
            "status": False,
            "message": "Uanauthorized access",
            "status_code": status.HTTP_401_UNAUTHORIZED
        }
    
def get_current_user(data: str = Depends(oauth2_scheme)):
    '''
    utility function for returning the current user based on token
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate",
        headers={"www-Authenticate", "Bearer"}
    )
    return verify_token(data, credentials_exception)



class IsTokenValidForUser(BasePermission):
    '''
    permission class to check token is valid or not
    Note : This permission class is only for backend user, not members (frontend user)
    '''
    def has_permission(self, request, view):
        is_allowed_user = True
        print("ramaam =========")
        try:
            token = request.META['HTTP_BEARER']
            current_user = get_current_user(token)
            # current_user = user
            user = User.objects.filter(uid=current_user['data']).last()
            if not user:
                raise NeedLogin()
        except Exception:
            raise NeedLogin()
        try:
            is_blacklisted = UserBlackListedToken.objects.get(
                user=user, token=token)
            if is_blacklisted:
                raise NeedLogin()
        except UserBlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user