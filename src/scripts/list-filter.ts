import {terms,matchesAll} from './kit/search';
const form=document.querySelector<HTMLFormElement>('#filters');
if(form){
 const names=['q','cat','model','open','year'] as const;
 const controls=Object.fromEntries(names.map(n=>[n,form.elements.namedItem(n)])) as Record<typeof names[number],HTMLInputElement|HTMLSelectElement>;
 const cards=Array.from(document.querySelectorAll<HTMLElement>('.card'));
 function filter(write=true){let n=0;for(const c of cards){c.hidden=!(matchesAll(c.dataset.search||'',terms(controls.q.value))&&(!controls.cat.value||c.dataset.category===controls.cat.value)&&(!controls.model.value||JSON.parse(c.dataset.models!).includes(controls.model.value))&&(!controls.open.value||c.dataset.open?.split(' ').includes(controls.open.value))&&(!controls.year.value||c.dataset.date?.startsWith(controls.year.value)));if(!c.hidden)n++;}
 document.querySelector('#count')!.textContent=`${n} ${n===1?'entry':'entries'}`;document.querySelector<HTMLElement>('.no-results')!.hidden=n!==0;
 if(write){const u=new URL(location.href);for(const name of names)controls[name].value?u.searchParams.set(name,controls[name].value):u.searchParams.delete(name);history.pushState(null,'',u);}}
 function restore(){const params=new URLSearchParams(location.search);for(const name of names)controls[name].value=params.get(name)||'';filter(false);}
 form.addEventListener('input',e=>{if((e.target as HTMLInputElement).name==='q')filter();});form.addEventListener('change',e=>{if(e.target instanceof HTMLSelectElement)filter();});form.addEventListener('submit',e=>{e.preventDefault();filter();});form.addEventListener('reset',()=>queueMicrotask(()=>filter()));document.querySelector('[data-clear-filters]')?.addEventListener('click',()=>{form.reset();controls.q.focus();});addEventListener('popstate',restore);restore();
}
