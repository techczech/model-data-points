#!/usr/bin/env python3
"""Curl every public baseline path and the new feed/agent routes; reject soft-404 bodies."""
import concurrent.futures
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent.parent
BASE=sys.argv[1].rstrip('/') if len(sys.argv)>1 else 'https://datapoints.semanticmachines.fyi'
manifest=(ROOT/'docs/urls-model-data-points-baseline.txt').read_text().splitlines()
# Pages consumes _headers as configuration; it has never been a served asset.
urls={('/'+p):p for p in manifest if p!='_headers'}
for p in (ROOT/'site').rglob('*'):
    if not p.is_file(): continue
    rel=str(p.relative_to(ROOT/'site'))
    if rel=='_headers': continue
    urls['/'+rel]=rel
    if rel.endswith('index.html'):
        urls['/'+rel.removesuffix('index.html')]=rel

def check(item):
    path,rel=item
    r=subprocess.run(['curl','--silent','--show-error','--location','--max-time','30','--retry','1','--user-agent','Mozilla/5.0 ModelDataPointsReleaseCheck','--write-out','\n__CHECK__%{http_code}|%{content_type}|%{url_effective}',BASE+path],capture_output=True)
    if r.returncode: return {'path':path,'ok':False,'error':r.stderr.decode(errors='replace')}
    body,meta=r.stdout.rsplit(b'\n__CHECK__',1)
    code,mime,effective=meta.decode().split('|',2)
    expected=(ROOT/'site'/rel).read_bytes()
    same=hashlib.sha256(body).digest()==hashlib.sha256(expected).digest()
    upgraded=False
    if not same and 'text/html' in mime:
        attr=re.compile(rb"((?:href|src)=[\"'])https?://([^\"']+)([\"'])")
        old=list(attr.finditer(expected)); new=list(attr.finditer(body))
        def normalise(data): return attr.sub(lambda m:m.group(0).replace(b'http://',b'https://',1),data)
        # Permit only one-way HTTPS upgrades in URL attributes. Every other byte must match.
        upgraded=(len(old)==len(new) and normalise(expected)==normalise(body) and all(b.group(0)==a.group(0) or (b'http://' in a.group(0) and b.group(0)==a.group(0).replace(b'http://',b'https://',1)) for a,b in zip(old,new)))
    return {'path':path,'status':int(code),'mime':mime,'effective':effective,'matches_build':same,'https_attribute_upgrades_only':upgraded,'ok':code=='200' and (same or upgraded)}
removed=[f'/data/2026-11-17-coding-agent-token-usage-{suffix}.csv' for suffix in ['daily','coverage','weekly-model-token-types']]
def check_removed(path):
    r=subprocess.run(['curl','--silent','--show-error','--max-time','30','--output','/dev/null','--write-out','%{http_code}',BASE+path],capture_output=True,text=True)
    return {'path':path,'status':r.stdout,'ok':r.returncode==0 and r.stdout=='404'}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(check,sorted(urls.items())))
results += [check_removed(path) for path in removed]
failures=[r for r in results if not r['ok']]
report={'base':BASE,'count':len(results),'baseline_public_paths':len([p for p in manifest if p!='_headers']),'failures':failures,'results':results}
out=ROOT/'.check';out.mkdir(exist_ok=True);(out/'live-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{"PASS" if not failures else "FAIL"}: {len(results)} URLs; {len([p for p in manifest if p!='_headers'])} baseline public paths; {len(failures)} failures. HTTP 200 and built bytes required for retained URLs; removed URLs require 404; one-way HTTPS attribute upgrades allowed and reported.')
for r in failures: print(json.dumps(r))
raise SystemExit(bool(failures))
