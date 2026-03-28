# Engineering Delivery Skill Pack

Codex skills for disciplined engineering delivery.

This repository contains:

- core custom skills that define the primary engineering workflow
- bundled companion skills that make the published workflow closer to the author's real local Codex setup

The goal is to make Codex handle engineering work more like a rigorous delivery lead and less like a fast prototype generator.

It focuses on ten things:

- providing a single entrypoint skill when the user wants to reference only one skill
- turning ambiguous requests into requirements, PRDs, tech specs, plans, and execution trackers
- forcing real end-to-end closure instead of premature “done”
- designing explicit acceptance test cases before implementation
- validating stateful products by real user lifecycle paths
- reconciling local claims with external sources of truth
- separating implementer and verifier when self-signoff would be risky
- turning Codex session history into evidence-driven skill evolution
- designing the harness for long-running agentic or stateful systems before feature work
- engineering the skills themselves with the right design pattern when the workflow needs new or evolved skills

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

Source and compatibility notes: [SOURCES.md](./SOURCES.md)

## Included Skills

This repository now ships both:

- core custom skills
- bundled companion skills needed to reproduce the local workflow more faithfully

### `project-hub`

A single-entry skill for users who do not want to remember multiple skill names.

It decides whether the task needs:

- `spec-to-ship`
- `done-means-done`
- both together

It is a routing and orchestration layer, not a replacement for the underlying skills.

### `spec-to-ship`

Turns vague feature work into:

- requirements
- PRD
- tech spec
- implementation plan
- execution tracker
- verified delivery

It now also emphasizes:

- rebaselining when the product shape changes
- requiring acceptance test matrices instead of abstract acceptance bullets
- routing stateful product work to lifecycle-focused validation
- separating local inference from external sources of truth

### `done-means-done`

Pushes work to a real finish line. It is explicitly designed to prevent:

- stopping at a partial implementation
- optionalizing in-scope follow-up work
- making completion claims without evidence
- treating pre-bug-fix validation as still valid after the user reports an issue

It now also emphasizes:

- user-journey-level acceptance cases
- formal-entry and real-path verification
- reconciliation with external systems
- redefining done when the product shape changes midstream
- light process for small changes without light thinking about impact or regression
- blocking completion until independent verifier issues are re-verified

### `independent-verification`

Separates implementer and verifier when a task cannot safely rely on self-signoff.

It focuses on:

- adversarial verification
- structured verification issues
- issue lifecycle and re-verification
- impact-surface and regression-point review
- blocking completion until evidence is independently confirmed

### `acceptance-test-design`

Turns feature requirements into explicit acceptance cases covering:

- user journeys
- visual outcomes
- interaction states
- functional outcomes
- edge cases
- regression paths

### `stateful-product-validation`

For chat, session-based, async, polling, streaming, attachment-heavy, and lifecycle-heavy products.

Its purpose is to catch cases where APIs look healthy but real user experience is still broken.

### `external-system-reconciliation`

For tasks involving third-party APIs, remote services, deployment state, payments, notifications, device state, or any external authority-backed system.

Its purpose is to catch cases where local logs or UI messages claim success but the external system does not agree.

### `session-to-skill-evolution`

For cases where you want to inspect one or more Codex sessions, a day of sessions, or a date range of sessions, extract how the user actually guides Codex, identify recurring execution failures, and convert those findings into skill updates.

It supports scoped updates:

- update only a named root skill and its recursively related skills
- or, if no scope is specified, update the global skill set and the current project skill set

### `skill-engineering`

For creating, updating, splitting, merging, slimming, or optimizing skills themselves.

It helps choose the right structure first:

- Tool Wrapper
- Generator
- Reviewer
- Inversion
- Pipeline
- or a combination of them

## Bundled Companion Skills

To make `project-hub` behave more like it does in the author's local Codex environment, this repository now also bundles these companion skills:

- `brainstorming`
- `writing-plans`
- `requesting-code-review`
- `test-driven-development`
- `using-git-worktrees`
- `verification-before-completion`
- `systematic-debugging`
- `frontend-design`
- `design-taste-frontend`

Some of these companion skills include local compatibility adjustments so they respect this repository's document paths, orchestration rules, and independent-verification model.

### `long-running-app-harness`

For agents, bots, schedulers, workers, queues, webhooks, long-running services, or any system that must be observable, replayable, and recoverable over time.

It forces harness-first thinking:

- repo-resident knowledge entrypoints
- one-command boot and isolation
- mechanical invariants
- runtime signals and observability
- evaluation gates
- verifier issue ledger and continuation packet
- kill switch and rollback

## Installation

Copy the skill directories under `skills/` into your Codex skills directory:

```bash
cp -R skills/* ~/.codex/skills/
```

If your environment uses `$CODEX_HOME/skills`, copy them there instead.

## Recommended Prompting

These skills work best when the user is explicit about outcome, completion, and verification.

Good prompt shape:

1. State the goal
2. State the required output
3. State that in-scope work should be finished end-to-end
4. State any important validation expectations

Example:

```text
Use $spec-to-ship and $done-means-done for this task.
Turn this request into requirements, a PRD, a tech spec, a plan, implementation, verification, and closeout.
Do not stop while in-scope work, validation, review fixes, or doc updates remain.
```

If you want a single skill entrypoint:

```text
Use $project-hub for this task.
Decide whether it needs $spec-to-ship, but always finish it to $done-means-done quality.
```

If you want Codex to learn from previous sessions and update skills:

```text
Use $session-to-skill-evolution for these session IDs or this date range.
Analyze how I guided Codex, identify recurring execution failures, and update the right skills in scope.
If I specify a root skill such as $project-hub, only update that skill and its recursively related skills.
```

If the task is UI-heavy:

```text
Use $done-means-done for this task.
This is a user-facing interface, so treat layout, interaction quality, readability, and mobile behavior as part of completion.
```

If the task is likely to produce user acceptance bugs:

```text
Use $acceptance-test-design before implementation and write explicit acceptance cases for user journeys, edge cases, and regression paths.
```

If the task is chat, session, streaming, async, polling, or lifecycle-heavy:

```text
Use $stateful-product-validation and make sure verification covers first-use, continued-use, slow-response, and recovery paths.
```

If the task depends on third-party or remote truth:

```text
Use $external-system-reconciliation and verify user-visible results against the external source of truth before claiming success.
```

If the task is a long-running app, bot, worker, or scheduler:

```text
Use $long-running-app-harness before deep implementation.
Define the harness first: knowledge entrypoints, runtime signals, evaluation gates, safety rails, and rollback.
```

## Recommended Way To Give This Repo To Codex

In practice, the easiest way is to give Codex the repository link directly and ask it to install the skills from GitHub.

Recommended wording:

```text
Install the skills from https://github.com/muhe-code/engineering-delivery-skill-pack.git into my Codex skills directory.
Use the repo as the source of truth and install these skills:
- project-hub
- spec-to-ship
- done-means-done
- skill-engineering
- acceptance-test-design
- stateful-product-validation
- external-system-reconciliation
- session-to-skill-evolution
- independent-verification
- long-running-app-harness
- brainstorming
- writing-plans
- requesting-code-review
- test-driven-development
- using-git-worktrees
- verification-before-completion
- systematic-debugging
- frontend-design
- design-taste-frontend
```

If your Codex environment supports a skill installer workflow, this usually works better than manually pasting long skill files into chat.

## How Third-Party-Derived Companion Skills Are Handled

This repository does bundle companion skills when they are part of the author's real local workflow and are needed for practical reproducibility.

The rule is:

- core custom skills in this repo are the primary method
- companion skills are bundled here when the local workflow depends on compatibility-adjusted versions
- bundled companion skills are not presented as original work from this repo
- source and compatibility notes live in [SOURCES.md](./SOURCES.md)

This means the current repository is intentionally an installable workflow pack, not only a minimal custom-skill showcase.

## Repository Layout

```text
skills/
  <core custom skills>
  <bundled companion skills>
```

For the exact inventory and origin status of each skill, see [SOURCES.md](./SOURCES.md).

## License

This repository is released under the [MIT License](./LICENSE).
