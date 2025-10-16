from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, Dose, Vaccine

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=150)
    # Override password fields to keep entered text after validation errors
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["vaccine", "branch", "datetime", "notes"]
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vaccine'].queryset = Vaccine.objects.order_by('name')

class DoseForm(forms.ModelForm):
    class Meta:
        model = Dose
        fields = ["vaccine", "date_administered", "appointment"]  # dose_number removed
        widgets = {
            'date_administered': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['vaccine'].queryset = Vaccine.objects.order_by('name')
        if user:
            self.fields['appointment'].queryset = user.appointments.order_by('-datetime')
        else:
            self.fields['appointment'].queryset = Appointment.objects.none()
        self.fields['appointment'].required = False
