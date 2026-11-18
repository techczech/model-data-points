import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {join,relative} from 'node:path';
import {parseHTML} from 'linkedom';
import assert from 'node:assert/strict';
import {files,getEntries,ROOT} from '../src/lib/content';
const old=join(ROOT,'.check/old-site'),next=join(ROOT,'site');
assert(existsSync(old),'Capture the old Python build in .check/old-site first.');
const a=files(old).map(f=>relative(old,f)),b=files(next).map(f=>relative(next,f));const removed=a.filter(f=>!b.includes(f)),added=b.filter(f=>!a.includes(f));assert.deepEqual(removed,[]);
const assets=a.filter(f=>!f.endsWith('.html')&&f!=='style.css');for(const f of assets)assert.deepEqual(readFileSync(join(old,f)),readFileSync(join(next,f)),f);
const normal=(el:any)=>el?.textContent.replace(/\s+/g,'').trim();const results=[];
for(const path of ['index.html','about/index.html',...getEntries().map(x=>x.slug+'/index.html')]){
 const before=parseHTML(readFileSync(join(old,path),'utf8')).document,after=parseHTML(readFileSync(join(next,path),'utf8')).document;
 const selectors=path==='index.html'?['.hero','.list','.models']:path.startsWith('about/')?['h1']:['h1','.facts','main table','.headline','.body-md'];
 for(const sel of selectors)assert.deepEqual([...after.querySelectorAll(sel)].map(normal),[...before.querySelectorAll(sel)].map(normal),`${path}: ${sel}`);
 if(path!=='index.html'){
  const clean=(d:any)=>{const main=d.querySelector('main')!.cloneNode(true);main.querySelectorAll('.toc-m,.cite').forEach((n:any)=>n.remove());return normal(main);};
  assert.equal(clean(after),clean(before),`${path}: full main text`);
 }
 const oldLinks=[...before.querySelectorAll('main a')].map((x:any)=>x.getAttribute('href'));const newLinks=[...after.querySelectorAll('main a')].map((x:any)=>x.getAttribute('href'));for(const href of oldLinks)assert(newLinks.includes(href),`${path}: missing link ${href}`);
 const meta=(doc:any)=>[...doc.querySelectorAll('meta[name^=citation_],meta[name^="DC."],meta[property^="og:"]')].map((x:any)=>[x.getAttribute('name')||x.getAttribute('property'),x.getAttribute('content')]);
 for(const m of meta(before))assert(meta(after).some(n=>JSON.stringify(n)===JSON.stringify(m)),`${path}: metadata ${m}`);
 results.push(path);
}
writeFileSync(join(ROOT,'.check/parity.json'),JSON.stringify({oldFiles:a.length,newFiles:b.length,removed,added,unchangedAssets:assets.length,pages:results},null,2));
console.log(`PASS: ${a.length} old paths retained, ${assets.length} assets byte-identical, all ${results.length} pages preserve text, tables, links and metadata; ${added.length} added files.`);
