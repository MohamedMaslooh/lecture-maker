# -*- coding: utf-8 -*-
"""Count the tokens a lecture used, from Claude Code session files. Optional: only where those files
exist (Claude Code, or the desktop app's Code tab). In the Claude app's chat or Cowork, use the
before-and-after reading of Settings > Usage instead (see references/cost-check.md).

    python tally_tokens.py <folder-with-.jsonl> [--sessions id1,id2] [--since 2026-10-01]

<folder> is a project folder under ~/.claude/projects/ (one .jsonl per session, agents in
<session>/subagents/). Each API response is counted once. Prints tokens by model and by kind, and
the share that were cache reads (cheap re-reads of the same context). No prices: on a subscription the
honest bill is a share of your plan, not API dollars.
"""
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import os, sys, json, glob, collections


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


if len(sys.argv) < 2:
    sys.exit(__doc__)
root = os.path.expanduser(sys.argv[1])
want = set((arg('--sessions') or '').split(',')) - {''}
since = arg('--since')

files = []
for p in glob.glob(os.path.join(root, '*.jsonl')):
    sid = os.path.basename(p)[:-6]
    if want and sid not in want:
        continue
    files.append((p, 'main'))
    files += [(q, 'agent') for q in glob.glob(os.path.join(root, sid, 'subagents', '*.jsonl'))]

best = {}
for p, kind in files:
    for line in open(p, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(line)
        except Exception:
            continue
        m = d.get('message')
        if not isinstance(m, dict) or not isinstance(m.get('usage'), dict) or m.get('model') in (None, '<synthetic>'):
            continue
        if since and (d.get('timestamp') or '') < since:
            continue
        k = m.get('id') or d.get('uuid')
        if k not in best or (m['usage'].get('output_tokens') or 0) >= (best[k][2].get('output_tokens') or 0):
            best[k] = (m['model'], kind, m['usage'])

tot = collections.defaultdict(lambda: collections.Counter())
for model, kind, u in best.values():
    c = tot[model]
    c['calls'] += 1
    c['input'] += u.get('input_tokens') or 0
    c['cache write'] += u.get('cache_creation_input_tokens') or 0
    c['cache read'] += u.get('cache_read_input_tokens') or 0
    c['output'] += u.get('output_tokens') or 0
    c['agent calls' if kind == 'agent' else 'main calls'] += 1

grand = collections.Counter()
print('%-28s %7s %12s %12s %14s %10s' % ('model', 'calls', 'input', 'cache write', 'cache read', 'output'))
for model, c in sorted(tot.items(), key=lambda x: -x[1]['cache read']):
    grand.update(c)
    print('%-28s %7d %12s %12s %14s %10s' % (model, c['calls'], f"{c['input']:,}", f"{c['cache write']:,}",
                                              f"{c['cache read']:,}", f"{c['output']:,}"))
alltok = grand['input'] + grand['cache write'] + grand['cache read'] + grand['output']
print('\nall tokens %s in %d calls (%d by agents); cache reads %.0f%%' % (
    f'{alltok:,}', grand['calls'], grand['agent calls'], 100 * grand['cache read'] / alltok if alltok else 0))
print('Anthropic publishes no token quota for its plans: compare with Settings > Usage, and label any share an estimate.')
