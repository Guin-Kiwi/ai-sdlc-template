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
    change_types_start = "<!-- BEGIN GENERATED CHANGE TYPES -->"
    change_types_end = "<!-- END GENERATED CHANGE TYPES -->"
    (root / "CONTRIBUTING.md").write_text(
        f"Before.\n{change_types_start}\nstale table\n{change_types_end}\nAfter.\n"
    )
    readme_paths = (
        "<!-- BEGIN GENERATED PROJECT PATHS -->stale project<!-- END GENERATED PROJECT PATHS -->"
        " | "
        "<!-- BEGIN GENERATED PROCESS PATHS -->stale process<!-- END GENERATED PROCESS PATHS -->"
    )
    current = (root / "README.md").read_text()
    updated = current.replace("Before.\n", f"Before.\n{readme_paths}\n")
    (root / "README.md").write_text(updated)
    docker_begin = "# BEGIN GENERATED PROCESS PATHS"
    docker_end = "# END GENERATED PROCESS PATHS"
    (root / ".dockerignore").write_text(
        f"keep-me\n{docker_begin}\nold process paths\n{docker_end}\nalso-keep-me\n"
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

    def test_check_skips_view_without_generated_region(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            initial_result = self.run_generator(root)
            self.assertEqual(initial_result.returncode, 0, initial_result.stdout + initial_result.stderr)
            readme = root / "README.md"
            readme.write_text("Repository-specific README without generated markers.\n")

            check_result = self.run_generator(root, "--check")
            write_result = self.run_generator(root)
            generated_readme = readme.read_text()

        self.assertEqual(check_result.returncode, 0, check_result.stdout + check_result.stderr)
        self.assertEqual(write_result.returncode, 0, write_result.stdout + write_result.stderr)
        self.assertEqual(generated_readme, "Repository-specific README without generated markers.\n")

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

    def test_check_fails_when_contributing_change_type_table_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            index_path = root / "docs" / "INDEX.json"
            index = json.loads(index_path.read_text())
            index["change_types"] = {"fix": {
                "prefixes": ["fix"],
                "meaning": "custom correction",
                "test": "a test description",
                "workflow": "a workflow description",
                "needs_spec": False,
            }, "breaking": {
                "prefixes": ["!"],
                "meaning": "breaking decision",
                "test": "supersedes test",
                "workflow": "record, ripple, code",
                "needs_spec": True,
            }}
            index_path.write_text(json.dumps(index))
            generated = self.run_generator(root)
            self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
            contributing = root / "CONTRIBUTING.md"
            contributing.write_text(contributing.read_text().replace("custom correction", "stale correction", 1))
            result = self.run_generator(root, "--check")

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CONTRIBUTING.md", result.stdout + result.stderr)

    def test_generation_renders_change_types_from_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            index_path = root / "docs" / "INDEX.json"
            index = json.loads(index_path.read_text())
            index["change_types"] = {"fix": {
                "prefixes": ["fix"],
                "meaning": "custom correction",
                "test": "a test description",
                "workflow": "a workflow description",
                "needs_spec": False,
            }, "tooling": {
                "prefixes": ["test", "ci", "chore"],
                "meaning": "tooling work",
                "test": "app unchanged",
                "workflow": "run checks",
                "needs_spec": False,
            }, "BREAKING": {
                "prefixes": ["!"],
                "meaning": "breaking decision",
                "test": "supersedes test",
                "workflow": "record, ripple, code",
                "needs_spec": True,
            }, "review": {
                "prefixes": ["review"],
                "meaning": "human review",
                "test": "no file changes",
                "workflow": "record with scripts/sdlc.py review",
                "needs_spec": False,
            }}
            index_path.write_text(json.dumps(index))

            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            contributing = root / "CONTRIBUTING.md"
            generated = contributing.read_text()

        self.assertIn("custom correction", generated)
        self.assertIn("a test description", generated)
        self.assertIn("a workflow description", generated)
        self.assertIn("`test:`, `ci:`, `chore:`", generated)
        self.assertIn("`!` after any prefix", generated)
        self.assertIn("human review", generated)
        self.assertNotIn("stale table", generated)

    def test_generated_table_contains_every_declared_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            index = json.loads((root / "docs" / "INDEX.json").read_text())
            generated = (root / "CONTRIBUTING.md").read_text()

        for details in index["change_types"].values():
            for prefix in details["prefixes"]:
                if prefix == "!":
                    self.assertIn("`!` after any prefix", generated)
                else:
                    self.assertIn(f"`{prefix}:`", generated)

    def test_check_fails_when_readme_path_region_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            self.run_generator(root)
            readme = root / "README.md"
            content = readme.read_text().replace("`docs/TASKS.md`", "stale TASKS path")
            readme.write_text(content)
            result = self.run_generator(root, "--check")

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("README.md", result.stdout + result.stderr)

    def test_check_fails_when_dockerignore_path_region_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            self.run_generator(root)
            dockerignore = root / ".dockerignore"
            dockerignore.write_text(dockerignore.read_text().replace("docs", "stale-docs", 1))
            result = self.run_generator(root, "--check")

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(".dockerignore", result.stdout + result.stderr)

    def test_generation_renders_index_project_and_process_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            readme = (root / "README.md").read_text()
            dockerignore = (root / ".dockerignore").read_text()
            index = json.loads((root / "docs" / "INDEX.json").read_text())

        for path in index["project"]:
            self.assertIn(f"`{path}`", readme)
        for path in index["process"]:
            self.assertIn(path, dockerignore)
            if path in index["template_only"]:
                self.assertNotIn(path, readme)
            else:
                self.assertIn(path, readme)
        self.assertIn("keep-me", dockerignore)
        self.assertIn("also-keep-me", dockerignore)

    def test_check_fails_when_dockerignore_or_readme_path_regions_are_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            self.run_generator(root)
            readme = root / "README.md"
            dockerignore = root / ".dockerignore"
            readme.write_text(readme.read_text().replace("`src/`", "stale-src", 1))
            dockerignore.write_text(dockerignore.read_text().replace(".dockerignore", "stale", 1))
            result = self.run_generator(root, "--check")

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("README.md", result.stdout + result.stderr)
        self.assertIn(".dockerignore", result.stdout + result.stderr)

    def test_readme_table_rows_stay_on_one_line_after_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            make_project(root)
            (root / "README.md").write_text((ROOT / "README.md").read_text())
            result = self.run_generator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            readme = (root / "README.md").read_text()

        rows = [line for line in readme.splitlines() if line.startswith("|")]
        self.assertTrue(rows, "README has no table rows")
        for row in rows:
            self.assertTrue(row.endswith("|"), f"table row is split across lines: {row!r}")
        self.assertIn("`src/`", readme)
        self.assertIn("`AGENTS.md`", readme)


if __name__ == "__main__":
    unittest.main()
