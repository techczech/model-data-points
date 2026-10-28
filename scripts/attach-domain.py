#!/usr/bin/env python3
"""One-off: attach datapoints.semanticmachines.fyi to the Pages project and add its proxied CNAME.
Token from env CLOUDFLARE_API_TOKEN only (inject with bws run). Creates; never edits or deletes existing records."""
import json, os, urllib.request, urllib.error
ACCOUNT = "b6ae5bced06492ee6f0c8f92776804da"
PROJECT, ZONE, HOST = "model-data-points", "semanticmachines.fyi", "datapoints.semanticmachines.fyi"
TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]

def api(method, path, body=None):
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/" + path, method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e: return json.load(e)

doms = api("GET", f"accounts/{ACCOUNT}/pages/projects/{PROJECT}/domains")
if any(d["name"] == HOST for d in doms.get("result") or []):
    print("pages domain: already attached")
else:
    r = api("POST", f"accounts/{ACCOUNT}/pages/projects/{PROJECT}/domains", {"name": HOST})
    print("pages domain:", r.get("success"), r.get("errors"))
zone = api("GET", f"zones?name={ZONE}")["result"][0]["id"]
existing = api("GET", f"zones/{zone}/dns_records?name={HOST}")["result"]
if existing:
    print("dns: record exists, not touched:", [(x["type"], x["content"]) for x in existing])
else:
    r = api("POST", f"zones/{zone}/dns_records", {"type": "CNAME", "name": "datapoints", "content": f"{PROJECT}.pages.dev", "proxied": True, "ttl": 1})
    print("dns:", r.get("success"), r.get("errors"))
