import {getEntries,ABOUT,NAME,INTRO,BASE} from '../lib/content';
const entries=getEntries();
const index=`# ${NAME}\n\n${INTRO}\n\n`+entries.map(x=>`## [${x.title}](${BASE}/${x.slug}/)\n\n${x.date}\n\n${x.headline}\n`).join('\n');
export function getStaticPaths(){
 const pages=[{path:'index',body:index},{path:'about/index',body:ABOUT.replace(/<h([12])>(.*?)<\/h\1>/g,(_,n,t)=>'\n'+'#'.repeat(Number(n))+' '+t+'\n').replace(/<a href="([^"]*)">(.*?)<\/a>/g,'[$2]($1)').replace(/<[^>]+>/g,'\n').trim()},{path:'search/index',body:'# Search Model Data Points\n\n'+index}];
 for(const x of entries)pages.push({path:`${x.slug}/index`,body:x._source});
 return pages.map(p=>({params:{page:p.path},props:{body:p.body}}));
}
export function GET({props}:{props:{body:string}}){return new Response(props.body,{headers:{'Content-Type':'text/markdown; charset=utf-8'}});}
