from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .seed import seed_initial
from .models import Vaccine, Branch

@receiver(post_migrate)
def seed_after_migrate(sender, **kwargs):
    # Only run when core app migrations finish
    if sender.label != 'core':
        return
    # If already have at least one vaccine and one branch, skip
    if Vaccine.objects.exists() and Branch.objects.exists():
        return
    seed_initial(verbose=True)
