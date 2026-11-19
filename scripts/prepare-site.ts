import {spawnSync} from 'node:child_process';
import {cpSync,mkdirSync,rmSync} from 'node:fs';
import {join,basename} from 'node:path';
import {ROOT,getEntries,privacyErrors} from '../src/lib/content';
import {readFileSync} from 'node:fs';
const usagePrivacy=spawnSync('python3',[join(ROOT,'scripts/check-usage-privacy.py')],{encoding:'utf8'});
if(usagePrivacy.status!==0)throw new Error(usagePrivacy.stdout+usagePrivacy.stderr);
const entries=getEntries();
// Publish only source-listed data, never collector output or private session logs.
const data=[...new Set(entries.flatMap(x=>x.sources.filter(s=>s.startsWith('data/'))))];
for(const source of data)if(source.endsWith('.csv')){const errors=privacyErrors(readFileSync(join(ROOT,source),'utf8'),source);if(errors.length)throw new Error(errors.join('\n'));}
const dest=join(ROOT,'.generated/public');rmSync(dest,{recursive:true,force:true});mkdirSync(dest,{recursive:true});
for(const asset of ['style.css','filters.js','copy.js','_headers'])cpSync(join(ROOT,'scripts/assets',asset),join(dest,asset));
for(const source of data){mkdirSync(join(dest,'data'),{recursive:true});cpSync(join(ROOT,source),join(dest,'data',basename(source)));}
console.log(`Prepared ${entries.length} entries and ${data.length} data downloads; validation/privacy passed.`);
