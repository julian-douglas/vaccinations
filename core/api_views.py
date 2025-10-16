from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Vaccine, Branch, Appointment, Dose
from .serializers import (
    UserSerializer, UserCreateSerializer, VaccineSerializer, 
    BranchSerializer, AppointmentSerializer, AppointmentCreateSerializer,
    DoseSerializer, DoseCreateSerializer
)

User = get_user_model()


@api_view(['GET'])
def api_health(request):
    """Health check endpoint"""
    return Response({"status": "ok"})


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations
    """
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class VaccineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Vaccine read operations
    """
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Branch read operations
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations
    """
    queryset = Appointment.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentCreateSerializer
        return AppointmentSerializer


class DoseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Dose CRUD operations
    """
    queryset = Dose.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DoseCreateSerializer
        return DoseSerializer
