"""
Tests for views in the core app
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import Vaccine, Branch, Appointment, Dose

User = get_user_model()


class HomeViewTest(TestCase):
    """Test the home view"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
    
    def test_home_view_anonymous(self):
        """Test home view for anonymous users"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_view_authenticated(self):
        """Test home view for authenticated users"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)


class SignupViewTest(TestCase):
    """Test the signup view"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')
    
    def test_signup_view_get(self):
        """Test GET request to signup"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
    
    def test_signup_view_post_valid(self):
        """Test POST request with valid data"""
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'SecureP@ssw0rd!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_signup_view_post_invalid(self):
        """Test POST request with invalid data"""
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'pass',
            'password2': 'different',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_signup_redirect_authenticated(self):
        """Test that authenticated users are redirected from signup"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class AppointmentListViewTest(TestCase):
    """Test the appointment list view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
        self.url = reverse('appointment_list')
    
    def test_appointment_list_login_required(self):
        """Test that login is required"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_appointment_list_view(self):
        """Test appointment list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_list.html')
    
    def test_appointment_list_split_upcoming_past(self):
        """Test that appointments are split into upcoming and past"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create upcoming appointment
        upcoming = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=7)
        )
        
        # Create past appointment
        past = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() - timedelta(days=7)
        )
        
        response = self.client.get(self.url)
        self.assertIn(upcoming, response.context['upcoming_appointments'])
        self.assertIn(past, response.context['past_appointments'])


class AppointmentCreateViewTest(TestCase):
    """Test the appointment create view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
        self.url = reverse('appointment_add')
    
    def test_appointment_create_login_required(self):
        """Test that login is required"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_appointment_create_get(self):
        """Test GET request to create appointment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_form.html')
    
    def test_appointment_create_post_valid(self):
        """Test POST request with valid data"""
        self.client.login(username='testuser', password='testpass123')
        future_datetime = (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        data = {
            'vaccine': self.vaccine.id,
            'branch': self.branch.id,
            'datetime': future_datetime,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Appointment.objects.filter(user=self.user).exists())


class AppointmentDeleteViewTest(TestCase):
    """Test the appointment delete view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
        self.appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=7)
        )
        self.url = reverse('appointment_delete', args=[self.appointment.id])
    
    def test_appointment_delete_login_required(self):
        """Test that login is required"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_appointment_delete_post(self):
        """Test deleting an appointment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())
    
    def test_appointment_delete_wrong_user(self):
        """Test that users can't delete other users' appointments"""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


class DoseCreateViewTest(TestCase):
    """Test the dose create view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.url = reverse('dose_add')
    
    def test_dose_create_login_required(self):
        """Test that login is required"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_dose_create_get(self):
        """Test GET request to create dose"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dose_form.html')
    
    def test_dose_create_post_valid(self):
        """Test POST request with valid data"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'vaccine': self.vaccine.id,
            'date_administered': timezone.now().date().strftime('%Y-%m-%d'),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dose.objects.filter(user=self.user).exists())


class DoseLinkAppointmentViewTest(TestCase):
    """Test linking appointments to doses"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
        
        # Create a past appointment
        self.appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() - timedelta(days=7)
        )
        
        # Create a dose without appointment
        self.dose = Dose.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            date_administered=timezone.now().date(),
            dose_number=1
        )
    
    def test_link_appointment_to_dose(self):
        """Test linking an appointment to a dose"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('dose_link_appointment', args=[self.dose.id])
        data = {'appointment_id': self.appointment.id}
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.dose.refresh_from_db()
        self.assertEqual(self.dose.appointment, self.appointment)
    
    def test_get_linkable_appointments(self):
        """Test getting available appointments to link"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('dose_link_appointments', args=[self.dose.id])
        response = self.client.get(f'{url}?vaccine_id={self.vaccine.id}&dose_date={self.dose.date_administered}')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('appointments', data)
        self.assertEqual(len(data['appointments']), 1)


class ProfileViewTest(TestCase):
    """Test the profile view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.url = reverse('profile')
    
    def test_profile_login_required(self):
        """Test that login is required"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view_get(self):
        """Test GET request to profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_profile_update_post(self):
        """Test updating profile"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'updated@example.com',
            'username': 'testuser',
        }
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'updated@example.com')
