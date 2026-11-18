"""Shared helpers for the cover-pipeline Claude Code hooks (standard library only).

The hooks are a second layer. The hard guards live in the cover scripts themselves
(assets/applied-covers/guards.py), so they still apply in Cowork, where hooks don't fire.
"""
import json
import os
import subprocess
import sys

PIPELINE_REL = os.path.join("assets", "applied-covers")
# Files whose edits must keep the pipeline passing verify_covers.py (hook: cover_verify.py).
VERIFY_TRIGGERS = {"gen_covers.py", "render.py", "calibration.json", "guards.py"}
# Files whose changes must be logged in the README's Changelog (hook: cover_changelog_stop.py).
LOGGED_FILES = {"gen_covers.py", "render.py", "verify_covers.py", "to_pdf.py", "guards.py", "calibration.json"}
# Titles rebuilt on every script/calibration edit: one per trim (6x9 and 8.5x11).
CANARY_KEYS = ["1-peter", "ten-commandments"]


def read_event():
    raw = sys.stdin.read()
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def project_dir(event):
    d = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    try:
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        if top.returncode == 0 and top.stdout.strip():
            return top.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return d


def pipeline_dir(root):
    return os.path.join(root, PIPELINE_REL)


def pipeline_relpath(event, pipe):
    """The edited file's path relative to the pipeline folder, or None if it's outside it."""
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return None
    if not os.path.isabs(path):
        path = os.path.join(event.get("cwd") or os.getcwd(), path)
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(pipe))
    return None if rel.startswith("..") else rel.replace(os.sep, "/")


def pipeline_python(pipe):
    """Interpreter with playwright, pillow, numpy and reportlab: $SDR_COVER_PYTHON, then a
    .venv beside the scripts, then ~/.venvs/sdr-covers, then this interpreter."""
    for cand in (os.environ.get("SDR_COVER_PYTHON"),
                 os.path.join(pipe, ".venv", "bin", "python"),
                 os.path.expanduser("~/.venvs/sdr-covers/bin/python")):
        if cand and os.path.exists(cand):
            return cand
    return sys.executable


def block(msg):
    """Exit 2: Claude Code shows stderr to Claude (PostToolUse) or refuses to stop (Stop)."""
    sys.stderr.write(msg.rstrip() + "\n")
    sys.exit(2)
