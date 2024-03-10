from django.contrib import admin
from .models import User, UserCodeVerification
# Register your models here.
admin.site.register([User, UserCodeVerification])