from django.contrib import admin
from .models import User,UserBlackListedToken




admin.site.register(User)
admin.site.register(UserBlackListedToken)