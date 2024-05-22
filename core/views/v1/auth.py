from django.core import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .utils import get_tokens_for_user
from django.contrib.auth.models import User
from core.models import AdminProfile
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        admin_profile = get_object_or_404(AdminProfile, email=email)
        if not admin_profile.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect Credentials")
        return Response(get_tokens_for_user(admin_profile.admin), status=status.HTTP_200_OK)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed("Incorrect Credentials")
    
@api_view(['GET'])
def admin_verify_email(request):
    uid = request.query_params.get('uid')
    if uid:
        id = smart_str(urlsafe_base64_decode(uid))
        admin = get_object_or_404(AdminProfile, id)
        admin.is_active = True
        admin.save(update_fields=['is_active'])
        return Response({'message': 'Admin account activated successfully!'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)
