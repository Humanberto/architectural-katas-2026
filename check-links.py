#!/usr/bin/env python3
"""
Check every relative markdown link in a repo: does the file exist,
and does the #anchor match a heading in it?

Usage:  python check-links.py            (from the repo root)
        python check-links.py path/to/repo
"""
import os, re, sys, unicodedata

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
FENCE = re.compile(r'^```')

def slug(text):
    """GitHub's heading -> anchor rules."""
    t = text.strip().lower()
    t = re.sub(r'`([^`]*)`', r'\1', t)                  # strip code ticks
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)      # link text only
    t = re.sub(r'[*_~]', '', t)                          # emphasis
    t = unicodedata.normalize('NFKD', t)
    t = re.sub(r'[^\w\s-]', '', t)                       # drop punctuation
    t = t.strip().replace(' ', '-')
    return t

def headings(path):
    out, in_fence = set(), False
    try:
        lines = open(path, encoding='utf-8').read().splitlines()
    except (OSError, UnicodeDecodeError):
        return out
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            out.add(slug(m.group(2)))
    return out

md_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules')]
    for f in filenames:
        if f.lower().endswith('.md'):
            md_files.append(os.path.join(dirpath, f))

heading_cache, problems, checked = {}, [], 0

for src in sorted(md_files):
    text = open(src, encoding='utf-8').read()
    # blank out fenced code so mermaid contents are not scanned
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    for label, target in LINK.findall(text):
        if target.startswith(('http://', 'https://', 'mailto:')):
            continue
        checked += 1
        path_part, _, anchor = target.partition('#')
        if path_part == '':
            dest = src                                   # same-file anchor
        else:
            dest = os.path.normpath(os.path.join(os.path.dirname(src), path_part))
        rel_src = os.path.relpath(src, ROOT)
        if not os.path.exists(dest):
            problems.append(f"{rel_src}: missing file  ->  {target}")
            continue
        if anchor:
            if dest not in heading_cache:
                heading_cache[dest] = headings(dest)
            if slug(anchor) not in heading_cache[dest]:
                problems.append(f"{rel_src}: missing anchor -> {target}")

print(f"{len(md_files)} markdown files, {checked} relative links checked")
if problems:
    print(f"\n{len(problems)} problem(s):\n")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print("\nAll relative links and anchors resolve.")
