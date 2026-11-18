import { getEntries, BASE } from '../lib/content';
export function GET() {
  return new Response(`# Model Data Points\n\n> Small experiments with AI models: what was tested, on which models, why, and what happened.\n\nMarkdown is the content source. Each data point records models, purpose, context, method, results and caveats.\n\n## Site\n\n- [Entries](${BASE}/index.md)\n- [About](${BASE}/about/index.md)\n- [Search](${BASE}/search/index.md)\n- [RSS](${BASE}/rss.xml)\n- [Public search index](${BASE}/search-index.json)\n\n## Data points\n\n${getEntries().map(x=>`- [${x.title}](${BASE}/${x.slug}/index.md): ${x.headline}`).join('\n')}\n`,{headers:{'Content-Type':'text/plain; charset=utf-8'}});
}
