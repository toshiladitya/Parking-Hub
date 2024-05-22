from django.core import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .utils import get_tokens_for_user
from django.contrib.auth.models import User
from core.models import AdminProfile
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from core.serializers import AdminProfileSerializer
from .utils import Utils
import re
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@api_view(['POST'])
def login(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        admin_profile = get_object_or_404(AdminProfile, email=email)
        if not admin_profile.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect Credentials")
        return Response(get_tokens_for_user(admin_profile.admin), status=status.HTTP_200_OK)
    except:
        return Response({'error':"Invalid credentials"})
    
@api_view(['GET'])
def admin_verify_email(request):
    uid = request.query_params.get('uid')
    if uid:
        id = smart_str(urlsafe_base64_decode(uid))
        admin = get_object_or_404(AdminProfile, id=id)
        admin.is_active = True
        admin.save(update_fields=['is_active'])
        return Response({'message': 'Admin account activated successfully!'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forget_password(request):
    email = request.data.get('email', None)
    if not email:
        return Response({"email": "Email is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user = get_object_or_404(AdminProfile, email=email)
    if user:
        uid = urlsafe_base64_encode(force_bytes(user.id))
        link = f'http://127.0.0.1:8000/api/v1/reset_password/{uid}/'
        text_content = f'Click the following link to reset your password: {link}'
        html_content = f'<p>Click the following link to reset your password:</p><p><a href="{link}">Reset Password</a></p>'
        data = {
            'email_subject': 'Reset Your Password',
            'text_content': text_content,
            'html_content': html_content,
            'to_email': user.email
        }
        Utils.send_email(data)
        return Response({"success": "Reset Password Link has been shared to the provided email address."}, status=status.HTTP_200_OK)
    return Response({"error": "User not found."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def reset_password(request, pk, *args, **kwargs): 
    pk = smart_str(urlsafe_base64_decode(pk))
    new_password = request.data.get('new_password', None)
    confirm_passwword = request.data.get('confirm_password', None)
    if not new_password and not confirm_passwword:
        return Response({"error": "Password is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if new_password == confirm_passwword:
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", new_password):
            user = get_object_or_404(AdminProfile, pk=pk)
            user.set_password(new_password)
            user.save()
            return Response({"success": "Passwrd has been successfully updated."}, status=status.HTTP_200_OK)
        return Response({"error": "Password must contain at least one lowercase letter, one uppercase letter, one digit, one special symbol, and be at least 8 characters long status."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"error": "Password do not match"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            
        
   