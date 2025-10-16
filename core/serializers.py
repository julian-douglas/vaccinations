from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vaccine, Branch, Appointment, Dose

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    status_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'postcode', 'phone', 'email', 'opening_hours', 'image_url', 'status_info']
    
    def get_status_info(self, obj):
        return obj.status_info()


class AppointmentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    vaccine_details = VaccineSerializer(source='vaccine', read_only=True)
    branch_details = BranchSerializer(source='branch', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['user', 'vaccine', 'branch', 'datetime', 'notes']


class DoseSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    vaccine_details = VaccineSerializer(source='vaccine', read_only=True)
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    
    class Meta:
        model = Dose
        fields = '__all__'


class DoseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dose
        fields = ['vaccine', 'user', 'appointment', 'date_administered', 'dose_number']
