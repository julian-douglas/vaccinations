const WizardForm = (function() {
  let currentStep = 1;
  const totalSteps = 4;
  let selectedData = {
    vaccine: null,
    branch: null,
    datetime: null
  };

  function init() {
    loadVaccines();
    loadBranches();
    setupNavigation();
    // Disable next button initially
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) nextBtn.disabled = true;
    
    // Check if we're editing (pre-filled values) or have URL parameters
    checkPreSelections();
  }
  
  function checkPreSelections() {
    // Check for pre-selected vaccine (edit mode)
    const vaccineInput = document.getElementById('selected-vaccine');
    const branchInput = document.getElementById('selected-branch');
    
    setTimeout(() => {
      if (vaccineInput && vaccineInput.value) {
        const vaccineCard = document.querySelector(`#vaccine-grid .selection-card[data-id="${vaccineInput.value}"]`);
        if (vaccineCard) {
          vaccineCard.click();
        }
      }
      
      if (branchInput && branchInput.value) {
        const branchCard = document.querySelector(`#branch-grid .selection-card[data-id="${branchInput.value}"]`);
        if (branchCard) {
          branchCard.click();
        }
      }
      
      // Check URL parameters (from branch page)
      const urlParams = new URLSearchParams(window.location.search);
      const urlBranchId = urlParams.get('branch');
      
      if (urlBranchId && !branchInput.value) {
        // Pre-select the branch but DON'T advance - let them pick vaccine first
        const branchCard = document.querySelector(`#branch-grid .selection-card[data-id="${urlBranchId}"]`);
        if (branchCard) {
          branchCard.click();
          // Stay on step 1 - user needs to select vaccine first
        }
      }
    }, 100);
  }

  function loadVaccines() {
    const vaccinesData = document.getElementById('vaccines-data');
    if (!vaccinesData) return;
    
    const vaccines = JSON.parse(vaccinesData.textContent);
    const grid = document.getElementById('vaccine-grid');
    
    vaccines.forEach(vaccine => {
      const card = document.createElement('div');
      card.className = 'selection-card vaccine-card';
      card.dataset.id = vaccine.id;
      card.dataset.sideEffects = JSON.stringify(vaccine.side_effects || []);
      card.innerHTML = `
        <div class="selection-card-title">${vaccine.name}</div>
        <div class="selection-card-info">£${vaccine.price}</div>
        ${vaccine.side_effects && vaccine.side_effects.length > 0 ? 
          `<button type="button" class="button is-small is-light vaccine-info-btn" onclick="event.stopPropagation(); showVaccineInfo(${vaccine.id}, '${vaccine.name.replace(/'/g, "\\'")}', ${JSON.stringify(vaccine.side_effects).replace(/"/g, '&quot;')})">
            ⓘ Side Effects
          </button>` : ''}
      `;
      
      card.addEventListener('click', () => selectVaccine(vaccine.id, vaccine.name, vaccine.side_effects || [], card));
      grid.appendChild(card);
    });
  }

  function loadBranches() {
    const branchesData = document.getElementById('branches-data');
    if (!branchesData) return;
    
    const branches = JSON.parse(branchesData.textContent);
    const grid = document.getElementById('branch-grid');
    
    branches.forEach(branch => {
      const card = document.createElement('div');
      card.className = 'selection-card branch-selection-card';
      card.dataset.id = branch.id;
      
      // Determine image source
      let imageSrc = '';
      if (branch.image_url) {
        if (branch.image_url.startsWith('http')) {
          imageSrc = branch.image_url;
        } else {
          imageSrc = `/static/${branch.image_url}`;
        }
      } else {
        imageSrc = '/static/img/branches/placeholder.jpg';
      }
      
      // Status text and class
      const statusText = branch.status?.text || 'Hours vary';
      const statusClass = branch.status?.class || 'status-open';
      
      card.innerHTML = `
        <div class="branch-card-image" style="background-image: url('${imageSrc}'); width: calc(100% + 3rem); height: 140px; background-size: cover; background-position: center; border-radius: 12px 12px 0 0; margin: -1.5rem -1.5rem 1rem -1.5rem;"></div>
        <div class="selection-card-title">${branch.name}</div>
        <div class="selection-card-info">${branch.postcode}</div>
      `;
      
      card.addEventListener('click', () => selectBranch(branch.id, branch.name, branch.opening_hours || [], card));
      grid.appendChild(card);
    });
  }

  function selectVaccine(id, name, sideEffects, card) {
    // Remove selection from all cards
    document.querySelectorAll('#vaccine-grid .selection-card').forEach(c => {
      c.classList.remove('selected');
    });
    
    // Select this card
    card.classList.add('selected');
    selectedData.vaccine = { id, name, sideEffects };
    document.getElementById('selected-vaccine').value = id;
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
  }

  // Global function for vaccine info modal
  window.showVaccineInfo = function(id, name, sideEffects) {
    const modal = document.getElementById('vaccine-info-modal');
    if (!modal) return;
    
    document.getElementById('modal-vaccine-name').textContent = name;
    const list = document.getElementById('modal-side-effects-list');
    list.innerHTML = '';
    
    if (sideEffects && sideEffects.length > 0) {
      sideEffects.forEach(effect => {
        const li = document.createElement('li');
        li.textContent = effect;
        list.appendChild(li);
      });
    } else {
      list.innerHTML = '<li>No known side effects listed</li>';
    }
    
    modal.classList.add('is-active');
  };
  
  window.closeVaccineModal = function() {
    const modal = document.getElementById('vaccine-info-modal');
    if (modal) modal.classList.remove('is-active');
  };

  function selectBranch(id, name, openingHours, card) {
    // Remove selection from all cards
    document.querySelectorAll('#branch-grid .selection-card').forEach(c => {
      c.classList.remove('selected');
    });
    
    // Select this card
    card.classList.add('selected');
    selectedData.branch = { id, name };
    document.getElementById('selected-branch').value = id;
    
    // Update opening hours data for AppointmentUI
    const hoursScript = document.getElementById('opening-hours-data');
    if (hoursScript) {
      hoursScript.textContent = JSON.stringify(openingHours);
    }
    
    // Initialize AppointmentUI with the branch hours (don't let it fetch from API)
    if (window.AppointmentUI) {
      AppointmentUI.init({
        branchSelectId: '', // Empty so it won't try to fetch
        hoursDataScriptId: 'opening-hours-data',
        dateInputId: 'appt-date',
        timeWrapperId: 'appt-time-wrapper',
        timePlaceholderId: 'time-placeholder',
        hiddenDatetimeId: 'id_datetime',
        dateErrorId: 'date-error'
      });
    }
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
  }

  function setupNavigation() {
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const submitBtn = document.getElementById('submit-btn');

    nextBtn.addEventListener('click', () => {
      if (validateStep(currentStep)) {
        goToStep(currentStep + 1);
      }
    });

    prevBtn.addEventListener('click', () => {
      goToStep(currentStep - 1);
    });
  }

  function validateStep(step) {
    switch(step) {
      case 1:
        if (!selectedData.vaccine) {
          alert('Please select a vaccine');
          return false;
        }
        break;
      case 2:
        if (!selectedData.branch) {
          alert('Please select a branch');
          return false;
        }
        break;
      case 3:
        const datetime = document.getElementById('id_datetime').value;
        if (!datetime) {
          alert('Please select a date and time');
          return false;
        }
        selectedData.datetime = datetime;
        updateConfirmation();
        break;
    }
    return true;
  }

  function goToStep(step) {
    if (step < 1 || step > totalSteps) return;

    // Hide all steps
    document.querySelectorAll('.step-content').forEach(el => {
      el.classList.remove('active');
    });

    // Show current step
    document.querySelector(`.step-content[data-step="${step}"]`).classList.add('active');

    // Update progress
    document.querySelectorAll('.wizard-step').forEach(el => {
      const stepNum = parseInt(el.dataset.step);
      el.classList.remove('active', 'completed');
      
      if (stepNum < step) {
        el.classList.add('completed');
      } else if (stepNum === step) {
        el.classList.add('active');
      }
    });

    // Update buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');

    prevBtn.style.display = step === 1 ? 'none' : 'block';
    nextBtn.style.display = step === totalSteps ? 'none' : 'block';
    submitBtn.style.display = step === totalSteps ? 'block' : 'none';

    // Disable next button based on current step's selection status
    if (step === 1) {
      nextBtn.disabled = !selectedData.vaccine;
    } else if (step === 2) {
      nextBtn.disabled = !selectedData.branch;
    } else if (step === 3) {
      // Check if date and time are selected
      const datetime = document.getElementById('id_datetime').value;
      nextBtn.disabled = !datetime;
      
      // Set up listener for datetime changes
      const dateInput = document.getElementById('appt-date');
      const timeWrapper = document.getElementById('appt-time-wrapper');
      
      const checkDateTime = () => {
        const dt = document.getElementById('id_datetime').value;
        nextBtn.disabled = !dt;
      };
      
      if (dateInput) {
        dateInput.removeEventListener('change', checkDateTime);
        dateInput.addEventListener('change', checkDateTime);
      }
      
      if (timeWrapper) {
        const observer = new MutationObserver(checkDateTime);
        observer.observe(timeWrapper, { childList: true, subtree: true });
      }
    } else {
      nextBtn.disabled = false;
    }

    currentStep = step;
  }

  function updateConfirmation() {
    document.getElementById('confirm-vaccine').textContent = selectedData.vaccine?.name || '';
    document.getElementById('confirm-branch').textContent = selectedData.branch?.name || '';
    
    // Show/hide side effects button on confirmation page
    const confirmBtn = document.getElementById('confirm-vaccine-info-btn');
    if (confirmBtn && selectedData.vaccine?.sideEffects?.length > 0) {
      confirmBtn.style.display = 'inline-block';
    } else if (confirmBtn) {
      confirmBtn.style.display = 'none';
    }
    
    if (selectedData.datetime) {
      const dt = new Date(selectedData.datetime);
      const formatted = dt.toLocaleString('en-GB', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      document.getElementById('confirm-datetime').textContent = formatted;
    }
  }
  
  // Global function for showing vaccine info on confirmation page
  window.showConfirmVaccineInfo = function() {
    if (selectedData.vaccine) {
      showVaccineInfo(selectedData.vaccine.id, selectedData.vaccine.name, selectedData.vaccine.sideEffects);
    }
  };

  return {
    init
  };
})();
