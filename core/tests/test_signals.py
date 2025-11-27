"""
Tests for Django signals
"""
from django.test import TestCase
from django.db.models.signals import post_migrate
from django.apps import apps
from unittest.mock import patch, MagicMock
from core.models import Vaccine, Branch
from core.signals import seed_after_migrate


class SignalTests(TestCase):
    """Test Django signal handlers"""
    
    @patch('core.signals.seed_initial')
    def test_seed_after_migrate_runs_when_empty(self, mock_seed):
        """Test that seed runs after migrate when database is empty"""
        # Ensure database is empty
        Vaccine.objects.all().delete()
        Branch.objects.all().delete()
        
        # Create a mock sender
        mock_sender = MagicMock()
        mock_sender.label = 'core'
        
        # Call the signal handler
        seed_after_migrate(sender=mock_sender)
        
        # Verify seed was called
        mock_seed.assert_called_once_with(verbose=True)
    
    @patch('core.signals.seed_initial')
    def test_seed_after_migrate_skips_when_data_exists(self, mock_seed):
        """Test that seed does not run when data already exists"""
        # Create some initial data
        Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        Branch.objects.create(
            name="Test Branch",
            address="123 Test St",
            postcode="12345",
            phone="123-456-7890",
            email="test@branch.com"
        )
        
        # Create a mock sender
        mock_sender = MagicMock()
        mock_sender.label = 'core'
        
        # Call the signal handler
        seed_after_migrate(sender=mock_sender)
        
        # Verify seed was NOT called
        mock_seed.assert_not_called()
    
    @patch('core.signals.seed_initial')
    def test_seed_after_migrate_skips_other_apps(self, mock_seed):
        """Test that seed does not run for other apps"""
        # Create a mock sender for a different app
        mock_sender = MagicMock()
        mock_sender.label = 'admin'
        
        # Call the signal handler
        seed_after_migrate(sender=mock_sender)
        
        # Verify seed was NOT called
        mock_seed.assert_not_called()
    
    @patch('core.signals.seed_initial')
    def test_seed_after_migrate_with_only_vaccines(self, mock_seed):
        """Test seed runs when only vaccines exist but no branches"""
        # Clear everything
        Vaccine.objects.all().delete()
        Branch.objects.all().delete()
        
        # Create only a vaccine
        Vaccine.objects.create(name="Test Vaccine", price_per_dose=20.00)
        
        # Create a mock sender
        mock_sender = MagicMock()
        mock_sender.label = 'core'
        
        # Call the signal handler
        seed_after_migrate(sender=mock_sender)
        
        # Should run seed because branches don't exist
        mock_seed.assert_called_once()
    
    @patch('core.signals.seed_initial')
    def test_seed_after_migrate_with_only_branches(self, mock_seed):
        """Test seed runs when only branches exist but no vaccines"""
        # Clear everything
        Vaccine.objects.all().delete()
        Branch.objects.all().delete()
        
        # Create only a branch
        Branch.objects.create(
            name="Test Branch",
            address="123 Test St",
            postcode="12345",
            phone="123-456-7890",
            email="test@branch.com"
        )
        
        # Create a mock sender
        mock_sender = MagicMock()
        mock_sender.label = 'core'
        
        # Call the signal handler
        seed_after_migrate(sender=mock_sender)
        
        # Should run seed because vaccines don't exist
        mock_seed.assert_called_once()
