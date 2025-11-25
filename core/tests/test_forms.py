"""
Tests for forms in the core app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.forms import AppointmentForm, DoseForm, UserProfileForm, CustomUserCreationForm
from core.models import Vaccine, Branch, Appointment

User = get_user_model()


class CustomUserCreationFormTest(TestCase):
    """Test the custom user creation form"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'SecureP@ssw0rd!',
        }
        form = CustomUserCreationForm(data=data)
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug output
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test form with mismatched passwords"""
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'DifferentP@ss123!',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_duplicate_username(self):
        """Test form with duplicate username"""
        User.objects.create_user(username='existinguser', password='testpass123')
        data = {
            'username': 'existinguser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'SecureP@ssw0rd!',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())


class AppointmentFormTest(TestCase):
    """Test the appointment form"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
    
    def test_valid_form(self):
        """Test form with valid data"""
        future_datetime = timezone.now() + timedelta(days=7)
        data = {
            'vaccine': self.vaccine.id,
            'branch': self.branch.id,
            'datetime': future_datetime,
        }
        form = AppointmentForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_past_datetime(self):
        """Test form with past datetime"""
        past_datetime = timezone.now() - timedelta(days=7)
        data = {
            'vaccine': self.vaccine.id,
            'branch': self.branch.id,
            'datetime': past_datetime,
        }
        form = AppointmentForm(data=data)
        # This depends on whether you have validation for past dates
        # If you add this validation, update the assertion
        self.assertTrue(form.is_valid())  # or assertFalse if you add validation
    
    def test_missing_required_fields(self):
        """Test form with missing required fields"""
        data = {
            'vaccine': self.vaccine.id,
            # missing branch and datetime
        }
        form = AppointmentForm(data=data)
        self.assertFalse(form.is_valid())


class DoseFormTest(TestCase):
    """Test the dose form"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
    
    def test_valid_form(self):
        """Test form with valid data"""
        data = {
            'vaccine': self.vaccine.id,
            'date_administered': timezone.now().date(),
        }
        form = DoseForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_future_date(self):
        """Test form with future date"""
        future_date = (timezone.now() + timedelta(days=7)).date()
        data = {
            'vaccine': self.vaccine.id,
            'date_administered': future_date,
        }
        form = DoseForm(data=data, user=self.user)
        # This depends on whether you have validation for future dates
        # If you add this validation, update the assertion
        self.assertTrue(form.is_valid())  # or assertFalse if you add validation
    
    def test_missing_required_fields(self):
        """Test form with missing required fields"""
        data = {
            'vaccine': self.vaccine.id,
            # missing date_administered
        }
        form = DoseForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())


class UserProfileFormTest(TestCase):
    """Test the user profile form"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_form(self):
        """Test form with valid data"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'username': 'testuser',
        }
        form = UserProfileForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email(self):
        """Test form with invalid email"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',
            'username': 'testuser',
        }
        form = UserProfileForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
    
    def test_duplicate_email(self):
        """Test form with duplicate email"""
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'other@example.com',
            'username': 'testuser',
        }
        form = UserProfileForm(data=data, instance=self.user)
        # Form validates unique emails, so this should be invalid
        self.assertFalse(form.is_valid())
