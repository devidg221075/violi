'use strict';
(()=>{
  const menu=document.querySelector('.mobile-menu');
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){const a=document.activeElement;if(a&&a.closest&&a.closest('.has-sub'))a.blur();}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.open){menu.open=false;menu.querySelector('summary').focus();}});
  menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.open=false;}));
  document.addEventListener('click',e=>{if(menu?.open&&!menu.contains(e.target))menu.open=false;});
  const form=document.getElementById('filters');
  if(!form)return;
  const search=document.getElementById('search'),category=document.getElementById('category'),sector=document.getElementById('sector'),application=document.getElementById('application');
  const cards=[...document.querySelectorAll('.category-card')], featured=[...document.querySelectorAll('.featured')];
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  function match(el){
    const query=normalize(search.value).split(/\s+/).filter(Boolean),haystack=normalize(el.dataset.search+' '+el.dataset.sector);
    return query.every(w=>haystack.includes(w))&&(!category.value||el.dataset.category===category.value)&&(!sector.value||el.dataset.sector.split(' ').includes(sector.value))&&(!application.value||normalize(el.dataset.application).includes(normalize(application.value)));
  }
  function apply(){
    cards.forEach(el=>{el.hidden=!match(el);}); featured.forEach(el=>{el.hidden=!match(el);});
    const count=cards.filter(el=>!el.hidden).length;
    document.getElementById('result-count').textContent=`${count} ${count===1?'categoria disponibile':'categorie disponibili'}`;
    document.getElementById('no-results').hidden=count!==0;
    document.getElementById('evidenza').hidden=!featured.some(el=>!el.hidden);
  }
  form.addEventListener('submit',e=>{e.preventDefault();apply();});
  search.addEventListener('input',apply);[category,sector,application].forEach(el=>el.addEventListener('change',apply));
  document.getElementById('reset-filters').addEventListener('click',()=>{form.reset();apply();search.focus();});
  const params=new URLSearchParams(location.search);
  for(const [key,el]of[['q',search],['categoria',category],['settore',sector],['applicazione',application]])if(params.has(key))el.value=params.get(key);
  if(params.size)apply();
  const dialog=document.getElementById('compare-dialog'),content=document.getElementById('compare-content');
  const choices=[...document.querySelectorAll('[data-compare]')];
  function update(){
    const selected=choices.filter(el=>el.checked);
    document.querySelectorAll('.compare-count').forEach(el=>el.textContent=`(${selected.length})`);
    choices.forEach(el=>{el.disabled=selected.length>=3&&!el.checked;});
    content.replaceChildren();
    if(!selected.length){const p=document.createElement('p');p.textContent='Seleziona “Confronta” sulle schede dei macchinari in evidenza per aggiungerli qui.';content.append(p);return;}
    const wrapper=document.createElement('div');wrapper.className='table-scroll';const table=document.createElement('table');
    const rows=[['Macchinario',...selected.map(el=>el.closest('.featured').querySelector('h3').textContent)],['Applicazione',...selected.map(el=>el.closest('.featured').querySelector('.tags span').textContent)],['Descrizione',...selected.map(el=>el.closest('.featured').querySelector('p').textContent)],['Specifiche tecniche',...selected.map(()=> 'Da verificare sulla scheda ufficiale')]];
    rows.forEach((row,i)=>{const tr=document.createElement('tr');row.forEach((value,j)=>{const cell=document.createElement(i===0||j===0?'th':'td');if(i===0)cell.scope='col';else if(j===0)cell.scope='row';cell.textContent=value;tr.append(cell);});table.append(tr);});
    const tr=document.createElement('tr'),th=document.createElement('th');th.scope='row';th.textContent='Approfondisci';tr.append(th);
    selected.forEach(el=>{const td=document.createElement('td'),a=document.createElement('a');a.href=el.closest('.featured').querySelector('.button').href;a.textContent='Scheda ufficiale →';a.className='text-link';td.append(a);tr.append(td);});table.append(tr);wrapper.append(table);content.append(wrapper);
  }
  choices.forEach(el=>el.addEventListener('change',update));
  document.querySelectorAll('.compare-open').forEach(btn=>btn.addEventListener('click',()=>{update();dialog.showModal();}));
  document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
})();
