import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, basename, resolve, sep } from 'node:path';
import { createHash } from 'node:crypto';
import { parseDocument, visit, isScalar } from 'yaml';
import { micromark } from 'micromark';
import { gfm, gfmHtml } from 'micromark-extension-gfm';
export const ROOT=process.cwd();
export const BASE='https://datapoints.semanticmachines.fyi', NAME='Model Data Points';
export const GITHUB='https://github.com/techczech/model-data-points', BENCHMARKS='https://semanticmachines.fyi/benchmarks', SNACKS='https://researchsnacks.semanticmachines.fyi';
export const TAGLINE='Small experiments with AI models: what was tested, on which models, why, and what happened.';
export const INTRO='A data point is one small experiment with AI models: what was tested, on which models, why, and what happened. They are not systematic benchmarks; read each one with its caveats.';
export const TASK_TYPES:Record<string,string>={ocr:'OCR','computer-use':'Computer use','local-models':'Local models',coding:'Coding','api-behaviour':'API behaviour','image-generation':'Image generation',speech:'Speech',other:'Other'};
export const ACCESS:Record<string,string>={api:'API',local:'Local',cli:'Command line'};
export type Model={name:string;provider:string;open_weights:boolean;access:string;version?:string};
export type Entry={id:string;title:string;date:string;task_type:string;models:Model[];purpose:string;context:string;method:string;headline:string;results:{columns:unknown[];rows:unknown[][]};caveats:string[];suggests:string;status:string;sources:string[];slug:string;_body:string;_source:string};
export function legacyText(v:unknown):string{
 if(v===null)return 'None';if(typeof v==='boolean')return v?'True':'False';
 if(Array.isArray(v))return '['+v.map(pyRepr).join(', ')+']';
 if(typeof v==='object')return '{'+Object.entries(v!).map(([k,w])=>pyRepr(k)+': '+pyRepr(w)).join(', ')+'}';
 return String(v);
}
function pyRepr(v:unknown):string{if(typeof v!=='string')return legacyText(v);const quote=v.includes("'")&&!v.includes('"')?'"':"'";return quote+v.replaceAll('\\','\\\\').replaceAll(quote,'\\'+quote).replaceAll('\n','\\n')+quote;}
export const e=(v:unknown)=>legacyText(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#x27;');
export const files=(dir:string):string[]=>existsSync(dir)?readdirSync(dir).sort().flatMap(n=>statSync(join(dir,n)).isDirectory()?files(join(dir,n)):[join(dir,n)]):[];
export function privacyErrors(text:string,label:string):string[]{
  return text.split('\n').flatMap((line,i)=>[[/\/Users\/|~\/|\/home\/|[A-Za-z]:\\/,'an absolute or home path'],[/javascript:|data:text\/html/i,'a script URL']].filter(([rx])=>(rx as RegExp).test(line)).map(([,what])=>`${label}:${i+1}: contains ${what}`));
}
export function parseEntry(path:string):Entry{
 const text=readFileSync(path,'utf8'), id=basename(path,'.md'), m=/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
 if(!m)throw new Error(`${id}: no YAML frontmatter`);
 let fm:any;try{const doc=parseDocument(m[1]);if(doc.errors.length)throw doc.errors[0];visit(doc,(_,node)=>{if(isScalar(node)&&typeof node.value==='number'&&Number.isInteger(node.value)&&/[.eE]/.test(node.source||''))node.value=node.value.toFixed(1);});fm=doc.toJS();}catch{throw new Error(`${id}: invalid YAML`);}
 if(!fm||typeof fm!=='object'||Array.isArray(fm))throw new Error(`${id}: frontmatter is not a mapping`);
 const errors=privacyErrors(text,id);
 for(const k of ['id','title','date','task_type','models','purpose','context','method','headline','results','caveats','suggests','status','sources'])if(fm[k]==null||fm[k]==='')errors.push(`${id}: missing required field '${k}'`);
 if(fm.id!==id)errors.push(`${id}: id does not match file name`);
 const match=/^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:[.-][a-z0-9]+)*)$/.exec(String(fm.id));
 if(!match)errors.push(`${id}: id must look like YYYY-MM-DD-slug`);
 if(!/^\d{4}-\d{2}-\d{2}$/.test(String(fm.date))||!Number.isFinite(Date.parse(fm.date))||new Date(fm.date).toISOString().slice(0,10)!==fm.date)errors.push(`${id}: date must be YYYY-MM-DD`);
 if(!(Object.hasOwn(TASK_TYPES,fm.task_type)))errors.push(`${id}: invalid task_type`);
 if(!['complete','partial'].includes(fm.status))errors.push(`${id}: status must be complete or partial`);
 for(const k of ['title','purpose','context','method','headline','suggests'])if(typeof fm[k]!=='string')errors.push(`${id}: ${k} must be text`);
 if(!Array.isArray(fm.models)||!fm.models.length)errors.push(`${id}: models must be a non-empty list`);
 else for(const [i,mo] of fm.models.entries()){
  if(!mo||typeof mo!=='object'){errors.push(`${id}: models[${i}] must be a mapping`);continue;}
  for(const k of ['name','provider'])if(typeof mo[k]!=='string'||!mo[k])errors.push(`${id}: models[${i}] missing '${k}'`);
  if(typeof mo.open_weights!=='boolean')errors.push(`${id}: models[${i}].open_weights must be true or false`);
  if(!(Object.hasOwn(ACCESS,mo.access)))errors.push(`${id}: models[${i}].access must be api, local or cli`);
 }
 const r=fm.results;
 if(!r||!Array.isArray(r.columns)||!Array.isArray(r.rows))errors.push(`${id}: results needs 'columns' and 'rows' lists`);
 else for(const [i,row] of r.rows.entries())if(!Array.isArray(row)||row.length!==r.columns.length)errors.push(`${id}: results row ${i+1} has wrong cell count`);
 for(const k of ['caveats','sources'])if(!Array.isArray(fm[k]))errors.push(`${id}: ${k} must be a list`);
 if(Array.isArray(fm.sources))for(const source of fm.sources){
  if(typeof source!=='string')continue;
  if(/^https?:\/\//.test(source)){try{const u=new URL(source);if(u.username||u.password)errors.push(`${id}: source URL contains credentials`);}catch{errors.push(`${id}: invalid source URL`);}continue;}
  const target=resolve(ROOT,source);
  if(!target.startsWith(ROOT+sep)||!existsSync(target)||!statSync(target).isFile())errors.push(`${id}: source file '${source}' does not exist in the repository`);
 }
 if(errors.length)throw new Error('BUILD FAILED:\n  '+errors.join('\n  '));
 return {...fm,slug:match![2],_body:m[2].trim(),_source:text};
}
export function getEntries(dir=process.env.MDP_ENTRIES_DIR||join(ROOT,'entries')):Entry[]{
 const entries=readdirSync(dir).filter(n=>n.endsWith('.md')).sort().map(n=>parseEntry(join(dir,n)));
 const slugs=new Set<string>();for(const x of entries){if(slugs.has(x.slug))throw new Error(`duplicate slug '${x.slug}'`);if(['about','search','data','style.css','filters.js','copy.js','rss.xml','llms.txt','search-index.json','index.md','index.html','_astro','_headers'].includes(x.slug))throw new Error(`${x.id}: slug '${x.slug}' is reserved`);slugs.add(x.slug);}
 return entries.sort((a,b)=>b.date.localeCompare(a.date)||b.id.localeCompare(a.id));
}
export const dateLabel=(d:string,month:'long'|'short'='long')=>new Intl.DateTimeFormat('en-GB',{day:'numeric',month,year:'numeric',timeZone:'UTC'}).format(new Date(d));
export const cssVersion=createHash('sha1').update(readFileSync(join(ROOT,'scripts/assets/style.css'))).digest('hex').slice(0,8);
export const pageCitation=(title:string,path:string,x?:Entry)=>({title,url:BASE+path,site:NAME,authors:['Dominik Lukeš'],...(x?{date:x.date}:{})});
export const categories=(x:Entry)=>[TASK_TYPES[x.task_type],x.status];
export const paragraphs=(s:string)=>s.trim().split(/\n\s*\n/).map(p=>`<p>${e(p.trim())}</p>`).join('');
export function renderMarkdown(s:string){return micromark(s,{extensions:[gfm()],htmlExtensions:[gfmHtml()]}).replaceAll(/<table>[\s\S]*?<\/table>/g,m=>`<div class="tw">${m}</div>`);}
export function chips(models:Model[]){return [...new Map(models.map(m=>[m.name,m])).values()].map(m=>`<span class="chip ${m.open_weights?'open':'closed'}" title="${m.open_weights?'Open weights':'Closed'}">${e(m.name)} · ${m.open_weights?'open':'closed'}</span>`).join('');}
export function withTOC(html:string){
 const used=new Set(['main','cite','cite-text']);const heads:{id:string;text:string}[]=[];
 html=html.replace(/<h([23])>(.*?)<\/h\1>/g,(_,level,text)=>{const base=text.replace(/<[^>]*>/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'section';let id=base,i=2;while(used.has(id))id=`${base}-${i++}`;used.add(id);heads.push({id,text});return `<h${level} id="${id}">${text}</h${level}>`;});
 return `<details class="toc-m"><summary>Contents</summary><nav aria-label="Contents"><ol>${heads.map(h=>`<li><a href="#${h.id}">${h.text}</a></li>`).join('')}</ol></nav></details>`+html;
}
export function entryHTML(x:Entry){
 const models=x.models.map(m=>`<tr><td>${e(m.name)}${m.version?' <span class="dim">('+e(m.version)+')</span>':''}</td><td>${e(m.provider)}</td><td>${m.open_weights?'Open weights':'Closed'}</td><td>${ACCESS[m.access]}</td></tr>`).join('');
 const results=x.results.rows.map(row=>'<tr>'+row.map(v=>`<td>${String(v).trim().toLowerCase()==='pending'?'<span class="pending">pending</span>':e(v)}</td>`).join('')+'</tr>').join('');
 return withTOC(`<h1>${e(x.title)}</h1><dl class="facts"><dt>Date</dt><dd>${dateLabel(x.date)}</dd><dt>Task type</dt><dd>${e(TASK_TYPES[x.task_type])}</dd><dt>Status</dt><dd>${x.status[0].toUpperCase()+x.status.slice(1)}</dd></dl>
 <h2>Models tested</h2><div class="tw"><table><thead><tr><th>Model or tool</th><th>Provider</th><th>Open?</th><th>How run</th></tr></thead><tbody>${models}</tbody></table></div>
 <h2>Purpose</h2>${paragraphs(x.purpose)}<h2>Context</h2>${paragraphs(x.context)}<h2>Method</h2>${paragraphs(x.method)}<h2>Results</h2><div class="headline">${e(x.headline)}</div><div class="tw"><table><thead><tr>${x.results.columns.map(c=>`<th>${e(c)}</th>`).join('')}</tr></thead><tbody>${results}</tbody></table></div>
 <h2>Caveats</h2><ul>${x.caveats.map(c=>`<li>${e(c)}</li>`).join('')}</ul><h2>What this suggests</h2>${paragraphs(x.suggests)}
 ${x._body?'<h2>More detail</h2><div class="body-md">'+renderMarkdown(x._body)+'</div>':''}
 <h2>Source</h2><p><a href="${GITHUB}/blob/main/entries/${x.id}.md">entries/${x.id}.md</a> in the GitHub repository (Markdown with YAML frontmatter).</p>${x.sources.length?'<ul>'+x.sources.map(s=>`<li><a href="${e(/^https?:\/\//.test(s)?s:GITHUB+'/blob/main/'+s)}">${e(s)}</a></li>`).join('')+'</ul>':''}`);
}
export const ABOUT=`<h1>About Model Data Points</h1>
<p>A data point is one small experiment with AI models: what was tested, on which models, why, and what happened. Each one is a single Markdown file with structured fields, so the entries can be read, filtered and reused.</p>
<h2>What these are not</h2><p>They are not systematic benchmarks. Most are one run on one machine with a handful of tasks. Every entry lists its caveats; read them before drawing a conclusion. For systematic comparisons see <a href="${BENCHMARKS}">Semantic Machines Benchmarks</a>.</p>
<h2>Sister site</h2><p><a href="${SNACKS}">Research Snacks</a> uses AI agents to check claims about the world against primary data, in the spirit of Mark Liberman's <a href="https://languagelog.ldc.upenn.edu/nll/index.php?s=breakfast">Breakfast Experiments™</a>. Model Data Points checks the models themselves.</p>
<h2>Use and licence</h2><p>The text and data are published under CC BY 4.0; the build scripts are MIT. The entries, raw data files and build script are in the <a href="${GITHUB}">GitHub repository</a>.</p>
<h2>Author</h2><p>Dominik Lukeš, part of <a href="https://semanticmachines.fyi">Semantic Machines</a>.</p>`;
