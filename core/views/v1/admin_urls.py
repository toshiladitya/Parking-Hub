from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
from django.urls.conf import path
from core.views.v1.admins import admin_profile

router = DefaultRouter()
router.register(r'admin_profiles', admin_profile.AdminProfileViewSet, basename='admin_profile')

urlpatterns = router.urls