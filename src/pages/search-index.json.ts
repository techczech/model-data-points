import { getEntries, NAME, TAGLINE, ABOUT, categories } from '../lib/content';
export function GET() {
  return Response.json({sections:[{slug:'entries',name:'Entries',href:'/'},{slug:'pages',name:'Pages',href:'/search/'}],items:[...getEntries().map(x=>({s:'entries',date:x.date,categories:categories(x),t:x.title,d:x.headline,u:`/${x.slug}/`,k:[x._body,x.task_type,...x.models.map(m=>m.name)].filter(Boolean).join(' '),x:`https://github.com/techczech/model-data-points/blob/main/entries/${x.id}.md`})),{s:'pages',t:NAME,d:TAGLINE,u:'/'},{s:'pages',t:'About Model Data Points',d:'How the series works, its inspiration and how to check the research.',u:'/about/',k:ABOUT},{s:'pages',t:'Search Model Data Points',d:'Browse entries and site pages.',u:'/search/'}]});
}
