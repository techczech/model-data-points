"""Small synthetic checks for collector deduplication and the personal-home boundary."""
import csv
import shutil
import subprocess
from decimal import Decimal
import contextlib
import io
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


class CollectorChecks(unittest.TestCase):
    def test_duplicate_usage_and_excluded_home(self):
        with tempfile.TemporaryDirectory(prefix='usage-test-', dir=ROOT) as tmp:
            root = Path(tmp)

            def save(relative, events):
                p = root / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(''.join(json.dumps(e) + '\n' for e in events))
                return p

            claude = dict(timestamp='2000-01-01T00:00:00Z', requestId='request',
                          message=dict(id='message', model='claude-opus-5-5',
                                       usage=dict(input_tokens=10, output_tokens=3, cache_read_input_tokens=50,
                                                  cache_creation=dict(ephemeral_5m_input_tokens=7, ephemeral_1h_input_tokens=2))))
            save('.claude/projects/synthetic/a.jsonl', [claude, claude])
            save('.claude/projects/synthetic/b.jsonl', [claude])
            context = dict(type='turn_context', payload=dict(model='gpt-6.1-sol'))
            event = dict(timestamp='2000-01-01T00:00:01Z', type='event_msg', payload=dict(type='token_count', info=dict(
                total_token_usage=dict(total_tokens=120), last_token_usage=dict(
                    total_tokens=120, input_tokens=100, cached_input_tokens=80, output_tokens=20, reasoning_output_tokens=12))))
            save('.codex/sessions/a.jsonl', [context, event, event])
            save('.codex/archived_sessions/b.jsonl', [context, event])
            save('.codex-t3/archived_sessions/a.jsonl', [context, event])
            excluded = save('.codex-enterprise/sessions/never-read.jsonl', [context, event])
            output = io.StringIO()
            collected = root / '.local-usage/collector.json'
            with patch('sys.argv', ['collect_usage.py', '--output', str(collected)]), patch('os.path.expanduser', return_value=str(root)), patch('builtins.open', wraps=open) as opened:
                with contextlib.redirect_stdout(output):
                    runpy.run_path(str(ROOT / 'scripts/collect_usage.py'), run_name='__main__')
                self.assertNotIn(str(excluded), [str(c.args[0]) for c in opened.call_args_list])
            rows = json.loads(collected.read_text())
            self.assertNotIn("2000-01-01", output.getvalue())
            self.assertEqual(len(rows), 3)
            self.assertEqual(next(r[5:] for r in rows if r[0] == 'claude'), [10, 3, 50, 7, 2, 0, 1])
            for r in rows:
                if r[0] == 'codex':
                    self.assertEqual(r[5:], [20, 20, 80, 0, 0, 12, 1])




class PublicationChecks(unittest.TestCase):
    def test_rejects_dates_and_daily_tables_but_allows_price_checks(self):
        check = runpy.run_path(str(ROOT/'scripts/check-usage-privacy.py'))['errors']
        with tempfile.TemporaryDirectory(prefix='privacy-', dir=ROOT/'.check') as tmp:
            root = Path(tmp)
            for name, content, rejected in [
                ('usage-weekly.csv', 'week,tokens\n2000-01-03,123\n', True),
                ('usage.csv', 'day,tokens\nMonday,123\n', True),
                ('usage.csv', 'day,tokens\n', True),
                ('usage.md', '| Tool | Day | Tokens |\n| --- | --- | --- |', True),
                ('usage.md', '| Day | Tokens |\n| --- | --- |\n| Monday | 123 |', True),
                ('usage.svg', '<g data-week-start="2000-01-03"/>', True),
                ('usage-prices.csv', 'model,checked_date\nmodel,2000-01-01\n', False),
                ('usage-weekly.csv', 'week,tokens\nWeek 1,123\n', False),
            ]:
                path = root/name
                path.write_text(content)
                self.assertEqual(bool(check(path)), rejected, name)

    def test_local_daily_valuation_exports_only_ranked_full_windows(self):
        with tempfile.TemporaryDirectory(prefix='value-', dir=ROOT/'.check') as tmp:
            root = Path(tmp)
            for folder in ['scripts','data','entries','.local-usage']:
                (root/folder).mkdir()
            shutil.copy2(ROOT/'scripts/value-coding-agent-usage.py',root/'scripts/value-coding-agent-usage.py')
            id = '2026-11-17-coding-agent-token-usage'
            (root/f'data/{id}-prices.csv').write_text('model,token_type,usd_per_million\ngpt-6.1-sol,uncached_input,2\nclaude-opus-5-5,uncached_input,3\n')
            daily = root/'.local-usage/input.csv'
            from datetime import date,timedelta
            with daily.open('w') as f:
                writer=csv.writer(f)
                writer.writerow(['tool','date','model','uncached_input','output','cache_read','cache_write_5m_or_codex_write','cache_write_1h','reasoning_included_in_output'])
                for i in range(8):
                    day=date(2000,1,3)+timedelta(weeks=i)
                    writer.writerow(['claude',day,'claude-opus-5-5',(8-i)*1000000,0,0,0,0,0])
                    if i>=5: writer.writerow(['codex',day,'gpt-6.1-sol',1000000,0,0,0,0,0])
            result=subprocess.run(['python3',str(root/'scripts/value-coding-agent-usage.py'),'--daily',str(daily),'--start','2000-01-03','--end','2000-02-27','--headline-start','2000-02-07','--claude-start','2000-01-03','--full-end','2000-02-27'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            summary=json.loads(result.stdout)
            self.assertEqual(Decimal(summary['priced_usd']),Decimal(24))
            self.assertEqual(Decimal(summary['weekly_median']),Decimal(8))
            self.assertEqual(Decimal(summary['claude_only_weekly_median']),Decimal('13.5'))
            with (root/f'data/{id}-weekly.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual([r['week'] for r in rows[:3]],['Week 1','Week 2','Week 3'])
            self.assertEqual([Decimal(r['priced_total_usd']) for r in rows[:3]],[11,8,5])
            self.assertTrue(all(r['codex_list_value_usd']=='' for r in rows[3:]))
            self.assertFalse(any('2000-' in p.read_text() for p in (root/'data').glob('*')))
            outputs = {str(p.relative_to(root)):p.read_bytes() for folder in ['data','entries'] for p in (root/folder).glob('*')}
            result=subprocess.run(['python3',str(root/'scripts/value-coding-agent-usage.py')],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            for name, content in outputs.items(): self.assertEqual((root/name).read_bytes(),content,name)


if __name__ == '__main__':
    unittest.main()
