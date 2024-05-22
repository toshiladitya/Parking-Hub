from django.urls import path, include

urlpatterns = [
    path("", include('core.views.v1.admin_urls')),
    # path("users/", include('core.views.v1.user_urls')),
]