#!/usr/bin/env python3
"""Rebuild the frozen usage entry from anonymous CSVs; standard library only."""
import argparse
import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
ID = '2026-11-17-coding-agent-token-usage'
ANTHROPIC = 'https://platform.claude.com/docs/en/about-claude/pricing'
OPENAI = 'https://developers.openai.com/api/docs/models/'
FIELDS = ['uncached_input', 'output', 'cache_read', 'cache_write_5m_or_codex_write', 'cache_write_1h']
TYPES = {'claude': ['uncached_input', 'output', 'cache_read', 'cache_write_5m', 'cache_write_1h'],
         'codex': ['uncached_input', 'output', 'cached_input', 'cache_write', None]}
LABELS = {'uncached_input': 'Uncached input', 'output': 'Output',
          'cache_read': 'Cache reads', 'cached_input': 'Cached input',
          'cache_write_5m': 'Cache writes, 5 minutes', 'cache_write_1h': 'Cache writes, 1 hour',
          'cache_write': 'Cache writes (none recorded)'}


def read(suffix):
    with (ROOT / f'data/{ID}-{suffix}.csv').open() as f:
        return list(csv.DictReader(f))


def write(suffix, header, rows):
    with (ROOT / f'data/{ID}-{suffix}.csv').open('w') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        w.writerows(rows)


def money(v):
    return f'${v:,.2f}'


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, r)) + ' |' for r in rows])


def aggregates(rows):
    result = {}
    for r in rows:
        result[(r['tool'], r['model'], r['token_type'])] = [
            int(r['tokens']), Decimal(r['list_value_usd'] or '0'), int(r['unpriced_tokens'])]
    return result


def private_inputs(args, rates, known_models):
    # Explicit dates are local command arguments, never frozen in public source.
    start, end, headline_start, claude_start, full_end = map(date.fromisoformat,
        [args.start, args.end, args.headline_start, args.claude_start, args.full_end])
    assert start <= claude_start <= headline_start <= full_end <= end
    assert headline_start.weekday() == claude_start.weekday() == 0 and full_end.weekday() == 6
    with args.daily.open() as f:
        daily = list(csv.DictReader(f))
    total = defaultdict(lambda: [0, Decimal(0), 0])
    full = defaultdict(lambda: [0, Decimal(0), 0])
    weekly = defaultdict(lambda: [0, Decimal(0), 0])
    for r in daily:
        tool, model, day = r['tool'], r['model'], date.fromisoformat(r['date'])
        assert start <= day <= end and model in known_models
        assert int(r['reasoning_included_in_output']) <= int(r['output'])
        week = day - timedelta(days=day.weekday())
        for field, kind in zip(FIELDS, TYPES[tool]):
            n = int(r[field])
            assert n >= 0
            if kind is None:
                assert n == 0
                continue
            rate = rates.get((model, kind))
            value = n * rate / 1_000_000 if rate is not None else Decimal(0)
            destinations = [((tool, model, kind), total), ((week, tool, model, kind), weekly)]
            if headline_start <= day <= full_end:
                destinations.append(((tool, model, kind), full))
            for key, dest in destinations:
                dest[key][0] += n
                dest[key][1] += value
                dest[key][2] += n if rate is None else 0
    weeks = []
    day = start - timedelta(days=start.weekday())
    while day <= end:
        vals = {tool: sum((v[1] for k, v in weekly.items() if k[0] == day and k[1] == tool), Decimal(0)) for tool in TYPES}
        nt = sum(v[0] for k, v in weekly.items() if k[0] == day)
        nu = sum(v[2] for k, v in weekly.items() if k[0] == day)
        cv = sum((v[1] for k, v in weekly.items() if k[0] == day and k[3] not in ('uncached_input', 'output')), Decimal(0))
        claude_coverage = ('partial_current_week' if day > full_end else
                           'full' if day >= claude_start else
                           'fragmentary' if nt else 'no_retained_records')
        codex_coverage = ('partial_current_week' if day > full_end else
                          'full' if day >= headline_start else
                          'partial_first_week' if day <= headline_start <= day + timedelta(days=6) else
                          'no_retained_records')
        weeks.append((day, min(day + timedelta(days=6), end), 'in_progress' if day > full_end else 'finished_calendar_week',
                      vals['claude'], vals['codex'], vals['claude'] + vals['codex'], cv, nt, nu,
                      headline_start <= day <= full_end, claude_start <= day <= full_end,
                      claude_coverage, codex_coverage))
        day += timedelta(days=7)

    return total, full, publish_weeks(weeks, weekly)


def publish_weeks(weeks, weekly):
    rows = []
    for window, flag, value_index in [('both_tools', 9, 5), ('claude_only', 10, 3)]:
        selected = sorted([w for w in weeks if w[flag]], key=lambda w: w[value_index], reverse=True)
        for rank, w in enumerate(selected, 1):
            if window == 'both_tools':
                values = list(w[3:9])
            else:
                kept = [v for k, v in weekly.items() if k[0] == w[0] and k[1] == 'claude']
                cache = sum((v[1] for k,v in weekly.items() if k[0] == w[0] and k[1] == 'claude' and k[3] not in ('uncached_input','output')), Decimal(0))
                values = [w[3], '', w[3], cache, sum(v[0] for v in kept), sum(v[2] for v in kept)]
            rows.append([window, f'Week {rank}'] + values)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--daily', type=Path, help='Ignored local daily CSV; never copied to public data')
    for name in ['start', 'end', 'headline-start', 'claude-start', 'full-end']:
        parser.add_argument('--'+name, help='Local coverage boundary for a fresh collection')
    args = parser.parse_args()
    prices = read('prices')
    rates = {(p['model'], p['token_type']): Decimal(p['usd_per_million']) for p in prices if p['usd_per_million']}
    known_models = {p['model'] for p in prices}
    if args.daily:
        if not all([args.start, args.end, args.headline_start, args.claude_start, args.full_end]):
            parser.error('--daily requires all five local coverage boundaries')
        if (ROOT/'data').resolve() in args.daily.resolve().parents:
            parser.error('Daily inputs must be outside public data/')
        total, full, public_weeks = private_inputs(args, rates, known_models)
        for suffix, values in [('model-token-types', total), ('full-record-model-token-types', full)]:
            write(suffix, ['tool','model','token_type','tokens','usd_per_million','list_value_usd','unpriced_tokens'],
                [list(k)+[v[0],rates.get((k[1],k[2]),''),format(v[1],'.6f') if (k[1],k[2]) in rates else '',v[2]] for k,v in sorted(values.items())])
        write('window-totals', ['window','tokens','priced_value_usd','unpriced_tokens','cached_value_usd'],
            [[name,sum(v[0] for v in data.values()),sum((v[1] for v in data.values()),Decimal(0)),sum(v[2] for v in data.values()),sum((v[1] for k,v in data.items() if k[2] not in ('uncached_input','output')),Decimal(0))] for name,data in [('both_tools',full),('all_retained',total)]])
        write('weekly', ['window','week','claude_list_value_usd','codex_list_value_usd','priced_total_usd','cached_value_usd','all_tokens','unpriced_tokens'], public_weeks)
    else:
        total = aggregates(read('model-token-types'))
        full = aggregates(read('full-record-model-token-types'))
    weeks = []
    for r in read('weekly'):
        values = [Decimal(r[k] or '0') for k in ['claude_list_value_usd','codex_list_value_usd','priced_total_usd','cached_value_usd']]
        weeks.append((r['week'], None, None, *values, int(r['all_tokens']), int(r['unpriced_tokens']), r['window']=='both_tools', r['window']=='claude_only'))
    headline_weeks = sorted([w for w in weeks if w[9]], key=lambda w:w[5], reverse=True)
    claude_weeks = sorted([w for w in weeks if w[10]], key=lambda w:w[3], reverse=True)
    assert len(headline_weeks) == 3 and len(claude_weeks) == 8
    summaries = {r['window']:r for r in read('window-totals')}
    dollars = Decimal(summaries['both_tools']['priced_value_usd'])
    tokens = sum(v[0] for v in full.values())
    unpriced = sum(v[2] for v in full.values())
    cache_value = Decimal(summaries['both_tools']['cached_value_usd'])
    cache_share = cache_value / dollars * 100
    full_median = median(w[5] for w in headline_weeks)
    full_mean = dollars / len(headline_weeks)
    claude_median = median(w[3] for w in claude_weeks)
    models = sorted({k[1] for k in total}, key=lambda m: sum(v[1] for k, v in total.items() if k[1] == m), reverse=True)
    full_models = sorted({k[1] for k in full}, key=lambda m: sum(v[1] for k, v in full.items() if k[1] == m), reverse=True)
    by_model = [[m, f'{sum(v[0] for k, v in full.items() if k[1] == m):,}',
                 money(sum((v[1] for k, v in full.items() if k[1] == m), Decimal(0)))
                 if any(k[0] == m for k in rates) else 'Unpriced'] for m in full_models]
    tool_rows = []
    for tool, label in [('claude', 'Claude Code'), ('codex', 'Codex'), (None, 'Combined')]:
        rows = [v for k, v in full.items() if tool is None or k[0] == tool]
        tool_rows.append(['Three consecutive full weeks; both tools', label, f'{sum(v[0] for v in rows):,}', money(sum((v[1] for v in rows), Decimal(0))), f'{sum(v[2] for v in rows):,}'])
    retained_dollars = Decimal(summaries['all_retained']['priced_value_usd'])
    retained_unpriced = sum(v[2] for v in total.values())
    tool_rows.append(['All retained logs; includes fragmentary periods and current partial week', 'Combined',
                      f'{sum(v[0] for v in total.values()):,}', money(retained_dollars), f'{retained_unpriced:,}'])
    caveats = [
        'One heavy user (n=1); this is a usage record, not a representative benchmark or a productivity measure.',
        'Local logs only, collected across several machines. Web and desktop chat use and unavailable sources are excluded.',
        'List-price value is not what was paid; subscriptions were used. These are current standard short-context API token rates, not reconstructed historical bills.',
        'Codex output tokens include reasoning. Reasoning is retained as an informational subset and is never added to output a second time.',
        'Earlier retained logs are fragmentary and excluded from the weekly chart and medians.',
        'Codex retention begins later than Claude retention despite earlier use; its first partially covered week is excluded from the combined window.',
        'The partial week at collection is excluded from the chart and both analysis windows. Weekly grouping uses recorded timestamps without local-time conversion; public weeks are ranked by value, not time.',
        'Deduplication is per tool home on each machine. Claude uses message ID and request ID; Codex uses timestamp, cumulative total and last-usage total across session files. Copies across homes or machines cannot be deduplicated from these daily aggregates.',
        'Codex model attribution uses the latest turn context, not a verified server-side response model. The codex-auto-review label has no public API list price found and is left unpriced.',
        'The collector keeps the first Claude usage record for each message/request pair; later streaming updates to the same pair are not merged. Incomplete usage records could understate output.',
        'Daily aggregates do not retain per-request context length or processing tier. Long-context surcharges, fast or ultrafast premiums, regional uplifts and non-token tool charges are excluded. Haiku 5.5 uses the base rate for prompts up to 100,000 tokens.',
    ]
    sources = [f'data/{ID}-{s}.csv' for s in ['prices', 'window-totals', 'full-record-model-token-types', 'model-token-types', 'weekly']]
    sources += [f'data/{ID}-weekly.svg', 'scripts/collect_usage.py', 'scripts/value-coding-agent-usage.py', f'design/{ID}-method.md', ANTHROPIC]
    sources += [OPENAI + m for m in models if m.startswith('gpt-')]
    sources += ['https://alignment.openai.com/auto-review/']
    fm = dict(id=ID, title="One heavy user's coding-agent token usage, ranked full weeks", date='2026-11-17', task_type='coding',
        models=[dict(name=m, provider='Anthropic' if m.startswith('claude-') else 'OpenAI', open_weights=False, access='cli', version=m) for m in models],
        purpose='Measure retained Claude Code and Codex token usage by model and token type, including cached tokens, and value it at public API list prices.',
        context='One heavy user across several machines. No session text or account identifiers are published.',
        method='Use three consecutive full weeks for both tools; separately report Claude Code over eight full weeks. Publish each window ranked by value, with no chronological ordering or dates. Value disjoint token categories at standard short-context API rates checked on 17 November; leave unknown prices blank. All-retained totals are secondary.',
        headline=f'Three consecutive full weeks: {money(dollars)} of priced API-equivalent value across three full weeks; median {money(full_median)}/week, mean {money(full_mean)}/week, {cache_share:.2f}% from cached categories.',
        results=dict(columns=['Window', 'Tool', 'Recorded tokens (including unpriced)', 'Priced API-equivalent value (USD)', 'Unpriced tokens'], rows=tool_rows),
        caveats=caveats, suggests='Cached tokens account for much of this workload and must be included in any API-rate comparison. These logs describe the volume and model mix of one user; they do not measure output quality, productivity or subscription savings.',
        status='partial', sources=sources)
    # JSON values are valid YAML; keep the date a YAML date for the validator.
    del fm['date']
    front = 'date: 2026-11-17\n' + '\n'.join(f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in fm.items())
    body = f'''\n## Both tools: three consecutive full weeks

Both tools have full retained records for **three consecutive full weeks**. Their combined priced value is **{money(dollars)}**, with a **median of {money(full_median)} per week** and a **mean of {money(full_mean)} per week**. This window contains **{tokens:,} recorded tokens**, including **{unpriced:,} unpriced tokens**. Unpriced usage is excluded from dollar amounts throughout.

{table(['Ranked week', 'Claude Code (USD)', 'Codex priced (USD)', 'Combined priced (USD)'], [[w[0], money(w[3]), money(w[4]), money(w[5])] for w in headline_weeks])}

The top chart panel shows these three weeks. The lower panel shows the separate Claude-only window; it does not treat missing Codex records as zero use. The [weekly CSV](https://github.com/techczech/model-data-points/blob/main/data/{ID}-weekly.csv) lists each window separately, ranked by value in descending order. Week labels are ranks within each window, not calendar positions; the two panels do not share week identities.

![Top: both tools, three consecutive full weeks. Bottom: Claude Code only, eight full weeks. Each panel is ranked by value; exact values are in the tables.](../data/{ID}-weekly.svg)

## Claude Code only: eight full weeks

The secondary window includes **eight full weeks of Claude Code records**, with a **median of {money(claude_median)} per week**. Claude's earlier default 30-day log cleanup left sparse records before retention was increased. Codex was in use before its first retained record, so this longer window makes no claim about combined usage.

{table(['Ranked week', 'Claude Code (USD)'], [[w[0], money(w[3])] for w in claude_weeks])}

## Models: three consecutive full weeks

{table(['Logged model', 'Tokens (including cached)', 'Priced value (USD)'], by_model)}

## Token types: three consecutive full weeks

Each row is a disjoint billing category. Cache value means cache reads plus writes and Codex cached input, divided by priced value: **{money(cache_value)} / {money(dollars)} = {cache_share:.2f}%**. It is the value assigned to cached categories, not a claim about money saved.

{table(['Tool', 'Token type', 'Tokens', 'Priced value (USD)', 'Unpriced tokens'], [[tool, LABELS[kind], f'{sum(v[0] for k,v in full.items() if k[0]==tool and k[2]==kind):,}', money(sum((v[1] for k,v in full.items() if k[0]==tool and k[2]==kind), Decimal(0))), f'{sum(v[2] for k,v in full.items() if k[0]==tool and k[2]==kind):,}'] for tool in TYPES for kind in TYPES[tool] if kind])}

The [full-record model/token-type CSV](https://github.com/techczech/model-data-points/blob/main/data/{ID}-full-record-model-token-types.csv) gives the complete tool × model × token-type split for the three consecutive full weeks, including separate cached categories. The [all-retained model/token-type CSV](https://github.com/techczech/model-data-points/blob/main/data/{ID}-model-token-types.csv) includes fragmentary periods and the current partial week. Blank prices and values mean unpriced, not free. Weekly and token-type dollar totals sum priced models only.

## Pricing and reconstruction

All rates are USD per million tokens, checked **17 November 2026**. The [rate CSV](https://github.com/techczech/model-data-points/blob/main/data/{ID}-prices.csv) records each model, token type, rate, source URL and check date. Claude prices come from [Anthropic's model pricing](https://platform.claude.com/docs/en/about-claude/pricing). OpenAI prices come from the official model pages for [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [Terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra), [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) and [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna).

Claude cache writes use 1.25 times input for five-minute retention and twice input for one-hour retention. When the logs omit that split, the collector assigns the aggregate creation count to five-minute writes. No Codex cache writes were recorded. Haiku 4.5's dated ID maps to the public Haiku 4.5 rate. No other older models appear.

The checked Fable 5.1 cache-read rate is **$0.25 per million**. Across all retained logs, using $1 instead, as in the initial pricing brief, would add **{money(sum(v[0] for k,v in total.items() if k[1]=='claude-fable-5-1' and k[2]=='cache_read') * Decimal('0.75') / 1_000_000)}**, bringing that secondary total to **{money(retained_dollars + sum(v[0] for k,v in total.items() if k[1]=='claude-fable-5-1' and k[2]=='cache_read') * Decimal('0.75') / 1_000_000)}**. All reported values use the checked public price.

The label `codex-auto-review` accounts for **{unpriced:,} unpriced tokens in the three-week headline window** and **{retained_unpriced:,} across all retained logs**. No public API price was found for that exact label on the pricing or model pages checked. OpenAI [describes auto-review](https://alignment.openai.com/auto-review/) as a separate approval agent; that does not establish the underlying model for these records, so no substitute model price is assigned.

The public reconstruction inputs are ranked, undated weekly values and whole-window model/token-type totals. Run `python3 scripts/value-coding-agent-usage.py` to regenerate the derived CSVs, chart and this entry, then `uv run scripts/build-site.py` to build the page. The collector is supplied for inspecting the method; it reads local logs and should not be used to publish its unsanitised JSON output. Fresh daily inputs remain in ignored local storage; public outputs contain only ranked, undated weeks and whole-window totals. Folders, entrypoints, origins, project paths and session content are excluded.
'''
    (ROOT / f'entries/{ID}.md').write_text('---\n' + front + '\n---\n' + body)
    chart(headline_weeks + claude_weeks)
    print(json.dumps(dict(tokens=tokens, priced_usd=str(dollars), weekly_median=str(full_median), weekly_mean=str(full_mean),
                         claude_only_weekly_median=str(claude_median), cache_share=str(cache_share), unpriced_tokens=unpriced,
                         all_retained_priced_usd=str(retained_dollars),
                         top_models=by_model[:5]), indent=2))


def chart(weeks):
    width, height, left, plot_h = 900, 620, 78, 180
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Weekly API-equivalent value in full-record windows</title>',
           '<desc id="desc">Top: three consecutive full weeks for both tools, stacked by tool. Bottom: eight full weeks for Claude Code only. Each panel is independently ranked by value, descending, with no time axis. Orange is Codex priced value and blue is Claude Code. Earlier fragmentary weeks, missing records and the current partial week are excluded. Exact ranked values are in the weekly CSV.</desc>',
           f'<rect width="{width}" height="{height}" fill="white"/>', '<g font-family="sans-serif" font-size="12" fill="#172b40">']
    panels = [('headline', 0, [w for w in weeks if w[9]], 'Both tools: three consecutive full weeks (ranked by value)', 5),
              ('claude_only', 305, [w for w in weeks if w[10]], 'Claude Code only: eight full weeks (ranked by value)', 3)]
    for window, offset, selected, title, value_index in panels:
        top = offset + 60
        peak = max(w[value_index] for w in selected) * Decimal('1.12')
        step = (width - left - 20) / len(selected)
        out += [f'<g data-window="{window}">',
                f'<text x="78" y="{offset+22}" font-size="15" font-weight="bold">{title}</text>',
                f'<text x="78" y="{offset+42}">Standard short-context API value (USD); unpriced tokens excluded</text>']
        for i in range(5):
            y = top + plot_h * (1 - i/4)
            out += [f'<path d="M{left} {y}H880" stroke="#d9e0e7"/>', f'<text x="70" y="{y+4}" text-anchor="end">${peak*i/4:,.0f}</text>']
        for i, w in enumerate(selected):
            x = left + i * step + step * .2
            bar_width = step * .6
            base = top + plot_h
            out.append(f'<g data-week-rank="{w[0]}">')
            values = [(w[3], '#2366a8', 'Claude Code')]
            if window == 'headline':
                values.append((w[4], '#cf661a', 'Codex (priced models)'))
            for value, colour, tool in values:
                h = float(value / peak) * plot_h
                base -= h
                out.append(f'<rect x="{x:.2f}" y="{base:.2f}" width="{bar_width:.2f}" height="{h:.2f}" fill="{colour}"><title>{w[0]}, {tool}: {money(value)}</title></rect>')
            out += [f'<text x="{x+bar_width/2:.2f}" y="{base-7:.2f}" text-anchor="middle">${w[value_index]:,.0f}</text>',
                    f'<text x="{x+bar_width/2:.2f}" y="{top+plot_h+23}" text-anchor="middle">{w[0]}</text>', '</g>']
        out.append('</g>')
    out += ['<rect x="78" y="278" width="12" height="12" fill="#2366a8"/><text x="97" y="289">Claude Code</text>',
            '<rect x="210" y="278" width="12" height="12" fill="#cf661a"/><text x="229" y="289">Codex (priced models)</text>',
            '<text x="78" y="605">Both panels exclude fragmentary periods and the partial week at collection.</text>', '</g></svg>']
    (ROOT / f'data/{ID}-weekly.svg').write_text('\n'.join(out))


if __name__ == '__main__':
    main()
