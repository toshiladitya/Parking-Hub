from django.urls import path, include

urlpatterns = [
    path("v1/", include('core.views.v1.urls')),
]
