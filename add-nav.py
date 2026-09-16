#!/usr/bin/env python3
"""
Add the 'Go straight to' strip and the back-to-top footer to every content page.

Run from the repo root:      python add-nav.py
Preview without writing:     python add-nav.py --dry-run

Skips any file that already contains 'Go straight to', so it is safe to re-run.
"""

import re
import sys
from pathlib import Path

DRY = "--dry-run" in sys.argv

ROOT = Path(".").resolve()

# Files that are repo process, not submission content.
SKIP_NAMES = {"CONTRIBUTING.md", "ONBOARDING.md", "PULL_REQUEST_TEMPLATE.md"}
SKIP_DIRS = {".github", ".git"}

TARGETS = {
    "docs/adrs": dict(
        home="../../README.md", adrs="README.md", diagrams="../diagrams/README.md",
        impl="../implementation.md", reqs="../requirements.md",
        chars="../architecture-characteristics.md", brief="../kata-brief.pdf",
    ),
    "docs/diagrams": dict(
        home="../../README.md", adrs="../adrs/README.md", diagrams="README.md",
        impl="../implementation.md", reqs="../requirements.md",
        chars="../architecture-characteristics.md", brief="../kata-brief.pdf",
    ),
    "docs": dict(
        home="../README.md", adrs="adrs/README.md", diagrams="diagrams/README.md",
        impl="implementation.md", reqs="requirements.md",
        chars="architecture-characteristics.md", brief="kata-brief.pdf",
    ),
}


def slug(heading: str) -> str:
    """GitHub's heading-anchor rule: lowercase, drop punctuation, spaces to hyphens."""
    s = heading.strip().lstrip("#").strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)      # drop . , : ( ) ' etc, keep word chars
    s = re.sub(r"\s+", "-", s)
    return s


def strip_line(p: dict) -> str:
    return (
        f"**Go straight to:** [Home]({p['home']}) · [ADRs]({p['adrs']}) · "
        f"[Diagrams]({p['diagrams']}) · [Implementation]({p['impl']}) · "
        f"[Requirements]({p['reqs']}) · [Characteristics]({p['chars']}) · "
        f"[Brief]({p['brief']})"
    )


def footer(p: dict, anchor: str) -> str:
    return (
        "\n---\n\n"
        '<p align="center">❦</p>\n\n'
        f'<p align="right"><a href="#{anchor}">↑ Back to top</a> · '
        f'<a href="{p["home"]}">Home</a> · '
        f'<a href="{p["adrs"]}">All ADRs</a> · '
        f'<a href="{p["diagrams"]}">All diagrams</a></p>\n'
    )


changed, skipped, problems = [], [], []

for path in sorted(ROOT.rglob("*.md")):
    rel = path.relative_to(ROOT)
    parts = rel.parts

    if any(d in SKIP_DIRS for d in parts) or path.name in SKIP_NAMES:
        continue

    parent = "/".join(parts[:-1])
    if parent not in TARGETS:
        continue            # root README.md handled by hand; it is home

    paths = TARGETS[parent]
    text = path.read_text(encoding="utf-8")

    if "Go straight to" in text:
        skipped.append(str(rel))
        continue

    lines = text.split("\n")
    h1_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if h1_idx is None:
        problems.append(f"{rel}: no H1 found, skipped")
        continue

    anchor = slug(lines[h1_idx])

    # Insert the strip directly after the H1, with a blank line either side.
    new = lines[: h1_idx + 1] + ["", strip_line(paths)] + lines[h1_idx + 1 :]
    out = "\n".join(new).rstrip("\n") + "\n" + footer(paths, anchor)

    if DRY:
        print(f"{rel}\n    anchor -> #{anchor}")
    else:
        path.write_text(out, encoding="utf-8")
    changed.append(str(rel))

print()
print(f"{len(changed)} file(s) {'would be ' if DRY else ''}updated")
print(f"{len(skipped)} already had the strip: {', '.join(skipped) or 'none'}")
for p in problems:
    print(f"  ! {p}")
if DRY:
    print("\nDry run. Nothing written. Re-run without --dry-run to apply.")
