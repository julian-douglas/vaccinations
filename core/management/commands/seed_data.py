from django.core.management.base import BaseCommand
from core.models import Vaccine, Branch
from seed_variables import seed_vaccines, seed_branches

class Command(BaseCommand):
    help = "Seed initial vaccines and branches"

    def handle(self, *args, **options):
        created_v = 0
        for data in seed_vaccines:
            obj, created = Vaccine.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                created_v += 1
        created_b = 0
        for data in seed_branches:
            obj, created = Branch.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                created_b += 1
        self.stdout.write(self.style.SUCCESS(f"Vaccines created: {created_v}; Branches created: {created_b}"))
