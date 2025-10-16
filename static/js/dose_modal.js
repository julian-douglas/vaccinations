(function(){
  const openBtn=document.getElementById('open-dose-modal');
  const modal=document.getElementById('dose-modal');
  if(!openBtn||!modal) return;
  const closeBtn=document.getElementById('dose-modal-close');
  const cancelBtn=document.getElementById('dose-modal-cancel');
  const bg=document.getElementById('dose-modal-bg');
  function show(){modal.classList.add('is-active');}
  function hide(){modal.classList.remove('is-active');}
  openBtn.addEventListener('click',show);
  [closeBtn,cancelBtn,bg].forEach(el=>el&&el.addEventListener('click',hide));
})();
