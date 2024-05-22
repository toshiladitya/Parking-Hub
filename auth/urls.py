from django.urls import path, include
from auth.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admins/login/', login),
    path('admin_verify_email/', admin_verify_email, name='admin_verify_email'),
    path('admin/forget_password/', forget_password, name="forget_password"),
    path('admin/reset_password/<str:pk>/', reset_password, name="reset_password"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]