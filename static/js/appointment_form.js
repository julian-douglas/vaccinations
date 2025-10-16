// Shared appointment booking logic (date + time buttons)
(function(global){
  function initAppointment(opts){
    const {
      hoursDataScriptId='opening-hours-data',
      dateInputId='appt-date',
      timeWrapperId='appt-time-wrapper',
      timePlaceholderId='time-placeholder',
      hiddenDatetimeId='id_datetime',
      branchSelectId='id_branch',
      dateErrorId='date-error',
      interval=30
    } = opts || {};
    const hoursScript=document.getElementById(hoursDataScriptId);
    let hours=[];try{if(hoursScript){const raw=hoursScript.textContent.trim();if(raw){hours=JSON.parse(raw);}}}catch(e){console.warn('hours parse',e)}
    const dateInput=document.getElementById(dateInputId);
    const timeWrapper=document.getElementById(timeWrapperId);
    const timePlaceholder=document.getElementById(timePlaceholderId);
    const hiddenDT=document.getElementById(hiddenDatetimeId);
    const branchSelect=document.getElementById(branchSelectId)||document.querySelector('[name=branch]');
    const dateError=dateErrorId?document.getElementById(dateErrorId):null;
    const order=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    let lastValidDate='';
    function dayMatch(spec,dn){if(!spec)return false;return spec.split(',').map(s=>s.trim()).some(part=>{if(part.includes('-')){const[a,b]=part.split('-').map(x=>x.trim());if(order.includes(a)&&order.includes(b)){const si=order.indexOf(a),ei=order.indexOf(b),di=order.indexOf(dn);return si<=ei?(di>=si&&di<=ei):(di>=si||di<=ei);}return false;}return part===dn;});}
    function is247(entry){if(!entry)return false;const o=(entry.open||'').trim();const c=(entry.close||'').trim();return (o==='00:00'||o==='0:00') && (c==='23:59'||c==='24:00');}
    function hoursForDate(d){const dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];const dn=dayNames[d.getDay()];if(hours.some(is247)){return [{days:'24/7',open:'00:00',close:'24:00'}];}return hours.filter(h=>dayMatch(h.days,dn));}
    function buildTimes(o,c){if(!o||!c)return[];const normClose=c==='24:00'?'23:59':c;const[oh,om]=o.split(':').map(Number),[ch,cm]=normClose.split(':').map(Number);let start=oh*60+om,end=ch*60+cm;if(end<=start)end+=1440;const out=[];for(let m=start;m<end;m+=interval){const hh=((m/60)|0)%24;const mm=m%60;out.push(String(hh).padStart(2,'0')+':'+String(mm).padStart(2,'0'));}return out;}
    async function fetchHours(id){hours=[];if(!id)return;try{const r=await fetch(`/branches/${id}/hours/`);if(r.ok){const j=await r.json();hours=Array.isArray(j.opening_hours)?j.opening_hours:[];}}catch(e){console.warn('fetch',e)} }
    function clearTimes(){if(timeWrapper) timeWrapper.innerHTML='';}
    function addTimeButton(t){const btn=document.createElement('button');btn.type='button';btn.className='button is-small time-slot';btn.textContent=t;btn.dataset.time=t;btn.addEventListener('click',()=>{document.querySelectorAll(`#${timeWrapperId} .time-slot.is-selected`).forEach(b=>b.classList.remove('is-selected','is-link'));btn.classList.add('is-selected','is-link');updateHidden();});timeWrapper.appendChild(btn);} 
    function updateHidden(){if(!hiddenDT||!dateInput)return;const d=dateInput.value;const sel=timeWrapper.querySelector('.time-slot.is-selected');const t=sel?sel.dataset.time:null;hiddenDT.value=d&&t?`${d} ${t}:00`:'';}
    function dayHasHours(date){return hoursForDate(date).length>0;}
    async function populate(){clearTimes();const dStr=dateInput.value;if(!dStr){if(timeWrapper&&timePlaceholder) timeWrapper.appendChild(timePlaceholder);return;}if(!hours.length&&branchSelect?.value){await fetchHours(branchSelect.value);}const blocks=hoursForDate(new Date(dStr+'T00:00:00'));const all=[];blocks.forEach(b=>all.push(...buildTimes(b.open,b.close)));const today=new Date().toISOString().slice(0,10);const nowHM=new Date().toTimeString().slice(0,5);const filtered=all.filter(hm=>dStr!==today||hm>nowHM);if(!filtered.length){const span=document.createElement('span');span.className='has-text-grey';span.textContent='No available times';timeWrapper.appendChild(span);}else{filtered.forEach(addTimeButton);}updateHidden();}
    async function onBranch(){hiddenDT&&(hiddenDT.value='');clearTimes();if(timeWrapper&&timePlaceholder) timeWrapper.appendChild(timePlaceholder);hours=[];if(branchSelect?.value){await fetchHours(branchSelect.value);}if(dateInput.value){await populate();}}
    branchSelect?.addEventListener('change',onBranch);
    dateInput?.addEventListener('change',()=>{const dStr=dateInput.value;if(!dStr){populate();updateHidden();return;}const d=new Date(dStr+'T00:00:00');if(!dayHasHours(d)){dateError&&(dateError.style.display='block');if(lastValidDate){dateInput.value=lastValidDate;}else{dateInput.value='';}clearTimes();const span=document.createElement('span');span.className='has-text-danger';span.textContent='Branch closed that day';timeWrapper.appendChild(span);hiddenDT&&(hiddenDT.value='');return;}else{dateError&&(dateError.style.display='none');lastValidDate=dStr;}populate();});
    if(branchSelect?.value){onBranch();}
  }
  global.AppointmentUI={init:initAppointment};
})(window);
