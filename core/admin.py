from django.contrib import admin
from .models import Vaccine, Branch, Appointment, Dose

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_dose", "primary_series_doses")
    search_fields = ("name",)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "postcode", "phone")
    search_fields = ("name", "postcode")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "vaccine", "branch", "datetime")
    list_filter = ("branch", "vaccine")
    search_fields = ("user__username", "notes")

@admin.register(Dose)
class DoseAdmin(admin.ModelAdmin):
    list_display = ("user", "vaccine", "dose_number", "date_administered")
    list_filter = ("vaccine",)
    search_fields = ("user__username",)
