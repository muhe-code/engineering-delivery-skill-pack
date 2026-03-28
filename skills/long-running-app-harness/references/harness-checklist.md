# Harness Checklist

## 1. Knowledge Entry

- Root entrypoint doc exists
- Deeper docs are linked, not hidden in chat history
- Source-of-truth files are explicit

## 2. Boot & Isolation

- One-command boot exists
- Local env and secrets path are explicit
- Isolation strategy exists: worktree, sandbox, containers, or equivalent

## 3. Mechanical Invariants

- Formatting / lint / schema / dependency boundaries are machine-enforced
- Critical architecture boundaries are not only written, but checked

## 4. Runtime Legibility

- Structured logs exist
- Health surface exists
- Metrics or equivalent counters exist
- External interactions can be observed or queried
- At least one user-visible path can be replayed

## 5. Evaluation Gates

- Capability coverage ledger exists
- Happy path coverage exists
- Negative path coverage exists
- Recovery / resumed path coverage exists
- Long-horizon observation path exists

## 6. Safety & Rollback

- Kill switch / disable path exists
- Rollback playbook exists
- Least-privilege credentials and egress boundaries are explicit
