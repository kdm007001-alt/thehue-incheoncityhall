const navButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('.nav');
navButton?.addEventListener('click',()=>{const open=navigation.classList.toggle('open');navButton.setAttribute('aria-expanded',String(open))});
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{navigation.classList.remove('open');navButton?.setAttribute('aria-expanded','false')}));
const zoom=document.querySelector('.zoom-modal');
document.querySelectorAll('[data-zoom]').forEach(el=>el.addEventListener('click',()=>{zoom.querySelector('img').src=el.dataset.zoom;zoom.classList.add('show');document.body.style.overflow='hidden'}));
zoom?.querySelector('button').addEventListener('click',()=>{zoom.classList.remove('show');document.body.style.overflow=''});
zoom?.addEventListener('click',e=>{if(e.target===zoom)zoom.querySelector('button').click()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&zoom?.classList.contains('show'))zoom.querySelector('button').click()});
document.querySelectorAll('.lead-form').forEach(form=>form.addEventListener('submit',async e=>{
  e.preventDefault();
  const state=form.querySelector('.form-status');
  const parts=[...form.querySelectorAll('[data-phone]')].map(el=>el.value.trim());
  if(parts.length===3&&!/^010\d{8}$/.test(parts.join(''))){state.textContent='연락처를 확인해 주세요.';return}
  const payload=Object.fromEntries(new FormData(form));
  payload.phone=parts.join('');
  state.textContent='접수 중입니다.';
  try{
    const response=await fetch('/api/interest',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});
    if(!response.ok)throw Error('접수 실패');
    form.reset();state.textContent='관심고객 등록이 완료되었습니다.';
  }catch{state.textContent='현재 온라인 접수가 연결되지 않았습니다. 1555-1622로 연락해 주세요.'}
}));
