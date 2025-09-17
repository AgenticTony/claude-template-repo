#!/usr/bin/env python3
"""
Minimal eval runner:
- Reads eval/tasks.yaml
- For each task, emits a run folder with:
  - prompt.txt       (what to paste into Claude Code for the Dev Agent)
  - review_prompt.txt (what to paste for the Reviewer Agent)
  - checklist.md     (acceptance criteria & doc-first reminders)
- Allows you to log quick outcomes (pass/fail, notes, token rough counts)

Why not "auto-drive" Claude? The CLI is interactive (tools, /agent use, shell.run).
You'll get higher reliability & lower token waste by running the Dev→Review loop
manually but *systematically*, logging results per task.

Extend later to shell out to `claude "..."` if you want, but start simple.
"""
import os, sys, yaml, datetime, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks.yaml"
OUT   = ROOT / "out"

DEV_AGENT_NAME = "Developer Agent"
REVIEW_AGENT_NAME = "Senior Reviewer Agent"

def load_tasks(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

DEV_TEMPLATE = """\
/agent use {dev_agent}
# TASK: {task_id}
# PROMPT:
{prompt}

# FOLLOW THIS SHAPE:
PLAN (bullets; cite official docs if infra/API/IaC/auth) ->
PATCH (small targeted hunks only) ->
TESTS (list added/updated tests) ->
RUN (exact commands e.g. `pytest -q` / `npm test`) ->
RISKS (edge cases, follow-ups)
"""

REVIEW_TEMPLATE = """\
/agent use {review_agent}
# REVIEW: {task_id}

Please audit the most recent diff using this structure:
ISSUES:
- [severity: high|med|low] file:line — one-line problem + fix hint
MISSING_TESTS:
- path::test_name — scenario to cover
SECURITY_PERF:
- bullets
STYLE_NITS:
- bullets (optional)
VERDICT:
- APPROVE | BLOCK — reason
IF_BLOCK_MINIMAL_PATCH:
- tiny diff or checklist for high/med items

If infra/API/IaC/auth changed, search official docs first and reconcile.
"""

CHECKLIST = """\
# {task_id} — Checklist

- [ ] **Doc-first**: If infra/API/IaC/auth touched, use `ref.search_documentation`
      and paste URL + 2–3 bullets (official docs only).
- [ ] **Small diffs** only; no whole-file dumps. Use `git.diff` & line reads.
- [ ] **Tests added/updated** and **run locally** (`pytest -q` / `npm test`).
- [ ] **Tool responses** default to `"concise"`; request `"detailed"` only when IDs are needed.
- [ ] Reviewer returns **APPROVE/BLOCK** with minimal patch if BLOCK.
- [ ] Log outcome in `result.json`.

## Quick logging template
Create `result.json` with something like:
{{
  "task_id": "{task_id}",
  "status": "pass | fail | partial",
  "tokens_estimate": {{
    "dev": 0,
    "review": 0
  }},
  "tool_calls": {{
    "ref.search_documentation": 0,
    "shell.run": 0,
    "other": 0
  }},
  "notes": "short notes"
}}
"""

def main():
    tasks = load_tasks(TASKS)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    OUT.mkdir(parents=True, exist_ok=True)
    session_dir = OUT / ts
    session_dir.mkdir()

    summary = []
    for t in tasks:
        task_id = t["id"]
        prompt  = t["prompt"]
        tdir = session_dir / task_id
        tdir.mkdir()
        (tdir / "prompt.txt").write_text(
            DEV_TEMPLATE.format(
                dev_agent=DEV_AGENT_NAME,
                task_id=task_id,
                prompt=prompt
            ),
            encoding="utf-8"
        )
        (tdir / "review_prompt.txt").write_text(
            REVIEW_TEMPLATE.format(
                review_agent=REVIEW_AGENT_NAME,
                task_id=task_id
            ),
            encoding="utf-8"
        )
        (tdir / "checklist.md").write_text(
            CHECKLIST.format(task_id=task_id),
            encoding="utf-8"
        )
        (tdir / "result.json").write_text(
            json.dumps({
                "task_id": task_id,
                "status": "pending",
                "tokens_estimate": {"dev": 0, "review": 0},
                "tool_calls": {"ref.search_documentation": 0, "shell.run": 0, "other": 0},
                "notes": ""
            }, indent=2),
            encoding="utf-8"
        )
        summary.append(f"- {task_id} → {tdir}")

    (session_dir / "_README.md").write_text(
        f"# Eval session {ts}\n\n" +
        "Folders created for each task. Paste `prompt.txt` into Claude using your Dev Agent,\n"
        "then `review_prompt.txt` with your Reviewer Agent. Update `result.json` after each.\n\n" +
        "\n".join(summary) + "\n",
        encoding="utf-8"
    )
    print(f"Eval session created: {session_dir}")
    for line in summary:
        print(line)

if __name__ == "__main__":
    main()