#!/usr/bin/env python3
"""PostToolUse (Edit|Write|MultiEdit) hook: after an edit to gen_covers.py, render.py, guards.py,
calibration.json or titles/*.json, rebuild and verify covers, and block on failure.

Rebuilds the canary titles (1 Peter, 6x9; The Ten Commandments, 8.5x11) together, and an
edited title in a run of its own: gen_covers.py -> render.py -> verify_covers.py. The edited
title runs alone because verify_covers.py's cross-title spine check compares rendered ink,
which varies with the letters in a title (James's spine title fails it beside 1 Peter even
though its CSS size is right). Each run builds into a temporary folder ($SDR_COVER_BUILD),
so the hook never touches build/ or its verification stamps.
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_common import (CANARY_KEYS, VERIFY_TRIGGERS, block, pipeline_dir, pipeline_python,  # noqa: E402
                          pipeline_relpath, project_dir, read_event)

STEP_TIMEOUT = 240


def runs_for(rel, pipe):
    """Groups of title keys, each verified in its own build: the canaries, then the edited title."""
    exists = lambda k: os.path.exists(os.path.join(pipe, "titles", k + ".json"))  # noqa: E731
    runs = [[k for k in CANARY_KEYS if exists(k)]]
    if rel.startswith("titles/") and rel.endswith(".json"):
        key = rel[len("titles/"):-len(".json")]
        if exists(key) and key not in CANARY_KEYS:
            runs.append([key])
    return [r for r in runs if r]


def run_pipeline(py, pipe, keys, rel):
    with tempfile.TemporaryDirectory(prefix="sdr-cover-hook-") as tmp:
        env = dict(os.environ, SDR_COVER_BUILD=tmp)
        for step in (["gen_covers.py", *keys], ["render.py", *keys], ["verify_covers.py"]):
            try:
                r = subprocess.run([py, *step], cwd=pipe, env=env, capture_output=True,
                                   text=True, timeout=STEP_TIMEOUT)
            except subprocess.TimeoutExpired:
                block(f"Cover check: {step[0]} timed out after {STEP_TIMEOUT}s while checking your edit to {rel}.")
            if r.returncode != 0:
                tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-25:])
                block(f"Cover check FAILED after your edit to {rel}: {step[0]} exited {r.returncode} "
                      f"(titles: {', '.join(keys)}; interpreter: {py}).\n{tail}\n"
                      "Fix the cause in the pipeline (gen_covers.py or calibration.json first), don't work around it.")


def is_trigger(rel):
    return rel in VERIFY_TRIGGERS or (rel.startswith("titles/") and rel.endswith(".json") and rel.count("/") == 1)


def main():
    event = read_event()
    pipe = pipeline_dir(project_dir(event))
    rel = pipeline_relpath(event, pipe)
    if not rel or not is_trigger(rel):
        return 0
    py = pipeline_python(pipe)
    runs = runs_for(rel, pipe)
    for keys in runs:
        run_pipeline(py, pipe, keys, rel)
    keys = [k for r in runs for k in r]
    print(f"Cover check passed for {', '.join(keys)} after editing {rel}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
