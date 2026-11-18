#!/usr/bin/env python3
"""PostToolUse (Edit|Write|MultiEdit) hook: after an edit to calibration.json, it must parse and
contain every key the cover scripts read.

The required keys are derived from the scripts' own source on every run (no hand-kept
list): each script is parsed with `ast`, every name bound to calibration.json or to a part
of it is followed (CAL, kl/bp/fp/sp, _KL.., fx = dict(CAL[...]), b6, and accessor lambdas
such as `f = lambda k: fp[k] * H` called as f("..."), and every constant-key read
through those names is required. Reads with .get(key, default) are optional and skipped.

Run directly to list the derived keys:  python3 calibration_keys.py --list [pipeline_dir]
"""
import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_common import block, pipeline_dir, pipeline_relpath, project_dir, read_event  # noqa: E402

SCRIPTS = ("gen_covers.py", "render.py", "verify_covers.py", "to_pdf.py", "guards.py")


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def required_keys_in(source):
    tree = ast.parse(source)
    aliases, accessors = {}, {}

    def resolve(node):
        if isinstance(node, ast.Name):
            return aliases.get(node.id)
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr == "load" and "calibration.json" in ast.unparse(node):
                return ()
            if isinstance(fn, ast.Name) and fn.id == "dict" and len(node.args) == 1:
                return resolve(node.args[0])
            return None
        if isinstance(node, ast.Subscript):
            base, key = resolve(node.value), _const_str(node.slice)
            return base + (key,) if base is not None and key is not None else None
        return None

    def bind(target, value):
        changed = False
        if isinstance(target, ast.Name):
            if isinstance(value, ast.Lambda) and len(value.args.args) == 1:
                p = value.args.args[0].arg
                for sub in ast.walk(value.body):
                    if isinstance(sub, ast.Subscript) and isinstance(sub.slice, ast.Name) and sub.slice.id == p:
                        base = resolve(sub.value)
                        if base is not None and accessors.get(target.id) != base:
                            accessors[target.id] = base
                            changed = True
                return changed
            path = resolve(value)
            if path is not None and aliases.get(target.id) != path:
                aliases[target.id] = path
                changed = True
        elif isinstance(target, ast.Tuple) and isinstance(value, ast.Tuple) and len(target.elts) == len(value.elts):
            for t, v in zip(target.elts, value.elts):
                changed |= bind(t, v)
        return changed

    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    for _ in range(10):  # propagate aliases of aliases until stable
        changed = False
        for a in assigns:
            for t in a.targets:
                changed |= bind(t, a.value)
        if not changed:
            break

    required = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):
            path = resolve(node)
            if path:
                required.add(path)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in accessors and node.args:
            key = _const_str(node.args[0])
            if key is not None:
                required.add(accessors[node.func.id] + (key,))
    return required


def required_keys(pipe):
    req = set()
    for name in SCRIPTS:
        p = os.path.join(pipe, name)
        if os.path.exists(p):
            req |= required_keys_in(open(p, encoding="utf-8").read())
    return sorted(req)


def missing_keys(cal, required):
    missing = []
    for path in required:
        node = cal
        for i, k in enumerate(path):
            if not isinstance(node, dict) or k not in node:
                missing.append(".".join(path[:i + 1]))
                break
            node = node[k]
    return sorted(set(missing))


def check(pipe):
    """Problems with calibration.json as a list of strings (empty when it's fine)."""
    path = os.path.join(pipe, "calibration.json")
    try:
        cal = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"calibration.json does not parse: {e}"]
    if not isinstance(cal, dict):
        return ["calibration.json must be a JSON object"]
    req = required_keys(pipe)
    if not req:
        return ["could not derive any calibration keys from the scripts; check calibration_keys.py"]
    return [f"missing key: {k}" for k in missing_keys(cal, req)]


def main(argv):
    if argv[:1] == ["--list"]:
        pipe = argv[1] if len(argv) > 1 else pipeline_dir(project_dir({}))
        print("\n".join(".".join(p) for p in required_keys(pipe)))
        return 0
    event = read_event()
    pipe = pipeline_dir(project_dir(event))
    if pipeline_relpath(event, pipe) != "calibration.json":
        return 0
    problems = check(pipe)
    if problems:
        block("calibration.json check FAILED (keys are derived from what the cover scripts read):\n  - "
              + "\n  - ".join(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
