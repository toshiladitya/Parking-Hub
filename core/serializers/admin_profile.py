from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models import AdminProfile
from django.contrib.auth.models import User
import re
from uuid import uuid4


class AdminProfileSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = (
            'id',
            'uuid',
            'full_name',
            'role',
            'phone',
            'country_code',
            'email',
            'intro',
            'gender'
        )

class AdminProfileSerializer(serializers.ModelSerializer):
    admins_ids = serializers.PrimaryKeyRelatedField(queryset=AdminProfile.objects.filter(
        role=AdminProfile.ADMIN), write_only=True, required=False, many=True, allow_null=True)
    admins = AdminProfileSearchSerializer(read_only=True, many=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminProfile
        fields = (
            'id',
            'uuid',
            'full_name',
            'role',
            'phone',
            'password',
            'confirm_password',
            'country_code',
            'email',
            'intro',
            'gender',
            'admins_ids',
            'super_admin',
            'admins',
        )
        read_only_fields = ('updated_at', 'created_at')

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            password = data['password']
            confirm_password = data['confirm_password']
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
                raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one digit, one special symbol, and be at least 8 characters long.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        admins = validated_data.pop('admins_ids', [])
        user = User.objects.create(username=str(uuid4()))
        instance = AdminProfile(**validated_data, admin=user)
        instance.save()
        if admins is not None:
            instance.admins.set(admins)
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        admins = validated_data.pop('admins_ids', [])
        instance = super().update(instance, validated_data)
        if admins is not None:
            instance.admins.set(admins)
        return instance
    
class AdminProfileChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AdminProfileChangePasswordSerializer, self).__init__(*args, **kwargs)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError("Please enter the correct password.")
        return value
    
    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", new_password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one digit, one special symbol, and be at least 8 characters long.")
        return data
    
class AdminProfileForgetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", new_password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one digit, one special symbol, and be at least 8 characters long.")
        return data
        
    
