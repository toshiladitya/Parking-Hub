from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import AdminProfile
from core.serializers import AdminProfileSerializer, AdminProfileChangePasswordSerializer
from rest_framework.decorators import action, api_view, permission_classes
from core.permissions import BaseAdminPermission
from core.pagination import CustomPageNumberPagination
from django.shortcuts import get_object_or_404

class AdminProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [BaseAdminPermission]
    serializer_class = AdminProfileSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return AdminProfile.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'change_password':
            return AdminProfileChangePasswordSerializer
        return AdminProfileSerializer
    
    def list(self, request, *args):
        queryset = self.get_queryset()
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args):
        admin_profile = self.get_serializer(data=request.data)
        if admin_profile.is_valid():
            admin_profile.save()
            return Response(admin_profile.data, status=status.HTTP_200_OK)
        else:
            return Response({"errors": admin_profile.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def retrieve(self, request, pk=None, *args):
        queryset = self.get_queryset()
        admin = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        admin = get_object_or_404(AdminProfile, pk=pk)
        serializer = self.get_serializer(data=request.data, user=admin)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            admin.set_password(new_password)
            admin.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

        
    
        

