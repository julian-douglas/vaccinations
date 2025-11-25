from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.http import JsonResponse, Http404
from django.utils import timezone
from datetime import date
import json
from .models import Appointment, Vaccine, Branch, Dose, User
from .forms import AppointmentForm, CustomUserCreationForm, DoseForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


def home(request):
    appointments = Appointment.objects.select_related('vaccine', 'branch').filter(user=request.user) if request.user.is_authenticated else []
    vaccines = Vaccine.objects.all()[:10]
    branches = Branch.objects.all()[:10]
    doses = Dose.objects.select_related('vaccine').filter(user=request.user).order_by('-date_administered')[:5] if request.user.is_authenticated else []
    return render(request, 'home.html', {
        'appointments': appointments,
        'vaccines': vaccines,
        'branches': branches,
        'recent_doses': doses,
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Welcome, your account has been created.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def appointment_create(request):
    # allow pre-select branch via query param (?branch=ID)
    initial = {}
    branch_id = request.GET.get('branch') if request.method == 'GET' else request.POST.get('branch')
    if branch_id:
        try:
            initial_branch = Branch.objects.get(pk=branch_id)
            initial['branch'] = initial_branch
        except Branch.DoesNotExist:
            pass
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.user = request.user
            appt.save()
            appt.save()
            messages.success(request, 'Appointment booked!')
            return redirect('appointment_confirmation', pk=appt.pk)
    else:
        form = AppointmentForm(initial=initial)
    # supply hours for selected branch (initial or from form)
    branch_obj = initial.get('branch') if initial.get('branch') else None
    if not branch_obj and 'branch' in request.POST:
        try:
            branch_obj = Branch.objects.get(pk=request.POST.get('branch'))
        except Branch.DoesNotExist:
            branch_obj = None
    opening_hours = branch_obj.opening_hours if branch_obj else []
    opening_hours_json = json.dumps(opening_hours if isinstance(opening_hours, list) else [])
    
    # Prepare vaccines and branches data for wizard
    vaccines = Vaccine.objects.all().order_by('name')
    vaccines_json = json.dumps([{
        'id': v.id,
        'name': v.name,
        'price': str(v.price_per_dose),
        'side_effects': v.side_effects if isinstance(v.side_effects, list) else []
    } for v in vaccines])
    
    branches = Branch.objects.all().order_by('name')
    branches_json = json.dumps([{
        'id': b.id,
        'name': b.name,
        'postcode': b.postcode,
        'image_url': b.image_url or '',
        'status': b.status_info() or {'text': 'Hours vary', 'class': 'status-open'},
        'opening_hours': b.opening_hours if isinstance(b.opening_hours, list) else []
    } for b in branches])
    
    return render(request, 'appointment_form.html', {
        'form': form,
        'opening_hours': opening_hours,
        'opening_hours_json': opening_hours_json,
        'vaccines_json': vaccines_json,
        'branches_json': branches_json,
        'today_str': date.today().isoformat(),
    })

@login_required
def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated.')
            return redirect('home')
    else:
        form = AppointmentForm(instance=appt)
    
    # Prepare vaccines and branches data for wizard (same as create)
    vaccines = Vaccine.objects.all().order_by('name')
    vaccines_json = json.dumps([{
        'id': v.id,
        'name': v.name,
        'price': str(v.price_per_dose),
        'side_effects': v.side_effects if isinstance(v.side_effects, list) else []
    } for v in vaccines])
    
    branches = Branch.objects.all().order_by('name')
    branches_json = json.dumps([{
        'id': b.id,
        'name': b.name,
        'postcode': b.postcode,
        'image_url': b.image_url or '',
        'status': b.status_info() or {'text': 'Hours vary', 'class': 'status-open'},
        'opening_hours': b.opening_hours if isinstance(b.opening_hours, list) else []
    } for b in branches])
    
    # Get opening hours for the appointment's branch
    opening_hours = appt.branch.opening_hours if isinstance(appt.branch.opening_hours, list) else []
    opening_hours_json = json.dumps(opening_hours)
    
    return render(request, 'appointment_form.html', {
        'form': form,
        'appointment': appt,
        'opening_hours': opening_hours,
        'opening_hours_json': opening_hours_json,
        'vaccines_json': vaccines_json,
        'branches_json': branches_json,
        'today_str': date.today().isoformat(),
    })

@login_required
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        appt.delete()
        messages.info(request, 'Appointment deleted.')
        # Redirect to the referring page or default to appointments list
        referer = request.META.get('HTTP_REFERER', '')
        if 'appointments' in referer:
            return redirect('appointment_list')
        else:
            return redirect('home')
    return render(request, 'appointment_delete_confirm.html', {'appointment': appt})

@login_required
def appointment_list(request):
    from django.utils import timezone
    now = timezone.now()
    
    upcoming = Appointment.objects.select_related('vaccine','branch').filter(
        user=request.user,
        datetime__gte=now
    ).order_by('datetime')
    
    past = Appointment.objects.select_related('vaccine','branch').filter(
        user=request.user,
        datetime__lt=now
    ).order_by('-datetime')
    
    return render(request, 'appointment_list.html', {
        'upcoming_appointments': upcoming,
        'past_appointments': past,
    })

@login_required
def appointment_confirmation(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, user=request.user)
    return render(request, 'appointment_confirmation.html', {'appointment': appt})

@login_required
def dose_list(request):
    allowed = {
        'date': 'date_administered',
        'vaccine': 'vaccine__name',
        'dose': 'dose_number',
    }
    sort = request.GET.get('sort', 'date')
    direction = request.GET.get('dir', 'desc')
    field = allowed.get(sort, 'date_administered')
    order = ('-' if direction == 'desc' else '') + field
    doses = Dose.objects.select_related('vaccine', 'appointment').filter(user=request.user).order_by(order)
    def next_dir(col):
        if sort == col and direction == 'asc':
            return 'desc'
        return 'asc'
    links = {
        'date': f"?sort=date&dir={next_dir('date')}",
        'vaccine': f"?sort=vaccine&dir={next_dir('vaccine')}",
        'dose': f"?sort=dose&dir={next_dir('dose')}",
    }
    dose_form = DoseForm(user=request.user)
    return render(request, 'dose_list.html', {
        'doses': doses,
        'sort': sort,
        'direction': direction,
        'links': links,
        'dose_form': dose_form,
    })

@login_required
def dose_create(request):
    from django.utils import timezone
    
    if request.method == 'POST':
        form = DoseForm(request.POST, user=request.user)
        if form.is_valid():
            dose = form.save(commit=False)
            dose.user = request.user
            # auto increment dose_number per vaccine & user
            last = Dose.objects.filter(user=request.user, vaccine=dose.vaccine).aggregate(m=Max('dose_number'))['m'] or 0
            dose.dose_number = last + 1
            dose.save()
            messages.success(request, f'Dose #{dose.dose_number} recorded.')
            return redirect('profile')
    else:
        form = DoseForm(user=request.user)
    
    # Prepare vaccine and appointment data for the wizard
    vaccines = Vaccine.objects.all().order_by('name')
    vaccines_json = json.dumps([{
        'id': v.id,
        'name': v.name,
        'price': str(v.price_per_dose),
    } for v in vaccines])
    
    # Only show past appointments for linking
    now = timezone.now()
    past_appointments = request.user.appointments.select_related('vaccine', 'branch').filter(
        datetime__lt=now
    ).order_by('-datetime')
    
    appointments_json = json.dumps([{
        'id': a.id,
        'vaccine_id': a.vaccine.id,
        'vaccine_name': a.vaccine.name,
        'branch_name': a.branch.name,
        'datetime': a.datetime.isoformat(),
        'datetime_display': a.datetime.strftime('%Y-%m-%d %H:%M'),
    } for a in past_appointments])
    
    return render(request, 'dose_form.html', {
        'form': form,
        'vaccines_json': vaccines_json,
        'appointments_json': appointments_json,
    })

@login_required
def dose_delete(request, pk):
    dose = get_object_or_404(Dose, pk=pk, user=request.user)
    if request.method == 'POST':
        dose.delete()
        messages.info(request, 'Dose deleted.')
        # Redirect to the referring page or default to profile
        referer = request.META.get('HTTP_REFERER', '')
        if 'profile' in referer:
            return redirect('profile')
        else:
            return redirect('dose_list')
    return render(request, 'dose_delete_confirm.html', {'dose': dose})

def branch_list(request):
    allowed = {
        'name': 'name',
        'postcode': 'postcode',
        'email': 'email',
        'created': 'id',
    }
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('dir', 'asc')
    field = allowed.get(sort, 'name')
    order = ('-' if direction == 'desc' else '') + field
    branches = Branch.objects.all().order_by(order)

    def next_dir(col):
        return 'desc' if (sort == col and direction == 'asc') else 'asc'

    links = {k: f"?sort={k}&dir={next_dir(k)}" for k in allowed.keys()}

    return render(
        request,
        'branches.html',
        {
            'branches': branches,
            'sort': sort,
            'direction': direction,
            'links': links,
        }
    )

def branch_detail(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    inline_form = None
    if request.user.is_authenticated:
        inline_form = AppointmentForm(initial={'branch': branch})
    opening_hours = branch.opening_hours if isinstance(branch.opening_hours, list) else []
    opening_hours_json = json.dumps(opening_hours)
    return render(request, 'branch.html', {
        'branch': branch,
        'inline_appointment_form': inline_form,
        'opening_hours': opening_hours,
        'opening_hours_json': opening_hours_json,
        'today_str': date.today().isoformat(),
    })

def branch_hours(request, pk):
    """Return opening_hours JSON for a branch (public)."""
    try:
        branch = Branch.objects.get(pk=pk)
    except Branch.DoesNotExist:
        raise Http404
    data = branch.opening_hours if isinstance(branch.opening_hours, list) else []
    return JsonResponse({'opening_hours': data})

@login_required
def profile(request):
    """User profile page with personal info editing and vaccination history"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get vaccination history (doses)
    allowed_sort = {
        'date': 'date_administered',
        'vaccine': 'vaccine__name',
        'dose': 'dose_number',
    }
    sort = request.GET.get('sort', 'date')
    direction = request.GET.get('dir', 'desc')
    field = allowed_sort.get(sort, 'date_administered')
    order = ('-' if direction == 'desc' else '') + field
    doses = Dose.objects.select_related('vaccine', 'appointment').filter(user=request.user).order_by(order)
    
    def next_dir(col):
        if sort == col and direction == 'asc':
            return 'desc'
        return 'asc'
    
    sort_links = {
        'date': f"?sort=date&dir={next_dir('date')}",
        'vaccine': f"?sort=vaccine&dir={next_dir('vaccine')}",
        'dose': f"?sort=dose&dir={next_dir('dose')}",
    }
    
    return render(request, 'profile.html', {
        'form': form,
        'doses': doses,
        'sort': sort,
        'direction': direction,
        'links': sort_links,
    })

@login_required
def dose_link_appointments(request, pk):
    """Get available appointments that can be linked to a dose"""
    dose = get_object_or_404(Dose, pk=pk, user=request.user)
    
    vaccine_id = request.GET.get('vaccine_id')
    dose_date = request.GET.get('dose_date')
    
    # Get past appointments for the same vaccine that aren't already linked to a dose
    appointments = Appointment.objects.filter(
        user=request.user,
        vaccine_id=vaccine_id,
        datetime__lt=timezone.now()
    ).exclude(
        doses__isnull=False  # Exclude appointments already linked to any dose
    ).select_related('vaccine', 'branch')
    
    # Serialize appointments
    appointments_data = [{
        'id': appt.id,
        'vaccine_name': appt.vaccine.name,
        'branch_name': appt.branch.name,
        'datetime_display': appt.datetime.strftime('%Y-%m-%d %H:%M'),
    } for appt in appointments]
    
    return JsonResponse({'appointments': appointments_data})

@login_required
def dose_link_appointment(request, pk):
    """Link an appointment to a dose"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    dose = get_object_or_404(Dose, pk=pk, user=request.user)
    appointment_id = request.POST.get('appointment_id')
    
    if not appointment_id:
        return JsonResponse({'error': 'Appointment ID required'}, status=400)
    
    try:
        appointment = Appointment.objects.get(pk=appointment_id, user=request.user)
        
        # Check if appointment is already linked to another dose
        if appointment.doses.exists():
            return JsonResponse({'error': 'This appointment is already linked to another dose'}, status=400)
        
        # Link the appointment
        dose.appointment = appointment
        dose.save()
        
        return JsonResponse({'success': True})
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
