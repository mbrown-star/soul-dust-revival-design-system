#!/usr/bin/env python3
"""Stop hook: don't let Claude finish while cover-pipeline changes are undocumented.

Checked over two spans, so an older changelog entry on the branch can't cover a new edit:
  - uncommitted work (HEAD -> working tree, staged, unstaged and untracked), and
  - the whole branch (merge-base with origin/main -> working tree).
In each span:
  - a change to a cover script or calibration.json needs a change to CHANGELOG.md at the
    repo root (the design system's changelog);
  - a new titles/<key>.json needs a change to the README's "## Register of shipped covers".

If Claude has already been sent back once for this (stop_hook_active), it lets the stop
through with a warning rather than looping.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_common import LOGGED_FILES, PIPELINE_REL, block, project_dir, read_event  # noqa: E402

README_REL = PIPELINE_REL.replace(os.sep, "/") + "/README.md"
CHANGELOG_REL = "CHANGELOG.md"


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=20)
    return r.stdout if r.returncode == 0 else None


def base_commit(root):
    for ref in ("origin/HEAD", "origin/main", "main"):
        mb = git(root, "merge-base", "HEAD", ref)
        if mb:
            return mb.strip()
    head = git(root, "rev-parse", "HEAD")
    return head.strip() if head else None


def read_at(root, base, rel):
    return git(root, "show", f"{base}:{rel}") or ""


def read_now(root, rel):
    try:
        return open(os.path.join(root, rel), encoding="utf-8").read()
    except OSError:
        return ""


def section(text, heading):
    """Body of the '## <heading>...' section, or '' if there isn't one."""
    out, inside = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith(heading.lower())
            continue
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def pipeline_changes(root, base):
    pipe = PIPELINE_REL.replace(os.sep, "/")
    diff = (git(root, "diff", "--name-status", base, "--", pipe) or "").splitlines()
    untracked = (git(root, "ls-files", "--others", "--exclude-standard", "--", pipe) or "").splitlines()
    changed, added = set(), set()
    for line in diff:
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        changed.add(path)
        if status.startswith("A"):
            added.add(path)
    changed |= set(untracked)
    added |= set(untracked)
    rel = lambda p: p[len(pipe) + 1:] if p.startswith(pipe + "/") else p  # noqa: E731
    scripts = sorted(rel(p) for p in changed if rel(p) in LOGGED_FILES)
    titles = sorted(rel(p) for p in added if rel(p).startswith("titles/") and rel(p).endswith(".json")
                    and rel(p).count("/") == 1)
    return scripts, titles


def main():
    event = read_event()
    root = project_dir(event)
    if not os.path.isdir(os.path.join(root, PIPELINE_REL)):
        return 0
    base = base_commit(root)
    if not base:
        return 0
    head = (git(root, "rev-parse", "HEAD") or "").strip()
    problems = []
    for since, span in ((head, "uncommitted"), (base, "on this branch")):
        if not since:
            continue
        scripts, titles = pipeline_changes(root, since)
        if scripts and read_at(root, since, CHANGELOG_REL) == read_now(root, CHANGELOG_REL):
            problems.append(f"{', '.join(scripts)} changed ({span}) but {CHANGELOG_REL} didn't. Add a dated entry "
                            "saying what changed and why.")
        if titles and (section(read_at(root, since, README_REL), "Register")
                       == section(read_now(root, README_REL), "Register")):
            problems.append(f"New title {', '.join(titles)} ({span}) but the register of shipped covers in "
                            f"{README_REL} didn't change. Add its row (title, type, trim, pages, spine, ground).")
        if problems:
            break
    if not problems:
        return 0
    msg = "Cover pipeline docs check: " + " ".join(problems)
    if event.get("stop_hook_active"):
        print(json.dumps({"systemMessage": "Warning, still undocumented: " + msg}))
        return 0
    block(msg)


if __name__ == "__main__":
    sys.exit(main())
