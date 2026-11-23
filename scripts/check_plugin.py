#!/usr/bin/env python3
"""Structural checks for the trustloop plugin. Run from the repository root; exits non-zero on any problem.

Checks:
- .claude-plugin/plugin.json and marketplace.json parse, and their names and versions agree with CHANGELOG.md.
- Every skill listed in plugin.json exists and its SKILL.md has YAML frontmatter with a name matching its
  folder and a non-empty description.
- Every Python script compiles.
- No live-looking API key text in tracked files (eval fixtures must assemble test values at scaffold time).
"""
import json
import pathlib
import py_compile
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
problems = []


def fail(msg):
    problems.append(msg)


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def main():
    try:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"manifest does not parse: {exc}")
        return

    if plugin.get("name") not in [p.get("name") for p in market.get("plugins", [])]:
        fail("marketplace.json does not list the plugin named in plugin.json")
    version = plugin.get("version", "")
    if f"## {version} " not in (ROOT / "CHANGELOG.md").read_text():
        fail(f"CHANGELOG.md has no entry for version {version}")

    for rel in plugin.get("skills", []):
        folder = (ROOT / rel).resolve()
        skill = folder / "SKILL.md"
        if not skill.is_file():
            fail(f"{rel}: SKILL.md missing")
            continue
        fm = frontmatter(skill.read_text())
        if fm is None:
            fail(f"{rel}/SKILL.md: no YAML frontmatter")
            continue
        if fm.get("name") != folder.name:
            fail(f"{rel}/SKILL.md: name '{fm.get('name')}' does not match folder '{folder.name}'")
        if not fm.get("description"):
            fail(f"{rel}/SKILL.md: empty description")

    for script in ROOT.rglob("*.py"):
        if "evals" in script.relative_to(ROOT).parts[:1]:
            continue
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"{script.relative_to(ROOT)}: does not compile: {exc.msg}")

    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    key = re.compile(r"\b(sk|rk)_live_[0-9A-Za-z]{16,}|\bAKIA[0-9A-Z]{16}\b|\bghp_[0-9A-Za-z]{30,}")
    for rel in tracked:
        path = ROOT / rel
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        if key.search(text):
            fail(f"{rel}: contains a live-looking key; assemble test values at scaffold time instead")


if __name__ == "__main__":
    main()
    for p in problems:
        print(f"::error::{p}")
    print(f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
