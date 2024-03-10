from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import uuid
import random
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

# Types of users
REGULAR, SUPPORT, ADMIN = ('regular', 'support', 'admin')

# Auth steps
NEW, CODE_VERIFIED, DONE, IMAGE_STEP = ('new', 'code_verified', 'done', 'image_step')

# Users register type
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')

class User(BaseModel,AbstractUser):

    # Types of users
    USER_ROLES = (
        (REGULAR, REGULAR),
        (SUPPORT, SUPPORT),
        (ADMIN, ADMIN),
    )

    # Auth steps
    AUTH_STEP_CHOICES = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (IMAGE_STEP, IMAGE_STEP),
    )

    # Users register type
    AUTH_TYPES_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL),
    )

    auth_type = models.CharField(max_length=20, choices=AUTH_TYPES_CHOICES)
    auth_status = models.CharField(max_length=20, choices=AUTH_STEP_CHOICES, default=NEW)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default=REGULAR)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    email = models.CharField(max_length=130, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def check_username(self):
        if not self.username:
            temp_username = f"{self.first_name}-{str(uuid.uuid4()).split('-')[-1]}"
            # temp_username = f"user-{str(uuid.uuid4()).split('-')[-1]}"
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def check_passwrd(self):
        if not self.password:
            temp_password = f"password{str(uuid.uuid4()).split('-')[-1]}"
            self.password = temp_password

    def check_hash_password(self):
        if not self.password.startswith("pbkdf2_"):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.check_username()
        self.check_passwrd()
        self.check_hash_password()

        super(User,self).save(*args, **kwargs)


class UserCodeVerification(BaseModel):
    AUTH_TYPES_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL),
    )

    auth_type = models.CharField(max_length=20, choices=AUTH_TYPES_CHOICES)
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)
    expire_time = models.DateTimeField(null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='confirmation_codes')


    def __str__(self):
        return f"{self.user.username} {self.code}"
    

    def save(self, *args, **kwargs):
        if self.auth_type == VIA_EMAIL:
            self.expire_time = datetime.now() + datetime.timedelta(minutes=5)
        
        elif self.auth_type == VIA_PHONE:
           self.expire_time = datetime.now() + datetime.timedelta(minutes=2)

        super(UserCodeVerification,self).save(*args, **kwargs)