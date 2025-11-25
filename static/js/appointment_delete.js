// Delete modal handler - v2.0
(function(){
  function qs(id){return document.getElementById(id);} // helper
  const modal=qs('appointment-delete-modal');
  if(!modal) return;
  const form=qs('delete-modal-form');
  const closeBtn=qs('delete-modal-close');
  const cancelBtn=qs('delete-modal-cancel');
  const bg=modal.querySelector('.modal-background');
  let currentRow = null; // Store the row to delete
  
  function open(actionUrl, desc, row){
    form.action=actionUrl;
    const text=qs('delete-modal-text');
    if(text){text.textContent=desc;}
    currentRow = row;
    modal.classList.add('is-active');
  }
  
  function close(){
    modal.classList.remove('is-active');
    currentRow = null;
  }
  
  [closeBtn,cancelBtn,bg].forEach(el=>el&&el.addEventListener('click',close));
  
  // Handle form submission via AJAX
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const actionUrl = form.action;
    const formData = new FormData(form);
    
    fetch(actionUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => {
      if (response.ok) {
        // Remove the row from the table
        if (currentRow) {
          currentRow.remove();
          
          // Check if table is now empty and show empty state
          const tbody = currentRow.closest('tbody');
          if (tbody && tbody.querySelectorAll('tr').length === 0) {
            // Reload to show empty state properly
            window.location.reload();
          }
        }
        
        // Show success message
        const container = document.querySelector('.container');
        if (container) {
          const notification = document.createElement('div');
          notification.className = 'notification is-success';
          notification.style.marginTop = '1rem';
          notification.innerHTML = '<button class="delete"></button>Item deleted successfully.';
          container.insertBefore(notification, container.firstChild);
          
          // Auto-dismiss after 3 seconds
          setTimeout(() => notification.remove(), 3000);
          
          // Make delete button work
          notification.querySelector('.delete').addEventListener('click', () => notification.remove());
        }
        
        close();
      } else {
        console.error('Delete failed');
        alert('Failed to delete. Please try again.');
        close();
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
      close();
    });
  });
  
  document.addEventListener('click',function(e){
    const t=e.target;
    if(!(t instanceof HTMLElement)) return;
    if(t.matches('.js-appt-delete') || t.closest('.js-appt-delete')){
      e.preventDefault();
      const btn = t.matches('.js-appt-delete') ? t : t.closest('.js-appt-delete');
      const url=btn.getAttribute('href');
      const label=btn.getAttribute('data-label') || '';
      const type=btn.getAttribute('data-type') || 'appointment';
      
      // Find the table row to delete
      const row = btn.closest('tr');
      
      let baseMsg= type==='dose' ? 'Delete this dose?' : 'Delete this appointment?';
      if(label){
        baseMsg = type==='dose' ? `Delete dose: ${label}?` : `Delete appointment: ${label}?`;
      }
      open(url, baseMsg, row);
    }
  });
})();
