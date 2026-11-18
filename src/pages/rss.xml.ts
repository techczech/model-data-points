import { BASE, NAME, TAGLINE, getEntries, categories } from '../lib/content';
const xml = (s: unknown) => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&apos;');
export function GET() {
  const items = getEntries().map(x => {
    const url = `${BASE}/${x.slug}/`;
    return `<item><title>${xml(x.title)}</title><link>${url}</link><guid isPermaLink="true">${url}</guid><pubDate>${new Date(x.date+'T00:00:00Z').toUTCString()}</pubDate><description>${xml(x.headline)}</description>${categories(x).map(c=>`<category>${xml(c)}</category>`).join('')}</item>`;
  }).join('\n');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>${NAME}</title><link>${BASE}/</link><description>${xml(TAGLINE)}</description><language>en-gb</language><atom:link href="${BASE}/rss.xml" rel="self" type="application/rss+xml"/>${items}</channel></rss>`,{headers:{'Content-Type':'application/rss+xml; charset=utf-8'}});
}
