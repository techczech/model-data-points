#!/usr/bin/env python3
"""Compatibility entry point: the static site is now built by Astro."""
import os
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
env = os.environ.copy()
if len(sys.argv) > 1:
    env['MDP_ENTRIES_DIR'] = str(Path(sys.argv[1]).resolve())
raise SystemExit(subprocess.call(['bun', 'run', 'build'], cwd=root, env=env))
