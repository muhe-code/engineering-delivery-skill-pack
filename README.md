# Engineering Delivery Skill Pack

Custom Codex skills for disciplined engineering delivery.

This repository contains a set of custom skills designed to help Codex handle engineering work more like a rigorous delivery lead and less like a fast prototype generator.

It focuses on eight things:

- providing a single entrypoint skill when the user wants to reference only one skill
- turning ambiguous requests into requirements, PRDs, tech specs, plans, and execution trackers
- forcing real end-to-end closure instead of premature “done”
- designing explicit acceptance test cases before implementation
- validating stateful products by real user lifecycle paths
- reconciling local claims with external sources of truth
- turning Codex session history into evidence-driven skill evolution
- designing the harness for long-running agentic or stateful systems before feature work

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

## Included Skills

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

### `long-running-app-harness`

For agents, bots, schedulers, workers, queues, webhooks, long-running services, or any system that must be observable, replayable, and recoverable over time.

It forces harness-first thinking:

- repo-resident knowledge entrypoints
- one-command boot and isolation
- mechanical invariants
- runtime signals and observability
- evaluation gates
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
- acceptance-test-design
- stateful-product-validation
- external-system-reconciliation
- session-to-skill-evolution
- long-running-app-harness
```

If your Codex environment supports a skill installer workflow, this usually works better than manually pasting long skill files into chat.

## Why This Repo Does Not Bundle Third-Party Companion Skills

This repository intentionally does not mirror third-party companion skills.

Reasons:

- to avoid repackaging upstream skills as if they were original to this repo
- to keep licensing and attribution boundaries clean
- to reduce maintenance burden when upstream skills evolve

If you want to reproduce the author’s broader workflow, you will usually also want companion skills such as:

- `brainstorming`
- `writing-plans`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `frontend-design`
- `design-taste-frontend`

Those are best installed from their own upstream sources.

## Repository Layout

```text
skills/
  acceptance-test-design/
  done-means-done/
  external-system-reconciliation/
  long-running-app-harness/
  project-hub/
  session-to-skill-evolution/
  spec-to-ship/
  stateful-product-validation/
```

## License

This repository is released under the [MIT License](./LICENSE).
