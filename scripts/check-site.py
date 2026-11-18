#!/usr/bin/env python3
"""Validate the built Astro pages, local links, citation contract and RSS 2.0 rules."""
from collections import defaultdict
from datetime import timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site'
BASE = 'https://datapoints.semanticmachines.fyi'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.meta=defaultdict(list); self.links=[]; self.ids=[]; self.canonical=[]; self.feedlinks=[]; self.jsonld=[]; self._json=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='meta': self.meta[a.get('name',a.get('property'))].append(a.get('content'))
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='link' and a.get('type')=='application/rss+xml': self.feedlinks.append(a['href'])
        if tag=='script' and a.get('type')=='application/ld+json': self._json=True
    def handle_data(self,data):
        if self._json: self.jsonld.append(json.loads(data))
    def handle_endtag(self,tag):
        if tag=='script': self._json=False

index=json.loads((OUT/'search-index.json').read_text())
paths=['/','/about/','/search/']+[x['u'] for x in index['items'] if x['s']=='entries']
parsed={}
for path in paths:
    file=OUT/(path.strip('/')+'/index.html' if path!='/' else 'index.html')
    text=file.read_text(); page=Page(text); parsed[path]=page
    title=next(x['t'] for x in index['items'] if x['u']==path)
    if path=='/about/': title='About · Model Data Points'
    if path=='/search/': title='Search · Model Data Points'
    expected={'citation_title':title,'citation_author':'Lukeš, Dominik','citation_public_url':BASE+path,'citation_language':'en','DC.type':'webpage','DC.title':title,'DC.creator':'Lukeš, Dominik','DC.publisher':'Model Data Points','DC.language':'en-GB','og:site_name':'Model Data Points','og:title':title,'og:url':BASE+path}
    for tag,value in expected.items(): assert page.meta[tag]==[value],(path,tag,page.meta[tag])
    assert page.canonical==[BASE+path]
    assert len(page.meta['description'])==1
    date=next((x['date'] for x in index['items'] if x['u']==path and x['s']=='entries'),None)
    assert page.meta['DC.date']==([date] if date else [])
    assert page.meta['citation_publication_date']==([date.replace('-','/')] if date else [])
    assert 'Z3988' not in text and 'citation_journal_title' not in text
    assert 'data-copy="#cite-text"' in text and 'Cite this page' in text
    assert page.feedlinks==['/rss.xml'] and 'Subscribe (RSS)' in text
    assert page.jsonld and page.jsonld[0]['url']==BASE+path
    assert len(page.ids)==len(set(page.ids)),(path,'duplicate ids')
    assert 'main' in page.ids
    if date:
        assert page.meta['og:type']==['article']
        assert 'https://github.com/techczech/model-data-points/blob/main/entries/' in text
    for link in page.links:
        u=urlparse(urljoin(BASE+path,link))
        if u.scheme not in ('http','https') or u.netloc!='datapoints.semanticmachines.fyi': continue
        rel=unquote(u.path).lstrip('/'); target=OUT/rel
        if u.path.endswith('/'): target=target/'index.html'
        assert target.is_file(),(path,link,'missing local target')
        if u.fragment and target.suffix=='.html':
            dest=page if u.path==path else Page(target.read_text())
            assert unquote(u.fragment) in dest.ids,(path,link,'missing fragment')

# RSS 2.0 local validator: well-formed XML, channel requirements, item fields,
# absolute HTTP URLs, unique permanent IDs, RFC 822 dates with UTC timezone,
# self-discovery, full summaries/categories and descending publication order.
feed=ET.parse(OUT/'rss.xml').getroot(); assert feed.tag=='rss' and feed.attrib['version']=='2.0'
channel=feed.find('channel'); assert channel is not None
for key in ('title','link','description','language'): assert channel.findtext(key)
assert channel.find('link').text==BASE+'/'
selflink=channel.find('{http://www.w3.org/2005/Atom}link'); assert selflink.attrib=={'href':BASE+'/rss.xml','rel':'self','type':'application/rss+xml'}
items=channel.findall('item'); expected=[x for x in index['items'] if x['s']=='entries']; assert len(items)==len(expected)
guids=[]; dates=[]
for item,entry in zip(items,expected):
    for key in ('title','link','guid','pubDate','description'): assert item.findtext(key)
    assert item.findtext('title')==entry['t']
    assert item.findtext('description')==entry['d'],'Feed summary was truncated or changed'
    assert item.findtext('link')==BASE+entry['u']
    guid=item.find('guid'); assert guid.attrib['isPermaLink']=='true' and guid.text==item.findtext('link')
    guids.append(guid.text); date=parsedate_to_datetime(item.findtext('pubDate')); assert date.utcoffset().total_seconds()==0; dates.append(date)
    assert [c.text for c in item.findall('category')]==entry['categories']
    assert date.date().isoformat()==entry['date']
assert len(guids)==len(set(guids)) and dates==sorted(dates,reverse=True)
assert (OUT/'llms.txt').is_file()
for path in paths: assert (OUT/path.strip('/')/'index.md').is_file()
print(f'PASS: {len(paths)} Astro pages, citations, canonical/social/agent metadata, local files/anchors; RSS 2.0 with {len(items)} complete summaries.')
