(function(){
  function attachPasswordChecklist(config){
    const input = document.getElementById(config.inputId);
    if(!input){ return; }
    const list = document.getElementById(config.listId);
    if(!list){ return; }
    const items = {
      length: list.querySelector('[data-rule="length"]'),
      upper: list.querySelector('[data-rule="upper"]'),
      lower: list.querySelector('[data-rule="lower"]'),
      number: list.querySelector('[data-rule="number"]'),
      special: list.querySelector('[data-rule="special"]')
    };
    function evaluate(value){
      const tests = {
        length: value.length >= (config.minLength||8),
        upper: /[A-Z]/.test(value),
        lower: /[a-z]/.test(value),
        number: /\d/.test(value),
        special: /[^A-Za-z0-9]/.test(value)
      };
      Object.keys(tests).forEach(k => {
        const li = items[k];
        if(!li) return;
        if(tests[k]) li.classList.add('met'); else li.classList.remove('met');
      });
    }
    input.addEventListener('input', function(){ evaluate(this.value); });
  // Show/hide behavior: hidden by default until focus
  list.style.display = 'none';
  input.addEventListener('focus', function(){ list.style.display='block'; });
  input.addEventListener('blur', function(){ if(!input.value){ list.style.display='none'; } });
    // initial state
    evaluate(input.value||'');
  }
  window.PasswordRequirements = { initAll: function(){
    // signup page
  attachPasswordChecklist({inputId:'id_password1', listId:'password-requirements', minLength:8});
    // reset confirm page
  attachPasswordChecklist({inputId:'id_new_password1', listId:'password-requirements-reset', minLength:8});
  }};
})();
