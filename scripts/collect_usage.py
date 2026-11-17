#!/usr/bin/env python3
"""Aggregate Claude Code and Codex token usage from local session logs.
Output: JSON list of daily rows, no content. Reads only the two supported personal Codex homes."""
import json, glob, os, sys, collections
H = os.path.expanduser('~')
agg = collections.defaultdict(lambda: [0]*7)  # unc_in, out, cache_read, w5, w1, reasoning, calls

def claude(home):
    seen = set()
    for f in glob.glob(home + '/projects/**/*.jsonl', recursive=True):
        try: fh = open(f, errors='ignore')
        except Exception: continue
        for l in fh:
            if '"usage"' not in l: continue
            try: e = json.loads(l)
            except Exception: continue
            m = e.get('message') or {}
            u = m.get('usage'); mo = m.get('model') or ''
            if not isinstance(u, dict) or not mo or mo.startswith('<'): continue
            k = (m.get('id'), e.get('requestId'))
            if k in seen: continue
            seen.add(k)
            cc = u.get('cache_creation') or {}
            w5 = cc.get('ephemeral_5m_input_tokens'); w1 = cc.get('ephemeral_1h_input_tokens')
            if w5 is None and w1 is None: w5, w1 = u.get('cache_creation_input_tokens', 0), 0
            r = agg[('claude', os.path.basename(home), (e.get('timestamp') or '')[:10], e.get('entrypoint') or '', mo)]
            for i, v in enumerate((u.get('input_tokens'), u.get('output_tokens'), u.get('cache_read_input_tokens'), w5, w1, 0, 1)):
                r[i] += v or 0
        fh.close()

def codex(home):
    seen = set()
    files = glob.glob(home + '/sessions/**/*.jsonl', recursive=True) + glob.glob(home + '/archived_sessions/**/*.jsonl', recursive=True)
    for f in files:
        model = ''; origin = ''; prev = None
        try: fh = open(f, errors='ignore')
        except Exception: continue
        for l in fh:
            if 'turn_context' not in l and 'token_count' not in l and 'session_meta' not in l: continue
            try: e = json.loads(l)
            except Exception: continue
            p = e.get('payload') or {}
            if e.get('type') == 'session_meta':
                origin = p.get('originator') or p.get('source') or ''
                if not isinstance(origin, str): origin = json.dumps(origin)[:30]
            elif e.get('type') == 'turn_context':
                model = p.get('model') or model
            elif p.get('type') == 'token_count':
                info = p.get('info') or {}
                tot = info.get('total_token_usage') or {}; last = info.get('last_token_usage') or {}
                t = tot.get('total_tokens')
                if not last or t is None or t == prev: continue
                prev = t
                k = (e.get('timestamp'), t, last.get('total_tokens'))
                if k in seen: continue
                seen.add(k)
                inp = last.get('input_tokens') or 0; cr = last.get('cached_input_tokens') or 0
                cw = last.get('cache_write_input_tokens') or 0
                r = agg[('codex', os.path.basename(home), (e.get('timestamp') or '')[:10], origin, model)]
                for i, v in enumerate((max(inp - cr - cw, 0), last.get('output_tokens'), cr, cw, 0, last.get('reasoning_output_tokens'), 1)):
                    r[i] += v or 0
        fh.close()

for d in sorted(glob.glob(H + '/.claude*')):
    if os.path.isdir(d + '/projects'): claude(d)
for d in (H + '/.codex', H + '/.codex-t3'):
    if 'enterprise' in d: continue
    if os.path.isdir(d + '/sessions') or os.path.isdir(d + '/archived_sessions'): codex(d)
json.dump([list(k) + v for k, v in agg.items()], sys.stdout)
