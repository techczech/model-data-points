import sharp, {type OverlayOptions} from 'sharp';
import {getEntries,ROOT} from '../src/lib/content';
import {join} from 'node:path';
import {mkdirSync,existsSync} from 'node:fs';
const raw=join(ROOT,'.check/release'),dest=join(ROOT,'.check/comparisons');mkdirSync(dest,{recursive:true});
const paths=['home','about',...getEntries().map(x=>x.slug)];
const xml=(s:string)=>s.replaceAll('&','&amp;').replaceAll('<','&lt;');
for(const width of [1280,390])for(let offset=0;offset<paths.length;offset+=8){
 const composites:OverlayOptions[]=[];const names=paths.slice(offset,offset+8);
 for(const [i,name] of names.entries()){
  const left=(i%2)*800,top=Math.floor(i/2)*640;
  composites.push({input:Buffer.from(`<svg width="800" height="40"><rect width="800" height="40" fill="white"/><text x="10" y="25" font-family="sans-serif" font-size="15">${xml(name)} — old left, new right (${width}px)</text></svg>`),left,top});
  for(const [j,kind] of ['old','new'].entries()){
   const file=join(raw,`${kind}-${name}-${width}.png`);if(!existsSync(file))continue;
   const meta=await sharp(file).metadata();const h=Math.min(meta.height!,Math.round(width*1.55));
   const image=await sharp(file).extract({left:0,top:0,width:meta.width!,height:h}).resize({width:390,height:595,fit:'inside',background:'white'}).png().toBuffer();
   composites.push({input:image,left:left+j*400,top:top+40});
  }
 }
 await sharp({create:{width:1600,height:Math.ceil(names.length/2)*640,channels:3,background:'#ddd'}}).composite(composites).png().toFile(join(dest,`pages-${width}-${offset/8+1}.png`));
}
const composites:OverlayOptions[]=[];
for(const [i,name] of ['dark-home','dark-coding-agent-token-usage','forced-home','forced-coding-agent-token-usage'].entries()){
 const input=await sharp(join(raw,name+'.png')).resize({width:700,height:1800,fit:'inside'}).png().toBuffer();composites.push({input,left:i*700,top:40});
}
await sharp({create:{width:2800,height:1840,channels:3,background:'white'}}).composite(composites).png().toFile(join(dest,'dark-forced.png'));
console.log('Retained four page comparison sheets (all 16 routes, desktop/phone) and dark/forced-colours sheet.');
