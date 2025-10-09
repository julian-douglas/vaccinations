import importlib
from django.db import transaction
from .models import Vaccine, Branch

def seed_initial(verbose: bool = False):
    try:
        data = importlib.import_module("seed_variables")
    except ModuleNotFoundError:
        if verbose:
            print("seed_variables module not found; skipping seeding.")
        return

    seed_vaccines = getattr(data, "seed_vaccines", [])
    seed_branches = getattr(data, "seed_branches", [])

    with transaction.atomic():
        v_created = 0
        for v in seed_vaccines:
            _, created = Vaccine.objects.update_or_create(
                name=v["name"],
                defaults={
                    "primary_series_doses": v.get("primary_series_doses"),
                    "booster_interval_years": v.get("booster_interval_years"),
                    "recurrence_interval_years": v.get("recurrence_interval_years"),
                    "price_per_dose": v.get("price_per_dose", 0),
                    "administration_route": v.get("administration_route"),
                    "age_min": v.get("age_min"),
                    "age_max": v.get("age_max"),
                    "contraindications": v.get("contraindications", []),
                    "side_effects": v.get("side_effects", []),
                    "notes": v.get("notes", ""),
                },
            )
            if created:
                v_created += 1
        b_created = 0
        for b in seed_branches:
            Branch.objects.update_or_create(
                name=b["name"],
                defaults={
                    "address": b.get("address"),
                    "postcode": b.get("postcode"),
                    "phone": b.get("phone"),
                    "email": b.get("email"),
                    "opening_hours": b.get("opening_hours"),
                    "image_url": b.get("image_url"), 
                },
            )
            if created:
                b_created += 1
    if verbose:
        print(f"Seeding complete. Vaccines new: {v_created}, Branches new: {b_created}")
