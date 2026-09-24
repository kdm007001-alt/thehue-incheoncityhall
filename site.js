const navButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('.nav');
navButton?.addEventListener('click',()=>{const open=navigation.classList.toggle('open');navButton.setAttribute('aria-expanded',String(open))});
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{navigation.classList.remove('open');navButton?.setAttribute('aria-expanded','false')}));
const zoom=document.querySelector('.zoom-modal');
document.querySelectorAll('[data-zoom]').forEach(el=>el.addEventListener('click',()=>{zoom.querySelector('img').src=el.dataset.zoom;zoom.classList.add('show');document.body.style.overflow='hidden'}));
zoom?.querySelector('button').addEventListener('click',()=>{zoom.classList.remove('show');document.body.style.overflow=''});
zoom?.addEventListener('click',e=>{if(e.target===zoom)zoom.querySelector('button').click()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&zoom?.classList.contains('show'))zoom.querySelector('button').click()});

const opensAt=Date.parse('2026-09-28T00:00:00+09:00');
const koreanToday=()=>new Date(Date.now()+9*60*60*1000).toISOString().slice(0,10);
document.querySelectorAll('.lead-form').forEach(form=>{
  const state=form.querySelector('.form-status');
  const submit=form.querySelector('.form-submit');
  const date=form.querySelector('[name=visit_date]');
  const updateAvailability=()=>{
    const today=koreanToday();
    date.min=today>'2026-09-28'?today:'2026-09-28';
    if(date.value&&date.value<date.min)date.value='';
    const open=Date.now()>=opensAt;
    submit.disabled=!open;
    submit.textContent=open?'방문예약 신청':'9월 28일부터 예약 가능';
  };
  updateAvailability();
  if(Date.now()<opensAt) setInterval(updateAvailability,60000);
  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(Date.now()<opensAt){state.textContent='9월 28일부터 방문예약이 가능합니다.';return}
    const parts=[...form.querySelectorAll('[data-phone]')].map(el=>el.value.trim());
    if(parts.length!==3||!/^010\d{8}$/.test(parts.join(''))){state.textContent='연락처를 확인해 주세요.';return}
    const payload=Object.fromEntries(new FormData(form));
    payload.phone=parts.join('');
    submit.disabled=true;
    state.textContent='예약 접수 중입니다.';
    try{
      const response=await fetch('/api/interest',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});
      const result=await response.json();
      if(!response.ok||!result.ok)throw Error(result.error||'방문예약 접수 중 오류가 발생했습니다.');
      form.reset();state.textContent='방문예약 접수가 완료되었습니다.';
    }catch(error){state.textContent=error.message||'접수 중 오류가 발생했습니다. 1555-1622로 연락해 주세요.'}
    finally{updateAvailability()}
  });
});
