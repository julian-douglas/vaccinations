(function() {
  'use strict';

  let currentStep = 1;
  const selectedData = {
    vaccine: null,
    date: null,
    appointment: null,
    isLinked: false // Track if using appointment data
  };

  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    loadVaccines();
    loadAppointments();
    setupEventListeners();
  });

  function loadVaccines() {
    const vaccinesData = document.getElementById('vaccines-data');
    if (!vaccinesData) return;
    
    const vaccines = JSON.parse(vaccinesData.textContent);
    const grid = document.getElementById('vaccine-grid');
    
    vaccines.forEach(vaccine => {
      const card = document.createElement('div');
      card.className = 'selection-card';
      card.dataset.id = vaccine.id;
      card.innerHTML = `
        <div class="selection-card-title">${vaccine.name}</div>
        <div class="selection-card-info">£${vaccine.price}</div>
      `;
      
      card.addEventListener('click', () => selectVaccine(vaccine.id, vaccine.name, card));
      grid.appendChild(card);
    });
  }

  function loadAppointments() {
    const appointmentsData = document.getElementById('appointments-data');
    if (!appointmentsData) return;
    
    const appointments = JSON.parse(appointmentsData.textContent);
    const container = document.getElementById('appointment-list-step1');
    
    if (!container) {
      console.error('appointment-list-step1 container not found');
      return;
    }
    
    if (appointments.length === 0) {
      container.innerHTML = '<div class="none-option"><p>No past appointments found. Please use manual entry.</p></div>';
      return;
    }
    
    appointments.forEach(appt => {
      const card = document.createElement('div');
      card.className = 'appointment-card';
      card.dataset.id = appt.id;
      card.dataset.vaccineId = appt.vaccine_id;
      card.dataset.vaccineName = appt.vaccine_name;
      card.dataset.datetime = appt.datetime;
      card.innerHTML = `
        <div class="appointment-card-header">${appt.vaccine_name}</div>
        <div class="appointment-card-detail">${appt.branch_name} • ${appt.datetime_display}</div>
      `;
      
      card.addEventListener('click', () => selectAppointmentStep1(appt, card));
      container.appendChild(card);
    });
  }

  function selectAppointmentStep1(appt, card) {
    document.querySelectorAll('.appointment-card').forEach(c => {
      c.classList.remove('selected');
    });
    
    card.classList.add('selected');
    selectedData.isLinked = true;
    selectedData.appointment = {
      id: appt.id,
      vaccineName: appt.vaccine_name,
      branchName: appt.branch_name,
      datetime: appt.datetime_display
    };
    selectedData.vaccine = { id: appt.vaccine_id, name: appt.vaccine_name };
    selectedData.date = appt.datetime.split('T')[0];
    
    document.getElementById('selected-appointment').value = appt.id;
    document.getElementById('selected-vaccine').value = appt.vaccine_id;
    document.getElementById('selected-date').value = selectedData.date;
  }

  function selectVaccine(id, name, card) {
    document.querySelectorAll('#vaccine-grid .selection-card').forEach(c => {
      c.classList.remove('selected');
    });
    
    card.classList.add('selected');
    selectedData.vaccine = { id, name };
    document.getElementById('selected-vaccine').value = id;
    document.getElementById('step2-next').disabled = false;
  }

  function setupEventListeners() {
    // Option toggle buttons on step 1
    document.querySelectorAll('.option-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const option = this.dataset.option;
        
        if (option === 'link') {
          document.getElementById('link-section-step1').classList.add('active');
          document.getElementById('manual-section').classList.remove('active');
          selectedData.isLinked = true;
        } else {
          document.getElementById('link-section-step1').classList.remove('active');
          document.getElementById('manual-section').classList.add('active');
          selectedData.isLinked = false;
          selectedData.appointment = null;
          selectedData.vaccine = null;
          selectedData.date = null;
          document.getElementById('selected-appointment').value = '';
          document.getElementById('selected-vaccine').value = '';
          document.getElementById('selected-date').value = '';
          // Deselect all appointment cards
          document.querySelectorAll('.appointment-card').forEach(c => c.classList.remove('selected'));
        }
      });
    });

    // Date input
    const dateInput = document.getElementById('date-input');
    dateInput.addEventListener('change', function() {
      selectedData.date = this.value;
      document.getElementById('selected-date').value = this.value;
      document.getElementById('step3-next').disabled = !this.value;
    });

    // Navigation buttons
    document.getElementById('step1-next').addEventListener('click', () => {
      if (selectedData.isLinked && selectedData.appointment) {
        // Skip vaccine and date steps, go straight to confirmation
        updateConfirmation();
        goToStep(4);
      } else {
        // Go to manual vaccine selection
        goToStep(2);
      }
    });
    
    document.getElementById('step2-back').addEventListener('click', () => goToStep(1));
    document.getElementById('step2-next').addEventListener('click', () => goToStep(3));
    document.getElementById('step3-back').addEventListener('click', () => goToStep(2));
    document.getElementById('step3-next').addEventListener('click', () => {
      updateConfirmation();
      goToStep(4);
    });
    document.getElementById('step4-back').addEventListener('click', () => {
      if (selectedData.isLinked) {
        goToStep(1);
      } else {
        goToStep(3);
      }
    });
  }

  function goToStep(step) {
    // Update step visibility
    document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
    document.querySelector(`.wizard-step[data-step="${step}"]`).classList.add('active');
    
    // Update progress indicators
    document.querySelectorAll('.progress-step').forEach((s, idx) => {
      s.classList.remove('active', 'completed');
      if (idx + 1 < step) {
        s.classList.add('completed');
      } else if (idx + 1 === step) {
        s.classList.add('active');
      }
    });
    
    currentStep = step;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function updateConfirmation() {
    document.getElementById('confirm-vaccine').textContent = selectedData.vaccine?.name || '';
    
    if (selectedData.date) {
      const date = new Date(selectedData.date + 'T00:00:00');
      const formatted = date.toLocaleDateString('en-GB', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      document.getElementById('confirm-date').textContent = formatted;
    }
    
    if (selectedData.appointment) {
      const apptText = `${selectedData.appointment.vaccineName} at ${selectedData.appointment.branchName} on ${selectedData.appointment.datetime}`;
      document.getElementById('confirm-appointment').textContent = apptText;
    } else {
      document.getElementById('confirm-appointment').textContent = 'Not linked';
    }
  }

})();
