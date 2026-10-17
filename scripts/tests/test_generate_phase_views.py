import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate_phase_views.py"


def make_project(root):
    (root / "docs").mkdir()
    (root / ".github" / "prompts").mkdir(parents=True)
    (root / "docs" / "INDEX.json").write_text((ROOT / "docs" / "INDEX.json").read_text())
    start = "<!-- BEGIN GENERATED PHASE LIST -->"
    end = "<!-- END GENERATED PHASE LIST -->"
    (root / "README.md").write_text(f"Before.\n{start}\nstale readme text\n{end}\nAfter.\n")
    (root / ".github" / "prompts" / "ai-sdlc.prompt.md").write_text(
        f"Before.\n{start}\nstale prompt text\n{end}\nAfter.\n"
    )


class GeneratePhaseViewsTests(unittest.TestCase):
    def run_generator(self, root, *args):
        return subprocess.run(
            [sys.executable, str(GENERATOR), "--root", str(root), *args],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_check_fails_when_generated_phase_views_are_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            result = self.run_generator(root, "--check")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("README.md", result.stdout + result.stderr)
        self.assertIn("ai-sdlc.prompt.md", result.stdout + result.stderr)

    def test_generation_uses_index_and_preserves_content_outside_regions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            readme = (root / "README.md").read_text()
            prompt = (root / ".github" / "prompts" / "ai-sdlc.prompt.md").read_text()
            phases = json.loads((root / "docs" / "INDEX.json").read_text())["phases"]
            names = [phase["name"] for phase in phases]
            self.assertIn("Before.\n", readme)
            self.assertIn("\nAfter.\n", readme)
            self.assertIn(f"{names[0]} (once, to define the project)", readme)
            self.assertIn(" → ".join(names[1:]), readme)
            self.assertIn(" | ".join(name.lower() for name in names), prompt)
            self.assertNotIn("stale", readme + prompt)

            checked = self.run_generator(root, "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_missing_or_reversed_markers_fail_without_overwriting_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            target = root / "README.md"
            original = target.read_text().replace(
                "<!-- BEGIN GENERATED PHASE LIST -->", "<!-- END GENERATED PHASE LIST -->", 1
            )
            target.write_text(original)
            result = self.run_generator(root)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(target.read_text(), original)

    def test_changed_index_phase_name_is_used_in_generated_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            index_path = root / "docs" / "INDEX.json"
            index = json.loads(index_path.read_text())
            index["phases"][1]["name"] = "DISCOVER"
            index_path.write_text(json.dumps(index))

            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            readme = (root / "README.md").read_text()
            prompt = (root / ".github" / "prompts" / "ai-sdlc.prompt.md").read_text()

        self.assertIn("DISCOVER", readme)
        self.assertIn("discover", prompt)
        self.assertNotIn("specify", prompt)


if __name__ == "__main__":
    unittest.main()
