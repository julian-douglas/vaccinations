from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import (
    UserViewSet, VaccineViewSet, BranchViewSet, 
    AppointmentViewSet, DoseViewSet, api_health
)

# API router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vaccines', VaccineViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'doses', DoseViewSet)

urlpatterns = [
    # Web interface URLs
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('appointments/add/', views.appointment_create, name='appointment_add'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('doses/', views.dose_list, name='dose_list'),
    path('doses/add/', views.dose_create, name='dose_add'),
    path('doses/<int:pk>/delete/', views.dose_delete, name='dose_delete'),
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/<int:pk>/', views.branch_detail, name='branch_detail'), 
    
    # API URLs
    path('api/health/', api_health, name='api_health'),
    path('api/', include(router.urls)),
]
