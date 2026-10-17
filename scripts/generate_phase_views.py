#!/usr/bin/env python3
"""Generate checked phase-list views from docs/INDEX.json."""

import argparse
import json
import pathlib
import sys

BEGIN = "<!-- BEGIN GENERATED PHASE LIST -->"
END = "<!-- END GENERATED PHASE LIST -->"
VIEWS = (
    pathlib.Path("README.md"),
    pathlib.Path(".github/prompts/ai-sdlc.prompt.md"),
)


def read_phases(root):
    try:
        index = json.loads((root / "docs/INDEX.json").read_text())
        phases = index["phases"]
        if not phases or any(not isinstance(phase.get("name"), str) for phase in phases):
            raise ValueError("phases must contain named entries")
        return phases
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ValueError(f"cannot read phases from docs/INDEX.json: {error}") from error


def generated_text(path, phases):
    names = [phase["name"] for phase in phases]
    if path == pathlib.Path("README.md"):
        bootstrap = next((phase["name"] for phase in phases if phase.get("phase") == 0), None)
        sequence = [name for name in names if name != bootstrap]
        if bootstrap is None or not sequence:
            raise ValueError("README phase view requires phase 0 and at least one later phase")
        return (
            f"{bootstrap} (once, to define the project), then "
            f"{' → '.join(sequence)} for each feature."
        )
    if path == pathlib.Path(".github/prompts/ai-sdlc.prompt.md"):
        choices = " | ".join(name.lower() for name in names)
        return f"Phase: ${{input:phase:{choices}}}"
    raise ValueError(f"unsupported generated view: {path}")


def replace_region(content, replacement, path):
    begin_count = content.count(BEGIN)
    end_count = content.count(END)
    if begin_count == 0 and end_count == 0:
        return None
    if begin_count != 1 or end_count != 1:
        raise ValueError(f"{path}: expected exactly one generated-region marker pair")
    start = content.index(BEGIN) + len(BEGIN)
    finish = content.index(END)
    if content.index(BEGIN) > content.index(END):
        raise ValueError(f"{path}: generated-region markers are out of order")
    return content[:start] + "\n" + replacement + "\n" + content[finish:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated views are stale")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        phases = read_phases(root)
        expected_regions = {
            path: generated_text(path, phases)
            for path in VIEWS
        }
        originals = {path: (root / path).read_text() for path in VIEWS}
        replacements = {
            path: replace_region(originals[path], expected_regions[path], path)
            for path in VIEWS
        }
        stale = []
        for relative_path in VIEWS:
            if replacements[relative_path] is None:
                continue
            if originals[relative_path] != replacements[relative_path]:
                stale.append(relative_path.as_posix())
                if not args.check:
                    (root / relative_path).write_text(replacements[relative_path])
        if args.check and stale:
            print("Generated phase views are stale: " + ", ".join(stale), file=sys.stderr)
            return 1
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
