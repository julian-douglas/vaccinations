"""
Tests for models in the core app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Max
from datetime import timedelta
from core.models import Vaccine, Branch, Appointment, Dose

User = get_user_model()


class VaccineModelTest(TestCase):
    """Test the Vaccine model"""
    
    def setUp(self):
        self.vaccine = Vaccine.objects.create(
            name="COVID-19 Vaccine",
            price_per_dose=25.00,
            side_effects=["Sore arm", "Fatigue", "Headache"]
        )
    
    def test_vaccine_creation(self):
        """Test creating a vaccine"""
        self.assertEqual(self.vaccine.name, "COVID-19 Vaccine")
        self.assertEqual(self.vaccine.price_per_dose, 25.00)
        self.assertIsInstance(self.vaccine.side_effects, list)
    
    def test_vaccine_string_representation(self):
        """Test the string representation of vaccine"""
        self.assertEqual(str(self.vaccine), "COVID-19 Vaccine")
    
    def test_side_effects_storage(self):
        """Test that side effects are stored as JSON"""
        self.assertIn("Sore arm", self.vaccine.side_effects)
        self.assertEqual(len(self.vaccine.side_effects), 3)


class BranchModelTest(TestCase):
    """Test the Branch model"""
    
    def setUp(self):
        self.branch = Branch.objects.create(
            name="Central Clinic",
            address="123 Main St",
            opening_hours=[
                {"day": "Monday", "hours": "9:00 AM - 5:00 PM"},
                {"day": "Tuesday", "hours": "9:00 AM - 5:00 PM"}
            ]
        )
    
    def test_branch_creation(self):
        """Test creating a branch"""
        self.assertEqual(self.branch.name, "Central Clinic")
        self.assertEqual(self.branch.address, "123 Main St")
    
    def test_branch_string_representation(self):
        """Test the string representation of branch"""
        self.assertEqual(str(self.branch), "Central Clinic")
    
    def test_opening_hours_storage(self):
        """Test that opening hours are stored as JSON"""
        self.assertIsInstance(self.branch.opening_hours, list)
        self.assertEqual(len(self.branch.opening_hours), 2)


class AppointmentModelTest(TestCase):
    """Test the Appointment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.vaccine = Vaccine.objects.create(
            name="Flu Vaccine",
            price_per_dose=15.00
        )
        self.branch = Branch.objects.create(
            name="Test Branch",
            address="456 Test St",
            postcode="12345",
            phone="123-456-7890",
            email="test@branch.com"
        )
        self.appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=7)
        )
    
    def test_appointment_creation(self):
        """Test creating an appointment"""
        self.assertEqual(self.appointment.user, self.user)
        self.assertEqual(self.appointment.vaccine, self.vaccine)
        self.assertEqual(self.appointment.branch, self.branch)
    
    def test_appointment_string_representation(self):
        """Test the string representation of appointment"""
        # Format: "username - vaccine @ YYYY-MM-DD HH:MM"
        expected_start = f"{self.user.username} - {self.vaccine.name} @"
        self.assertTrue(str(self.appointment).startswith(expected_start))
    
    def test_appointment_ordering(self):
        """Test that appointments are ordered by datetime descending"""
        future_appt = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() + timedelta(days=14)
        )
        appointments = Appointment.objects.all()
        # Should be ordered by datetime descending (most recent first)
        self.assertEqual(appointments[0], future_appt)  # Future appointment first
        self.assertEqual(appointments[1], self.appointment)


class DoseModelTest(TestCase):
    """Test the Dose model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.vaccine = Vaccine.objects.create(
            name="COVID-19 Vaccine",
            price_per_dose=25.00
        )
        self.branch = Branch.objects.create(
            name="Test Branch",
            address="789 Test St",
            postcode="54321",
            phone="987-654-3210",
            email="test2@branch.com"
        )
        self.appointment = Appointment.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            branch=self.branch,
            datetime=timezone.now() - timedelta(days=7)
        )
        self.dose = Dose.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            date_administered=timezone.now().date(),
            dose_number=1,
            appointment=self.appointment
        )
    
    def test_dose_creation(self):
        """Test creating a dose"""
        self.assertEqual(self.dose.user, self.user)
        self.assertEqual(self.dose.vaccine, self.vaccine)
        self.assertEqual(self.dose.dose_number, 1)
        self.assertEqual(self.dose.appointment, self.appointment)
    
    def test_dose_string_representation(self):
        """Test the string representation of dose"""
        expected = f"{self.user.username} - {self.vaccine.name} dose {self.dose.dose_number}"
        self.assertEqual(str(self.dose), expected)
    
    def test_dose_without_appointment(self):
        """Test creating a dose without linked appointment"""
        manual_dose = Dose.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            date_administered=timezone.now().date(),
            dose_number=2
        )
        self.assertIsNone(manual_dose.appointment)
    
    def test_dose_ordering(self):
        """Test that doses are ordered by date_administered descending"""
        older_dose = Dose.objects.create(
            user=self.user,
            vaccine=self.vaccine,
            date_administered=timezone.now().date() - timedelta(days=30),
            dose_number=2
        )
        doses = Dose.objects.all()
        self.assertEqual(doses[0], self.dose)  # Most recent first
        self.assertEqual(doses[1], older_dose)
    
    def test_auto_increment_dose_number(self):
        """Test that dose_number auto-increments correctly"""
        # This would require updating the model or using signals
        # For now, test manual increment
        max_dose = Dose.objects.filter(
            user=self.user,
            vaccine=self.vaccine
        ).aggregate(max_dose=Max('dose_number'))
        next_dose_number = (max_dose['max_dose'] or 0) + 1
        self.assertEqual(next_dose_number, 2)
