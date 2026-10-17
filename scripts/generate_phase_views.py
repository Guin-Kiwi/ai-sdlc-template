#!/usr/bin/env python3
"""Generate checked phase-list and change-type views from docs/INDEX.json."""

import argparse
import json
import pathlib
import sys

BEGIN = "<!-- BEGIN GENERATED PHASE LIST -->"
END = "<!-- END GENERATED PHASE LIST -->"
CHANGE_TYPES_BEGIN = "<!-- BEGIN GENERATED CHANGE TYPES -->"
CHANGE_TYPES_END = "<!-- END GENERATED CHANGE TYPES -->"
README_PROJECT_BEGIN = "<!-- BEGIN GENERATED PROJECT PATHS -->"
README_PROJECT_END = "<!-- END GENERATED PROJECT PATHS -->"
README_PROCESS_BEGIN = "<!-- BEGIN GENERATED PROCESS PATHS -->"
README_PROCESS_END = "<!-- END GENERATED PROCESS PATHS -->"
DOCKER_PROCESS_BEGIN = "# BEGIN GENERATED PROCESS PATHS"
DOCKER_PROCESS_END = "# END GENERATED PROCESS PATHS"
PATH_REGISTRY = {
    (pathlib.Path("README.md"), README_PROJECT_BEGIN, README_PROJECT_END): ("project", "inline", True),
    (pathlib.Path("README.md"), README_PROCESS_BEGIN, README_PROCESS_END): ("process", "inline", True),
    (pathlib.Path(".dockerignore"), DOCKER_PROCESS_BEGIN, DOCKER_PROCESS_END): ("process", "docker", False),
}


def read_index(root):
    try:
        index = json.loads((root / "docs/INDEX.json").read_text())
        phases = index["phases"]
        change_types = index["change_types"]
        if not phases or any(not isinstance(phase.get("name"), str) for phase in phases):
            raise ValueError("phases must contain named entries")
        if not change_types or any(
            not all(isinstance(details.get(key), str) for key in ("meaning", "test", "workflow"))
            or not isinstance(details.get("prefixes"), list)
            or not details["prefixes"]
            or any(not isinstance(prefix, str) or not prefix for prefix in details["prefixes"])
            or not isinstance(details.get("needs_spec"), bool)
            for details in change_types.values()
        ):
            raise ValueError("change_types must contain meaning, test, workflow and needs_spec for each prefix")
        return index
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ValueError(f"cannot read phase and change-type metadata from docs/INDEX.json: {error}") from error


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


def generated_change_types(change_types):
    lines = ["| Prefix | Meaning | Test | Workflow |", "|---|---|---|---|"]
    for prefix, details in change_types.items():
        if "!" in details["prefixes"]:
            label = "`!` after any prefix"
        else:
            label = ", ".join(f"`{item}:`" for item in details["prefixes"])
        lines.append(
            f"| {label} | {details['meaning']} | {details['test']} | {details['workflow']} |"
        )
    return "\n".join(lines)


def generated_inline_paths(paths):
    return ", ".join(f"`{path}`" for path in paths)


def generated_docker_paths(paths):
    return "\n".join(paths)


def without_template_only(paths, template_only):
    return [
        path for path in paths
        if not any(
            path == exempt or (exempt.endswith("/") and path.startswith(exempt))
            for exempt in template_only
        )
    ]


def replace_region(content, replacement, path, begin_marker, end_marker):
    begin_count = content.count(begin_marker)
    end_count = content.count(end_marker)
    if begin_count == 0 and end_count == 0:
        return None
    if begin_count != 1 or end_count != 1:
        raise ValueError(f"{path}: expected exactly one generated-region marker pair")
    start = content.index(begin_marker) + len(begin_marker)
    finish = content.index(end_marker)
    if content.index(begin_marker) > content.index(end_marker):
        raise ValueError(f"{path}: generated-region markers are out of order")
    return content[:start] + "\n" + replacement + "\n" + content[finish:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated views are stale")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        index = read_index(root)
        targets = (
            (pathlib.Path("README.md"), BEGIN, END, generated_text(pathlib.Path("README.md"), index["phases"])),
            (pathlib.Path(".github/prompts/ai-sdlc.prompt.md"), BEGIN, END,
             generated_text(pathlib.Path(".github/prompts/ai-sdlc.prompt.md"), index["phases"])),
            (pathlib.Path("CONTRIBUTING.md"), CHANGE_TYPES_BEGIN, CHANGE_TYPES_END,
             generated_change_types(index["change_types"])),
            (pathlib.Path("README.md"), README_PROJECT_BEGIN, README_PROJECT_END, "project"),
            (pathlib.Path("README.md"), README_PROCESS_BEGIN, README_PROCESS_END, "process"),
            (pathlib.Path(".dockerignore"), DOCKER_PROCESS_BEGIN, DOCKER_PROCESS_END, "process"),
        )
        originals = {path: (root / path).read_text() for path in {target[0] for target in targets}}
        replacements = dict(originals)
        for path, begin_marker, end_marker, generated in targets:
            registry_target = PATH_REGISTRY.get((path, begin_marker, end_marker))
            if registry_target:
                key, format_name, hide_template_only = registry_target
                paths = index[key]
                if hide_template_only:
                    paths = without_template_only(paths, index.get("template_only", []))
                generated = (generated_docker_paths(paths) if format_name == "docker"
                             else generated_inline_paths(paths))
            updated = replace_region(replacements[path], generated, path, begin_marker, end_marker)
            if updated is not None:
                replacements[path] = updated
        stale = [path for path in originals if originals[path] != replacements[path]]
        if not args.check:
            for relative_path in stale:
                (root / relative_path).write_text(replacements[relative_path])
        if args.check and stale:
            print("Generated views are stale: " + ", ".join(path.as_posix() for path in stale), file=sys.stderr)
            return 1
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
