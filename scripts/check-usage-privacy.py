#!/usr/bin/env python3
"""Fail publication when usage data exposes dates, daily rows or machine coverage."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISO_DATE = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')


def errors(path):
    text = path.read_text()
    problems = []
    if re.search(r'-(daily|coverage|weekly-model-token-types)\.', path.name):
        problems.append('daily, coverage and weekly/model usage tables are private')
    if path.suffix == '.csv':
        reader = csv.DictReader(text.splitlines())
        for column in reader.fieldnames or []:
            if re.search(r'(^|_)(day|daily|date|timestamp|first|last)(_|$)', column, re.I):
                if not (path.name.endswith('-prices.csv') and column == 'checked_date'):
                    problems.append('per-day or dated usage column: '+column)
        rows = list(reader)
        for row in rows:
            for column, value in row.items():
                if column is None:
                    problems.append('malformed CSV row')
                    continue
                if ISO_DATE.search(value or '') and not (path.name.endswith('-prices.csv') and column == 'checked_date'):
                    problems.append('ISO date in usage column: '+column)
    elif ISO_DATE.search(text):
        problems.append('ISO date in usage asset')
    if re.search(r'^\s*\|[^\n]*\|?\s*(day|daily|date)\s*\|', text, re.I | re.M) or re.search(r'<th[^>]*>\s*(day|daily|date)\s*</th>', text, re.I):
        problems.append('per-day table')
    return sorted(set(problems))


def main():
    failures = []
    for path in sorted((ROOT/'data').glob('*usage*')):
        if path.is_file():
            failures.extend(f'{path.name}: {e}' for e in errors(path))
    if failures:
        raise SystemExit('\n'.join(failures))
    print('Usage publication privacy: ranked undated weeks and whole-window totals only.')


if __name__ == '__main__':
    main()
