from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.http import JsonResponse, Http404
from datetime import date
import json
from .models import Appointment, Vaccine, Branch, Dose, User
from .forms import AppointmentForm, CustomUserCreationForm, DoseForm
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
    return render(request, 'appointment_form.html', {
        'form': form,
        'opening_hours': opening_hours,
        'opening_hours_json': opening_hours_json,
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
    return render(request, 'appointment_form.html', {'form': form, 'appointment': appt})

@login_required
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        appt.delete()
        messages.info(request, 'Appointment deleted.')
        return redirect('home')
    return render(request, 'appointment_delete_confirm.html', {'appointment': appt})

@login_required
def appointment_list(request):
    appts = Appointment.objects.select_related('vaccine','branch').filter(user=request.user).order_by('datetime')
    return render(request, 'appointment_list.html', {'appointments': appts})

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
            return redirect('dose_list')
    else:
        form = DoseForm(user=request.user)
    return render(request, 'dose_form.html', {'form': form})

@login_required
def dose_delete(request, pk):
    dose = get_object_or_404(Dose, pk=pk, user=request.user)
    if request.method == 'POST':
        dose.delete()
        messages.info(request, 'Dose deleted.')
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