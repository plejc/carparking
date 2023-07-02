from django.db import models
from uuid import uuid4
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,BaseUserManager



class UserManager(BaseUserManager):
    '''
    custom fucnton for creating superuser.

    '''
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    '''
    models to store the basic impofrmation of user.

    '''
    uid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField("first name", blank=False, null=False, max_length=50)
    middle_name = models.CharField("middle name", blank=True, null=True,max_length=50)
    last_name = models.CharField("last name", blank=True, null=True, max_length=50)
    email = models.EmailField("email", null=False, blank=False,unique=True, error_messages={"unique":"An account with this email already exists:"})
    phone = models.BigIntegerField("phone", null=True, blank=True)
    USERNAME_FIELD = "email"
    objects = UserManager()
    full_name = models.CharField("full name", blank=True, null=True,max_length=150)
    updated_at = models.DateTimeField("updated at", blank=True, null=True)
    created_at = models.DateTimeField("created at", blank=True, null=True)
    is_staff = models.BooleanField("is staff", default=False)
    is_active = models.BooleanField("is active", default=True)

    def save(self, *args, **kwargs):
        if self.last_name and self.middle_name:
            self.full_name = self.first_name.title() + " " + self.middle_name.title()+\
            " " + self.last_name.title()
        elif self.middle_name and not self.last_name:
            self.full_name = self.first_name.title() + " " + self.middle_name.title()
        elif self.last_name and not self.middle_name:
            self.full_name = self.first_name.title() + " " + self.last_name.title()
        else:
            self.full_name = self.first_name.title()
        self.email = self.email.lower()
        self.email = self.email.strip()
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = "BackendUser"



class UserBlackListedToken(models.Model):
    '''
    models to store the blacklisted login token for the user (only backend user)
    '''
    uid = models.UUIDField(primary_key=True,default=uuid4, editable=False)
    token = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('token', 'user')
        db_table = "BackEndUserBlackListedToken"