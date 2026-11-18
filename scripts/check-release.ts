import { chromium } from 'playwright-core';
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';
import { homedir } from 'node:os';
import assert from 'node:assert/strict';
import { getEntries, ROOT } from '../src/lib/content';
const dir=join(ROOT,'.check/release');mkdirSync(dir,{recursive:true});
const servers:any[]=[];
function serve(root:string){const s=Bun.serve({hostname:'127.0.0.1',port:0,async fetch(req){let p=decodeURIComponent(new URL(req.url).pathname);if(p.endsWith('/'))p+='index.html';const f=Bun.file(join(root,p));return await f.exists()?new Response(f):new Response('Not found',{status:404});}});servers.push(s);return `http://127.0.0.1:${s.port}`;}
const current=process.argv[2] || serve(join(ROOT,'site'));
const baseline=existsSync(join(ROOT,'.check/old-site/index.html'))?serve(join(ROOT,'.check/old-site')):undefined;
const executablePath=join(homedir(),'Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell');
const browser=await chromium.launch({headless:true,...(existsSync(executablePath)?{executablePath}:{})});
const records:Record<string,any>={target:current,checks:[],comparisons:[]};
const passed=(name:string,detail:any=true)=>{records.checks.push({name,passed:true,detail});console.log(`PASS ${name}`);};
const entries=getEntries();const paths=['/','/about/',...entries.map(x=>`/${x.slug}/`)];const entryCount=entries.length;
const label=(path:string)=>path==='/'?'home':path.split('/').filter(Boolean)[0];
async function contrast(page:any){
 const failures=await page.evaluate(()=>{
  const rgb=(s:string)=>s.match(/[\d.]+/g)!.slice(0,3).map(Number).map(v=>{const n=v/255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;});
  const lum=(s:string)=>rgb(s).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
  return ['body','.hero p','.card p','.meta','.chip.open','.chip.closed','nav.main a','.logo b','.legend'].flatMap(selector=>Array.from(document.querySelectorAll(selector)).slice(0,3).flatMap(el=>{
   let parent:Element|null=el,bg='rgba(0, 0, 0, 0)';while(parent){bg=getComputedStyle(parent).backgroundColor;if(bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent')break;parent=parent.parentElement;}
   const fg=getComputedStyle(el).color,a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);return ratio<4.5?[{selector,ratio,fg,bg}]:[];
  }));
 });assert.deepEqual(failures,[],'Text contrast below 4.5:1');
}
try {
  // Capture all 16 original routes at desktop and phone widths, with JS off so the same PNGs are compared.
  const nojs=await browser.newContext({javaScriptEnabled:false,colorScheme:'light'});
  const p=await nojs.newPage();
  for(const width of [1280,390]){
    await p.setViewportSize({width,height:900});
    for(const path of paths){
      for(const [kind,base] of [['new',current],['old',baseline]] as const){
        if(!base)continue;
        const response=await p.goto(base+path);assert.equal(response?.status(),200);
        await p.locator('main').first().waitFor();
        await p.evaluate(async()=>{for(const img of document.images)img.loading='eager';await Promise.all(Array.from(document.images).map(img=>img.complete?Promise.resolve():new Promise(r=>{img.onload=r;img.onerror=r;})));assertImages();function assertImages(){if(Array.from(document.images).some(i=>!i.naturalWidth))throw new Error('Broken image');}});
        assert(await p.locator('main').innerText());
        if(kind==='new')assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${kind} ${path} overflow at ${width}`);
        await p.screenshot({path:join(dir,`${kind}-${label(path)}-${width}.png`),fullPage:true});
      }
      records.comparisons.push({path,width,old:!!baseline,new:true});
    }
  }
  await p.goto(current+'/search/');assert.equal(await p.locator('main li').count(),entryCount+2);await nojs.close();passed('JavaScript off: 16 routes render, all PNGs load; no page overflow on desktop/phone');
  const ctx=await browser.newContext({colorScheme:'light',reducedMotion:'reduce'});const page=await ctx.newPage();const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(current);await page.locator('.js').waitFor();await contrast(page);passed('Light theme text contrast: body, cards, labels, chips, links and logo meet 4.5:1');
  // keyboard open/containment/Esc/focus return for both dialogs.
  for(const [opener,dialog] of [['[data-open-search]','#search-dlg'],['[data-open-keys]','#keys-dlg']]){
    await page.locator(opener).focus();await page.keyboard.press('Enter');assert(await page.locator(dialog).evaluate((d:any)=>d.open));
    for(let i=0;i<14;i++){await page.keyboard.press('Tab');assert(await page.locator(dialog).evaluate(d=>d.contains(document.activeElement)||document.activeElement===document.body),`${dialog} focus escaped to ${await page.evaluate(()=>document.activeElement?.outerHTML.slice(0,200))}`);}
    await page.keyboard.press('Escape');assert.equal(await page.locator(dialog).evaluate((d:any)=>d.open),false);assert(await page.locator(opener).evaluate(el=>el===document.activeElement));
  }
  passed('Native search/keys dialogs: keyboard opening, Tab never reaches background controls, Esc, focus return');
  await page.locator('[data-open-keys]').click();await page.locator('[data-single-keys]').uncheck();await page.keyboard.press('Escape');
  await page.keyboard.press('/');await page.keyboard.press('?');await page.keyboard.press('m');assert.equal(await page.locator('dialog[open]').count(),0);assert.equal(await page.locator('html').getAttribute('data-theme'),null);
  await page.keyboard.press('Control+k');assert(await page.locator('#search-dlg').evaluate((d:any)=>d.open));await page.keyboard.press('Escape');
  await page.locator('[data-open-keys]').click();await page.locator('[data-single-keys]').check();await page.keyboard.press('Escape');passed('Single-key off switch stops /, ?, m; Ctrl+K still works');
  await page.keyboard.press('/');await page.locator('#search-input').fill('OCR comparison:');await page.waitForFunction(()=>document.querySelectorAll('#search-results [role=option]').length>0);assert((await page.locator('#search-results').innerText()).includes('OCR comparison:'));await page.keyboard.press('ArrowDown');assert(await page.locator('#search-input').getAttribute('aria-activedescendant'));await page.keyboard.press('Escape');
  passed('Build-time search returns grouped results with combobox selection');
  await page.locator('.filters [name=q]').fill('zz-no-match');assert.equal(await page.locator('.card:visible').count(),0);assert(await page.locator('.no-results').isVisible());await page.locator('[data-clear-filters]').click();assert.equal(await page.locator('.card:visible').count(),entryCount);
  await page.locator('.filters [name=cat]').selectOption('OCR');assert.equal(await page.locator('.card:visible').count(),entries.filter(x=>x.task_type==='ocr').length);assert(new URL(page.url()).searchParams.get('cat')==='OCR');await page.goBack();assert.equal(await page.locator('.card:visible').count(),entryCount);passed('Home filters: query/category URL state, count, no results, clear, Back');
  for(const [name,value] of [['model','Gemma 4 31B'],['open','closed'],['year','2026']]){await page.locator('.filters button[type=reset]').click();await page.locator(`.filters [name=${name}]`).selectOption(value);assert(await page.locator('.card:visible').count()>0);assert.equal(new URL(page.url()).searchParams.get(name),value);}
  passed('Existing model/open/year filters retain URL state and results');
  assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');await page.locator('[data-open-keys]').click();assert.equal(await page.locator('#keys-dlg').evaluate(d=>getComputedStyle(d).animationName),'none');await page.keyboard.press('Escape');
  await page.locator('[data-open-keys]').click();assert.equal(await page.locator('#keys-dlg').evaluate(el=>getComputedStyle(el).animationName),'none');await page.keyboard.press('Escape');passed('Reduced motion: instant scrolling and no dialog animation');
  await page.goto(current+'/coding-agent-token-usage/');
  assert.equal(await page.locator('.body-md img').count(),1);assert(await page.locator('.body-md img').evaluate((i:any)=>i.naturalWidth>0));
  await page.locator('.toc-m summary').click();await page.locator('#results').scrollIntoViewIfNeeded();await page.waitForFunction(()=>!!document.querySelector('.toc-m [aria-current="location"]'));passed('Usage chart loads; server-rendered contents and current-section observer work');
  // Copy: API success, API rejection + legacy success, total failure visible.
  for(const mode of ['success','fallback','failure']){
    await page.evaluate(mode=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{if(mode!=='success')throw new Error('blocked');}}});document.execCommand=()=>mode==='fallback';},mode);
    await page.locator('[data-copy]').click();assert.equal(await page.locator('[data-copy]').innerText(),mode==='failure'?'Copy failed':'Copied');
    if(mode==='failure')assert((await page.locator('#toast').innerText()).includes('select the text'));
    await page.waitForFunction(()=>!document.querySelector('[data-copy]')?.hasAttribute('data-copy-state'));
  }
  passed('Copy: Clipboard API, execCommand fallback and visible failure');
  assert.deepEqual(errors,[]);await ctx.close();
  for(const scheme of ['dark','forced']){
    const c=await browser.newContext({colorScheme:'dark',forcedColors:scheme==='forced'?'active':'none'});const q=await c.newPage();
    for(const path of ['/','/coding-agent-token-usage/']){await q.goto(current+path);if(path==='/'&&scheme==='dark')await contrast(q);await q.screenshot({path:join(dir,`${scheme}-${label(path)}.png`),fullPage:true});}
    await q.goto(current);await q.locator('[data-theme-set=light]').click();assert.equal(await q.locator('html').getAttribute('data-theme'),'light');if(scheme==='dark')assert.equal(await q.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(251, 250, 247)');await c.close();
  }
  passed('Dark and forced-colours screenshots; explicit light overrides dark system');
  const enlarged=await browser.newContext({reducedMotion:'reduce'});const large=await enlarged.newPage();
  for(const width of [1280,390]){await large.setViewportSize({width,height:900});for(const path of paths){await large.goto(current+path);const normal=await large.evaluate(()=>parseFloat(getComputedStyle(document.body).fontSize));await large.addStyleTag({content:'html{font-size:200%}'});const doubled=await large.evaluate(()=>parseFloat(getComputedStyle(document.body).fontSize));assert.equal(doubled,normal*2);assert.equal(await large.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${path} overflows with 200% text at ${width}`);}}
  await large.screenshot({path:join(dir,'text-200-percent-phone.png'),fullPage:true});await enlarged.close();passed('200% browser text: body doubles on 16 routes; no page overflow at desktop/phone widths');
  const blocked=await browser.newContext();await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked');}}));const b=await blocked.newPage();await b.goto(current);await b.locator('[data-theme-set=dark]').click();assert.equal(await b.locator('html').getAttribute('data-theme'),'dark');await b.locator('[data-open-keys]').click();await b.locator('[data-single-keys]').uncheck();await b.keyboard.press('Escape');await b.keyboard.press('/');assert.equal(await b.locator('dialog[open]').count(),0);await b.keyboard.press('Control+k');assert(await b.locator('#search-dlg').evaluate((d:any)=>d.open));await blocked.close();passed('Throwing storage: theme, page, shortcut off switch and Ctrl+K work');
  records.passed=true;
} catch(error) {records.passed=false;records.error=String(error);throw error;}
finally{writeFileSync(join(dir,'release.json'),JSON.stringify(records,null,2));await browser.close();for(const s of servers)s.stop(true);}
