import {test,expect} from 'bun:test';
import {mkdtempSync,writeFileSync,rmSync,readFileSync,mkdirSync,cpSync,readdirSync} from 'node:fs';
import {join} from 'node:path';
import {getEntries,parseEntry,renderMarkdown,ROOT} from '../src/lib/content';
mkdirSync(join(ROOT,'.check'),{recursive:true});
const original=readFileSync(join(ROOT,'entries/2026-03-08-local-image-generation-m4-max.md'),'utf8');
function fixture(text:string,run:(path:string,dir:string)=>void){const dir=mkdtempSync(join(ROOT,'.check/fixture-'));try{const path=join(dir,'2026-03-08-local-image-generation-m4-max.md');writeFileSync(path,text);run(path,dir);}finally{rmSync(dir,{recursive:true,force:true});}}
test('all canonical entries and date-free slugs load, preserving order and legacy scalars',()=>{const entries=getEntries();expect(entries.length).toBe(readdirSync(join(ROOT,'entries')).filter(n=>n.endsWith('.md')).length);expect(entries.some(x=>x.slug==='coding-agent-token-usage')).toBe(true);expect(entries.find(x=>x.slug==='computer-use-haiku-terra-luna')!.results.rows[3][3]).toBe('1.0');});
test('required fields, id shape/match, date, enums, model booleans/access, results widths and lists reject malformed content',()=>{
 for(const [from,to] of [['title:','missing_title:'],['2026-03-08-local-image-generation-m4-max','wrong-id'],['date: 2026-03-08','date: 2026-02-30'],['task_type: image-generation','task_type: unknown'],['status: complete','status: pending'],['open_weights: true','open_weights: "true"'],['access: local','access: browser'],['columns: [Model, Quantisation, Resolution, Steps, Time]','columns: [One]'],['sources: []','sources: wrong'],['caveats:','missing_caveats:']])fixture(original.replace(from,to),path=>expect(()=>parseEntry(path)).toThrow());
});
test('private paths, script URLs and missing/local-traversal source files fail with useful errors',()=>{
 for(const extra of ['/Users/private/file','~/private','/home/private','C:\\private','javascript:evil()','DATA:TEXT/HTML,x'])fixture(original+'\n'+extra,path=>expect(()=>parseEntry(path)).toThrow(/contains/));
 for(const source of ['data/missing.csv','../README.md'])fixture(original.replace('sources: []',`sources: [${source}]`),path=>expect(()=>parseEntry(path)).toThrow(/source file/));
});
test('malformed frontmatter, models and results fail; duplicate/reserved slugs fail before output',()=>{
 for(const text of ['no YAML','---\n- a\n---',original.replace('results:','unused_results:'),original.replace('models:','unused_models:')])fixture(text,path=>expect(()=>parseEntry(path)).toThrow());
 fixture(original,(path,dir)=>{const other='2026-03-09-local-image-generation-m4-max';writeFileSync(join(dir,other+'.md'),original.replaceAll('2026-03-08-local-image-generation-m4-max',other));expect(()=>getEntries(dir)).toThrow(/duplicate slug/);});
 fixture(original,(path,dir)=>{rmSync(path);writeFileSync(join(dir,'2026-03-08-about.md'),original.replaceAll('2026-03-08-local-image-generation-m4-max','2026-03-08-about'));expect(()=>getEntries(dir)).toThrow(/reserved/);});
});
test('Markdown keeps tables, fenced code, images and escapes authored HTML and unsafe URLs',()=>{const html=renderMarkdown('| A | B |\n| - | - |\n| 1 | 2 |\n\n```js\na < b\n```\n\n<script>bad()</script>\n\n![chart](../data/chart.svg)\n\n[x](javascript:evil)');expect(html).toContain('<table>');expect(html).toContain('<pre>');expect(html).toContain('src="../data/chart.svg"');expect(html).not.toContain('<script>');expect(html).not.toContain('href="javascript:');});
test('usage valuation regenerates the frozen entry, CSVs and chart unchanged in an isolated fixture',()=>{
 const tmp=mkdtempSync(join(ROOT,'.check/usage-value-'));try{
  for(const d of ['scripts','data','entries'])mkdirSync(join(tmp,d));
  cpSync(join(ROOT,'scripts/value-coding-agent-usage.py'),join(tmp,'scripts/value-coding-agent-usage.py'));
  const id='2026-11-17-coding-agent-token-usage';
  for(const suffix of ['prices','weekly','model-token-types','full-record-model-token-types','window-totals'])cpSync(join(ROOT,`data/${id}-${suffix}.csv`),join(tmp,`data/${id}-${suffix}.csv`));
  const result=Bun.spawnSync(['python3',join(tmp,'scripts/value-coding-agent-usage.py')]);expect(result.exitCode).toBe(0);
  for(const suffix of ['model-token-types.csv','full-record-model-token-types.csv','window-totals.csv','weekly.csv','weekly.svg'])expect(readFileSync(join(tmp,`data/${id}-${suffix}`))).toEqual(readFileSync(join(ROOT,`data/${id}-${suffix}`)));
  expect(readFileSync(join(tmp,`entries/${id}.md`))).toEqual(readFileSync(join(ROOT,`entries/${id}.md`)));
 }finally{rmSync(tmp,{recursive:true,force:true});}
});
