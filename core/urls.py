from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('appointments/add/', views.appointment_create, name='appointment_add'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('doses/', views.dose_list, name='dose_list'),
    path('doses/add/', views.dose_create, name='dose_add'),
    path('doses/<int:pk>/delete/', views.dose_delete, name='dose_delete'),
    path('branches/', views.branch_list, name='branch_list'),
]
