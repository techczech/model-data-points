import { initDialogs, openDialog, closeDialog, isOpen } from './kit/dialog';
import { initKeyboard, bindSingleKeysSwitch } from './kit/keys';
import { cycleTheme } from './kit/theme';
import { initCopy } from './kit/copy';
import { toast } from './kit/toast';
import { scrollToSafe } from './kit/motion';
import { h, terms, matchesAll, highlight, listboxNav, loadJSON } from './kit/search';
import { keyMap } from '../lib/keys';

initDialogs(); initCopy();
const search = document.querySelector<HTMLDialogElement>('#search-dlg')!;
const keys = document.querySelector<HTMLDialogElement>('#keys-dlg')!;
const input = search.querySelector<HTMLInputElement>('input')!;
const results = search.querySelector<HTMLElement>('[role=listbox]')!;
const status = search.querySelector<HTMLElement>('.search-status')!;
const nav = listboxNav(input,results);
type Item = {s:string;t:string;d:string;u:string;k?:string;x?:string};
type Index = {sections:{slug:string;name:string;href:string}[];items:Item[]};
const safeURL = (url: string) => { try { const u=new URL(url,location.origin); return ['http:','https:'].includes(u.protocol) ? u.href : null; } catch {return null;} };
let renderId=0;
async function renderSearch() {
  const id=++renderId;
  const q=input.value.trim(), ts=terms(q);
  try {
    const index=await loadJSON<Index>('/search-index.json'); if(id!==renderId)return;
    results.replaceChildren(); let count=0;
    for(const section of index.sections) {
      const all=index.items.filter(x=>x.s===section.slug && matchesAll(`${x.t} ${x.d} ${x.k || ''}`,ts));
      if(!all.length)continue;
      const group=h('div',{role:'group','aria-label':`${section.name}: ${all.length} results`});
      group.append(h('h3',{},`${section.name} (${all.length})`));
      for(const x of all.slice(0,6)) {
        const url=safeURL(x.u); if(!url)continue;
        const link=h('a',{href:url,role:'option',id:`search-result-${count++}`,'data-source':x.x ? safeURL(x.x) : null},h('strong',{},highlight(x.t,ts)),h('span',{},highlight(x.d,ts)));
        group.append(link);
      }
      if(all.length>6)group.append(h('a',{href:`${section.href}?q=${encodeURIComponent(q)}`},`All ${all.length} in ${section.name}`));
      results.append(group);
    }
    status.textContent = count ? q ? `${count} results for “${q}”` : 'Search entry titles, summaries and text. Try “OCR”, “Gemma” or “coding”.' : `No results for “${q}”. Try a different search.`;
    if(!q) {
      const suggestions=h('div',{class:'search-suggestions'});
      for(const word of ['OCR','Gemma','coding']) {const b=h('button',{type:'button'},word); b.addEventListener('click',()=>{input.value=word;void renderSearch();input.focus();});suggestions.append(b);}
      results.prepend(suggestions);
    }
    nav.reset();
  } catch {
    if(id!==renderId)return;
    results.replaceChildren(h('p',{},'Search is unavailable. Browse ',h('a',{href:'/'},'all entries'),' or ',h('a',{href:'/about/'},'About'),'. Open search again to retry.'));
    status.textContent='The search index could not be loaded.';
  }
}
function openSearch() {openDialog(search,{focus:'input',onClose:()=>input.setAttribute('aria-expanded','false')});input.setAttribute('aria-expanded','true');void renderSearch();}
function openKeys(){openDialog(keys,{focus:'[data-single-keys]'});}
input.addEventListener('input',()=>void renderSearch());
input.addEventListener('keydown',e=>{
  if(e.key==='Escape'){e.preventDefault();closeDialog(search);}
  if(e.key==='Enter') {const current=nav.current();const url=e.shiftKey ? current?.dataset.source : current?.getAttribute('href');if(url){e.preventDefault();location.assign(url);}}
});
document.querySelectorAll('[data-open-search]').forEach(a=>a.addEventListener('click',e=>{if(e instanceof MouseEvent && (e.metaKey||e.ctrlKey||e.altKey||e.shiftKey))return;e.preventDefault();openSearch();}));
document.querySelectorAll('[data-open-keys]').forEach(b=>b.addEventListener('click',openKeys));
bindSingleKeysSwitch(document.querySelector<HTMLInputElement>('[data-single-keys]')!,toast);
const actions: Record<string,()=>void>={theme:()=>{cycleTheme();},top:()=>scrollToSafe(window,{top:0})};
initKeyboard({search:openSearch,toggleSearch:()=>isOpen(search)?closeDialog(search):openSearch(),help:openKeys,keys:Object.fromEntries(keyMap.filter(k=>k.action).map(k=>[k.key,actions[k.action!]]))});
document.querySelectorAll('[data-top]').forEach(b=>b.addEventListener('click',actions.top));
if(location.pathname.replace(/\/$/,'')==='/search') {input.value=new URLSearchParams(location.search).get('q') || '';openSearch();}

import './list-filter';

const headings=Array.from(document.querySelectorAll<HTMLElement>('main.entry h2[id],main.entry h3[id]'));
const tocLinks=Array.from(document.querySelectorAll<HTMLAnchorElement>('.toc a[href^="#"],.toc-m a[href^="#"]'));
if(headings.length && 'IntersectionObserver' in window) {
  let current=headings[0];
  const observer=new IntersectionObserver(()=>{
    current=headings.filter(h=>h.getBoundingClientRect().top<Math.max(160,innerHeight*.3)).at(-1) || headings[0];
    tocLinks.forEach(a=>{if(a.hash===`#${current.id}`)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');a.classList.toggle('on',a.hash===`#${current.id}`);});
    document.querySelectorAll('.toc li.h2').forEach(li=>li.classList.toggle('open',!!li.querySelector('[aria-current=location]')));
  },{rootMargin:'-10% 0px -65% 0px',threshold:[0,1]});
  headings.forEach(h=>observer.observe(h));
}
document.querySelectorAll('.toc-m a').forEach(a=>a.addEventListener('click',()=>{a.closest('details')!.open=false;}));
const header=document.querySelector('header.site')!;
if('ResizeObserver' in window)new ResizeObserver(()=>document.documentElement.style.setProperty('--header-height',`${header.getBoundingClientRect().height}px`)).observe(header);

