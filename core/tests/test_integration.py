"""
Integration tests for the core app - testing complete user workflows
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import Vaccine, Branch, Appointment, Dose

User = get_user_model()


class UserBookingWorkflowTest(TestCase):
    """Test the complete user booking workflow"""
    
    def setUp(self):
        self.client = Client()
        self.vaccine = Vaccine.objects.create(
            name="COVID-19 Vaccine",
            price_per_dose=25.00,
            side_effects=["Sore arm", "Fatigue"]
        )
        self.branch = Branch.objects.create(
            name="Central Clinic",
            address="123 Main St",
            opening_hours=[
                {"day": "Monday", "hours": "9:00 AM - 5:00 PM"}
            ]
        )
    
    def test_complete_booking_workflow(self):
        """Test complete workflow: signup -> login -> book -> view"""
        # 1. Sign up
        signup_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'SecureP@ssw0rd!',
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)
        
        # 2. User should be logged in automatically after signup
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_authenticated)
        
        # 3. Book an appointment
        future_datetime = (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        appointment_data = {
            'vaccine': self.vaccine.id,
            'branch': self.branch.id,
            'datetime': future_datetime,
        }
        response = self.client.post(reverse('appointment_add'), appointment_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. View appointments
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['upcoming_appointments']), 1)
    
    def test_record_dose_workflow(self):
        """Test complete workflow for recording a dose"""
        # 1. Create and login user
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # 2. Record a dose
        dose_data = {
            'vaccine': self.vaccine.id,
            'date_administered': timezone.now().date().strftime('%Y-%m-%d'),
        }
        response = self.client.post(reverse('dose_add'), dose_data)
        self.assertEqual(response.status_code, 302)
        
        # 3. View profile to see dose
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['doses']), 1)
    
    def test_link_appointment_to_dose_workflow(self):
        """Test workflow: book appointment -> record dose -> link them"""
        # 1. Create and login user
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # 2. Book appointment in the past
        past_datetime = timezone.now() - timedelta(days=7)
        appointment = Appointment.objects.create(
            user=user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=past_datetime
        )
        
        # 3. Record a dose
        dose = Dose.objects.create(
            user=user,
            vaccine=self.vaccine,
            date_administered=timezone.now().date(),
            dose_number=1
        )
        
        # 4. Link appointment to dose
        url = reverse('dose_link_appointment', args=[dose.id])
        data = {'appointment_id': appointment.id}
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        dose.refresh_from_db()
        self.assertEqual(dose.appointment, appointment)


class BranchBrowsingWorkflowTest(TestCase):
    """Test browsing and viewing branch information"""
    
    def setUp(self):
        self.client = Client()
        self.branch = Branch.objects.create(
            name="Central Clinic",
            address="123 Main St",
            opening_hours=[
                {"day": "Monday", "hours": "9:00 AM - 5:00 PM"},
                {"day": "Tuesday", "hours": "9:00 AM - 5:00 PM"}
            ]
        )
    
    def test_browse_branches(self):
        """Test browsing branch list"""
        response = self.client.get(reverse('branch_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.branch.name)
    
    def test_view_branch_details(self):
        """Test viewing branch details"""
        response = self.client.get(reverse('branch_detail', args=[self.branch.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.branch.name)
        self.assertContains(response, self.branch.address)


class AppointmentManagementWorkflowTest(TestCase):
    """Test managing appointments - edit and delete"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        self.branch = Branch.objects.create(name="Test Branch", address="123 Test St", postcode="12345", phone="123-456-7890", email="test@branch.com")
        self.client.login(username='testuser', password='testpass123')
    
    def test_edit_appointment_workflow(self):
        """Test editing an appointment"""
        # 1. Create appointment
        appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=7)
        )
        
        # 2. Edit appointment
        new_datetime = (timezone.now() + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M')
        edit_data = {
            'vaccine': self.vaccine.id,
            'branch': self.branch.id,
            'datetime': new_datetime,
        }
        url = reverse('appointment_edit', args=[appointment.id])
        response = self.client.post(url, edit_data)
        
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        # Verify the datetime was updated (comparing dates only to avoid timezone issues)
        self.assertNotEqual(appointment.datetime.date(), (timezone.now() + timedelta(days=7)).date())
    
    def test_delete_appointment_workflow(self):
        """Test deleting an appointment"""
        # 1. Create appointment
        appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=7)
        )
        
        # 2. Delete appointment
        url = reverse('appointment_delete', args=[appointment.id])
        response = self.client.post(url)
        
        # 3. Verify deletion
        self.assertFalse(Appointment.objects.filter(id=appointment.id).exists())


class ProfileManagementWorkflowTest(TestCase):
    """Test user profile management"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_update_profile_workflow(self):
        """Test updating user profile"""
        # 1. View profile
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Update profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'username': 'testuser',
        }
        response = self.client.post(reverse('profile'), update_data)
        
        # 3. Verify update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
    
    def test_view_vaccination_history_workflow(self):
        """Test viewing vaccination history in profile"""
        # 1. Create some doses
        vaccine = Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        Dose.objects.create(
            user=self.user,
            vaccine=vaccine,
            date_administered=timezone.now().date(),
            dose_number=1
        )
        Dose.objects.create(
            user=self.user,
            vaccine=vaccine,
            date_administered=(timezone.now() - timedelta(days=30)).date(),
            dose_number=2
        )
        
        # 2. View profile
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['doses']), 2)
        
        # 3. Test sorting
        response = self.client.get(reverse('profile') + '?sort=date&dir=asc')
        doses = response.context['doses']
        self.assertTrue(doses[0].date_administered < doses[1].date_administered)
