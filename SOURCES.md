# Sources

This repository now includes two groups of skills:

## 1. Core Custom Skills

These are the primary local methods that define the engineering delivery workflow in this repo:

- `project-hub`
- `spec-to-ship`
- `done-means-done`
- `skill-engineering`
- `session-to-skill-evolution`
- `independent-verification`
- `acceptance-test-design`
- `stateful-product-validation`
- `external-system-reconciliation`
- `long-running-app-harness`

## 2. Bundled Companion Skills

These skills are bundled so that users who pull this repository can get behavior closer to the author's local Codex environment instead of a partial workflow.

Bundled companion skills:

- `brainstorming`
- `writing-plans`
- `requesting-code-review`
- `test-driven-development`
- `using-git-worktrees`
- `verification-before-completion`
- `systematic-debugging`
- `frontend-design`
- `design-taste-frontend`

## Compatibility Notes

- Some bundled companion skills are derived from third-party skill sets and were locally adapted for compatibility with this repository's workflow.
- In particular, compatibility adjustments were applied so that these skills do not override:
  - the current repository's document paths
  - the `project-hub -> spec-to-ship -> done-means-done` control flow
  - the current independent verification model
  - the current lightweight-change protocol
- This means the bundled versions may intentionally differ from their original upstream variants.

## Reproducibility Goal

The purpose of bundling these companion skills is practical reproducibility:

- users who install only this repository should get behavior closer to the author's real working environment
- the repository should no longer rely on undocumented local-only companion skill edits
