(function(){
  function qs(id){return document.getElementById(id);} // helper
  const modal=qs('appointment-delete-modal');
  if(!modal) return;
  const form=qs('delete-modal-form');
  const closeBtn=qs('delete-modal-close');
  const cancelBtn=qs('delete-modal-cancel');
  const bg=modal.querySelector('.modal-background');
  function open(actionUrl, desc){
    form.action=actionUrl;
    const text=qs('delete-modal-text');
    if(text){text.textContent=desc;}
    modal.classList.add('is-active');
  }
  function close(){modal.classList.remove('is-active');}
  [closeBtn,cancelBtn,bg].forEach(el=>el&&el.addEventListener('click',close));
  document.addEventListener('click',function(e){
    const t=e.target;
    if(!(t instanceof HTMLElement)) return;
    if(t.matches('.js-appt-delete')){
      e.preventDefault();
      const url=t.getAttribute('href');
      const label=t.getAttribute('data-label') || '';
      const type=t.getAttribute('data-type') || 'appointment';
      let baseMsg= type==='dose' ? 'Delete this dose?' : 'Delete this appointment?';
      if(label){
        baseMsg = type==='dose' ? `Delete dose: ${label}?` : `Delete appointment: ${label}?`;
      }
      open(url, baseMsg);
    }
  });
})();
