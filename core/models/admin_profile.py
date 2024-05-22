from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .audit_coulmn import AuditColumns
from django.contrib.auth.hashers import make_password, check_password as django_check_password, identify_hasher

def validate_phone(value):
    if value and len(value) == 10:
        return value
    else:
        raise ValidationError("Please enter a valid 10 digit phone number.")


class AdminProfile(AuditColumns):
    class Meta:
        app_label = "core"
        db_table = "admin_profile"

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    SUB_ADMIN = 'sub_admin'


    GENDER_CHOICE = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]

    ROLE_CHOICE = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (SUB_ADMIN, 'Sub Admin')

    ]

    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50)
    role = models.CharField(max_length=30, choices=ROLE_CHOICE)
    phone = models.CharField(max_length=10, unique=True, validators=[validate_phone])
    password = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5, default='+91')
    email = models.EmailField(max_length=255, unique=True)
    intro = models.TextField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICE)
    super_admin = models.BooleanField(default=False)
    admins = models.ManyToManyField('AdminProfile', null=True, blank=True, related_name='admins_profile_admins')
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.full_name

    @property
    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN

    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_sub_admin(self):
        return self.role == self.SUB_ADMIN
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



