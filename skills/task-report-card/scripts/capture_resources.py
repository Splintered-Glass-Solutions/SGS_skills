#!/usr/bin/env python3
"""Append one observed local RAM/context sample to a task report JSON."""
import argparse
from datetime import datetime, timezone
import json
import os
import tempfile
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('data', type=Path)
parser.add_argument('--thread-id', required=True)
parser.add_argument('--session-file', type=Path, help='Optional Codex session JSONL with token_count events')
args = parser.parse_args()
point = {'at': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'threadId': args.thread_id}
try:
    vm = subprocess.check_output(['vm_stat'], text=True, timeout=5)
    size = int(re.search(r'page size of (\d+) bytes', vm).group(1))
    free = int(re.search(r'Pages free:\s*(\d+)', vm).group(1))
    file_backed = int(re.search(r'File-backed pages:\s*(\d+)', vm).group(1))
    total = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize'], text=True, timeout=5))
    point.update(ramAvailableGb=round((free + file_backed) * size / 1e9, 3), ramTotalGb=round(total / 1e9, 3))
    try:
        level = int(subprocess.check_output(['sysctl', '-n', 'kern.memorystatus_vm_pressure_level'], text=True, timeout=5))
        point['ramPressure'] = {1: 'normal', 2: 'warning', 4: 'critical'}.get(level, 'unknown')
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
except (OSError, ValueError, AttributeError, subprocess.SubprocessError):
    pass
context_point = None
if args.session_file:
    try:
        latest = None
        with args.session_file.open() as source:
            for line in source:
                try:
                    item = json.loads(line); payload = item.get('payload', {}); info = payload.get('info') if payload.get('type') == 'token_count' else None
                    if info and info.get('model_context_window') and info.get('last_token_usage', {}).get('input_tokens'):
                        latest = (item.get('timestamp'), info['last_token_usage']['input_tokens'], info['model_context_window'])
                except (ValueError, AttributeError, TypeError):
                    continue
        if latest:
            context_point = {'at': latest[0], 'threadId': args.thread_id, 'contextInputTokens': latest[1], 'contextWindowTokens': latest[2]}
    except OSError:
        pass
if 'ramAvailableGb' not in point and context_point is None:
    raise SystemExit('No resource measurement available; report unchanged')
data = json.loads(args.data.read_text())
if not isinstance(data.get('resourceHistory', []), list):
    raise SystemExit('resourceHistory must be an array')
history = data.setdefault('resourceHistory', [])
if 'ramAvailableGb' in point:
    history.append(point)
if context_point and not any(p.get('at') == context_point['at'] and p.get('threadId') == args.thread_id and p.get('contextInputTokens') == context_point['contextInputTokens'] for p in history):
    history.append(context_point)
fd, name = tempfile.mkstemp(prefix='.' + args.data.name + '.', dir=args.data.parent)
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
        out.write('\n')
    os.chmod(name, args.data.stat().st_mode & 0o777)
    os.replace(name, args.data)
finally:
    if os.path.exists(name):
        os.unlink(name)
print('Recorded one resource sample; unavailable measurements omitted.')
