"""Unit tests for the cover-pipeline hooks, driven the way Claude Code drives them: JSON on
stdin, exit code and stderr out. Standard library only.

    python3 -m unittest discover -s .claude/hooks -v

The cover_verify tests run the real pipeline (gen -> render -> verify) on a scratch copy and
are skipped when no interpreter with playwright/pillow/numpy/reportlab is found.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HOOKS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HOOKS))
PIPE_SRC = os.path.join(REPO, "assets", "applied-covers")
HERO_SRC = os.path.join(REPO, "assets", "hero-source.png")
sys.path.insert(0, HOOKS)
from cover_common import pipeline_python  # noqa: E402


def run_hook(script, event, project, extra_env=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project, **(extra_env or {}))
    r = subprocess.run([sys.executable, os.path.join(HOOKS, script)], input=json.dumps(event),
                       capture_output=True, text=True, env=env, timeout=900)
    return r.returncode, r.stdout, r.stderr


def edit_event(path, cwd, tool="Edit"):
    return {"session_id": "test", "hook_event_name": "PostToolUse", "tool_name": tool, "cwd": cwd,
            "tool_input": {"file_path": path, "old_string": "a", "new_string": "b"},
            "tool_response": {"success": True}}


def copy_project(tmp):
    """A scratch project with the pipeline at assets/applied-covers (not a git repo)."""
    pipe = os.path.join(tmp, "assets", "applied-covers")
    shutil.copytree(PIPE_SRC, pipe, ignore=shutil.ignore_patterns("build", ".venv", "__pycache__"))
    if os.path.exists(HERO_SRC):
        shutil.copy(HERO_SRC, os.path.join(tmp, "assets", "hero-source.png"))
    return pipe


def edit_json(path, fn):
    d = json.load(open(path, encoding="utf-8"))
    fn(d)
    json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


class CalibrationKeysHook(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pipe = copy_project(self.tmp)
        self.cal = os.path.join(self.pipe, "calibration.json")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def hook(self, path=None):
        return run_hook("calibration_keys.py", edit_event(path or self.cal, self.tmp), self.tmp)

    def test_ignores_other_files(self):
        self.assertEqual(self.hook(os.path.join(self.tmp, "README.md"))[0], 0)

    def test_current_calibration_passes(self):
        code, _, err = self.hook()
        self.assertEqual(code, 0, err)

    def test_relative_path_from_cwd(self):
        edit_json(self.cal, lambda d: d["keyline"].pop("line_weight_frac_of_dpi"))
        code, _, err = run_hook("calibration_keys.py", edit_event("assets/applied-covers/calibration.json", self.tmp),
                                self.tmp)
        self.assertEqual(code, 2)
        self.assertIn("keyline.line_weight_frac_of_dpi", err)

    def test_missing_leaf_key_blocks(self):
        edit_json(self.cal, lambda d: d["fixed_px_at_300dpi"].pop("back_hook"))
        code, _, err = self.hook()
        self.assertEqual(code, 2)
        self.assertIn("missing key: fixed_px_at_300dpi.back_hook", err)

    def test_missing_lambda_accessor_key_blocks(self):
        # read only as f("tagline_font_frac_of_panel_height") through `f = lambda k: fp[k] * H`
        edit_json(self.cal, lambda d: d["front_panel"].pop("tagline_font_frac_of_panel_height"))
        code, _, err = self.hook()
        self.assertEqual(code, 2)
        self.assertIn("front_panel.tagline_font_frac_of_panel_height", err)

    def test_missing_section_blocks(self):
        edit_json(self.cal, lambda d: d.pop("back_panel_6x9"))
        code, _, err = self.hook()
        self.assertEqual(code, 2)
        self.assertIn("missing key: back_panel_6x9", err)

    def test_optional_get_keys_not_required(self):
        # spine.font_family and spine.font_weights are read with .get(key, default)
        edit_json(self.cal, lambda d: (d["spine"].pop("font_family"), d["spine"].pop("font_weights")))
        self.assertEqual(self.hook()[0], 0)

    def test_bad_json_blocks(self):
        open(self.cal, "a").write("\n,}")
        code, _, err = self.hook()
        self.assertEqual(code, 2)
        self.assertIn("does not parse", err)

    def test_empty_stdin_is_harmless(self):
        r = subprocess.run([sys.executable, os.path.join(HOOKS, "calibration_keys.py")], input="",
                           capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=self.tmp))
        self.assertEqual(r.returncode, 0)


def _have_pipeline_deps():
    py = pipeline_python(PIPE_SRC)
    return subprocess.run([py, "-c", "import playwright, PIL, numpy, reportlab"], capture_output=True).returncode == 0


@unittest.skipUnless(_have_pipeline_deps(), "no interpreter with the cover pipeline's dependencies")
class CoverVerifyHook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.pipe = copy_project(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def hook(self, rel):
        return run_hook("cover_verify.py", edit_event(os.path.join(self.pipe, rel), self.tmp), self.tmp)

    def test_ignores_untracked_names(self):
        code, out, _ = self.hook("README.md")
        self.assertEqual((code, out), (0, ""))
        code, out, _ = self.hook("verify_covers.py")
        self.assertEqual((code, out), (0, ""))

    def test_clean_title_edit_passes_and_leaves_build_alone(self):
        code, out, err = self.hook("titles/james.json")
        self.assertEqual(code, 0, err)
        self.assertIn("1-peter, ten-commandments, james", out)
        self.assertFalse(os.path.exists(os.path.join(self.pipe, "build")), "hook must not write build/")

    def test_duplicate_ground_blocks(self):
        p = os.path.join(self.pipe, "titles", "james.json")
        orig = open(p, encoding="utf-8").read()
        try:
            edit_json(p, lambda d: d.update(ground="#2C211E"))  # Cinder: The Ten Commandments
            code, _, err = self.hook("titles/james.json")
            self.assertEqual(code, 2)
            self.assertIn("gen_covers.py exited 1", err)
            self.assertIn("already used in the README register", err)
        finally:
            open(p, "w", encoding="utf-8").write(orig)

    def test_broken_layout_fails_verify_and_blocks(self):
        p = os.path.join(self.pipe, "gen_covers.py")
        orig = open(p, encoding="utf-8").read()
        try:
            # A layout number typed straight into the script: keyline inset doubled.
            bad = orig.replace('kl_tb = round(kl["top_bottom_inset_frac_of_panel_height"] * H)',
                               'kl_tb = 2 * round(kl["top_bottom_inset_frac_of_panel_height"] * H)')
            self.assertNotEqual(bad, orig)
            open(p, "w", encoding="utf-8").write(bad)
            code, _, err = self.hook("gen_covers.py")
            self.assertEqual(code, 2)
            self.assertIn("verify_covers.py exited 1", err)
            self.assertIn("keyline top inset", err)
        finally:
            open(p, "w", encoding="utf-8").write(orig)


class ChangelogStopHook(unittest.TestCase):
    README = ("# Applied covers\n\n## Building a cover\n\nsteps\n\n## Register of shipped covers\n\n"
              "| Title | Type | Trim | Pages | Spine | Ground |\n|---|---|---|---|---|---|\n"
              "| 1 Peter | Book Study | 6x9 | 189 | 0.4725in | Soot `#2a2a26` |\n\n"
              "## Changelog\n\n- **2026-11-17:** restored.\n")
    CHANGELOG = "# Changelog\n\n## 2026-11-17: Cover pipeline restored\n"

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pipe = os.path.join(self.tmp, "assets", "applied-covers")
        os.makedirs(os.path.join(self.pipe, "titles"))
        self.write("README.md", self.README)
        self.write("gen_covers.py", "print('gen')\n")
        self.write("calibration.json", "{}\n")
        self.write("titles/1-peter.json", "{}\n")
        self.write("../../CHANGELOG.md", self.CHANGELOG)
        self.git("init", "-q", "-b", "main")
        self.git("-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "x")
        self.git("add", "-A")
        self.git("-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "base")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def git(self, *a):
        subprocess.run(["git", "-C", self.tmp, *a], check=True, capture_output=True)

    def write(self, rel, text, mode="w"):
        with open(os.path.join(self.pipe, rel), mode, encoding="utf-8") as f:
            f.write(text)

    def stop(self, active=False):
        ev = {"session_id": "test", "hook_event_name": "Stop", "cwd": self.tmp, "stop_hook_active": active}
        return run_hook("cover_changelog_stop.py", ev, self.tmp)

    def test_no_changes_allows_stop(self):
        self.assertEqual(self.stop()[0], 0)

    def test_script_change_without_changelog_blocks(self):
        self.write("gen_covers.py", "print('changed')\n")
        code, _, err = self.stop()
        self.assertEqual(code, 2)
        self.assertIn("gen_covers.py changed but CHANGELOG.md didn't", err)

    def test_calibration_change_with_changelog_allows(self):
        self.write("calibration.json", '{"a": 1}\n')
        self.write("../../CHANGELOG.md", "\n## 2026-11-18: changed calibration\n", mode="a")
        code, _, err = self.stop()
        self.assertEqual(code, 0, err)

    def test_readme_change_does_not_stand_in_for_changelog(self):
        self.write("gen_covers.py", "print('changed')\n")
        self.write("README.md", "- **2026-11-18:** changed gen.\n", mode="a")
        self.assertEqual(self.stop()[0], 2)

    def test_both_needed_when_script_changed_and_title_added(self):
        self.write("gen_covers.py", "print('changed')\n")
        self.write("titles/james.json", "{}\n")
        self.write("../../CHANGELOG.md", "\n## 2026-11-18: x\n", mode="a")
        code, _, err = self.stop()
        self.assertEqual(code, 2)
        self.assertIn("register", err)
        self.assertNotIn("CHANGELOG.md didn't", err)

    def test_committed_change_is_still_caught(self):
        self.write("gen_covers.py", "print('changed')\n")
        self.git("-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qam", "change")
        self.assertEqual(self.stop()[0], 2)

    def test_new_title_without_register_row_blocks(self):
        self.write("titles/james.json", "{}\n")
        code, _, err = self.stop()
        self.assertEqual(code, 2)
        self.assertIn("New title titles/james.json", err)
        self.assertNotIn("CHANGELOG", err)

    def test_new_title_with_register_row_allows(self):
        self.write("titles/james.json", "{}\n")
        self.write("README.md", self.README.replace(
            "Soot `#2a2a26` |\n", "Soot `#2a2a26` |\n| James | Book Study | 6x9 | 202 | 0.505in | Coal `#1b1b1b` |\n"))
        self.assertEqual(self.stop()[0], 0)

    def test_edit_to_existing_title_needs_nothing(self):
        self.write("titles/1-peter.json", '{"pages": 190}\n')
        self.assertEqual(self.stop()[0], 0)

    def test_second_stop_warns_instead_of_looping(self):
        self.write("gen_covers.py", "print('changed')\n")
        code, out, _ = self.stop(active=True)
        self.assertEqual(code, 0)
        self.assertIn("still undocumented", json.loads(out)["systemMessage"])

    def test_project_without_pipeline_is_ignored(self):
        shutil.rmtree(os.path.join(self.tmp, "assets"))
        self.assertEqual(self.stop()[0], 0)


if __name__ == "__main__":
    unittest.main()
