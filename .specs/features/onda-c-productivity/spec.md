# Feature: onda-c-productivity

> Onda C — pause/resume cross-feature; discuss vs specify modes for Júri; design-state.py inspector.

**Source plan:** `docs/design-spec-driven-plan.md` REQ-C1..REQ-C3.

## REQs

- **REQ-C1** `/design-spec pause` writes `.design-spec/pause-state.yaml` with active feature/phase/task/timestamp; `/design-spec resume` reads + summarizes + asks "continue or re-prioritize?". After >14d → suggest light re-discovery.
- **REQ-C2** `/juri discuss <topic>` informal, no docs. `/juri specify <feature>` formal (existing discovery flow).
- **REQ-C3** `python scripts/design-state.py` outputs current feature/phase/task/blocked/last commit; `--feature` scopes; `--json` machine-readable.

## Acceptance

- [ ] `pause-state.yaml` written/read correctly (round-trip).
- [ ] `/juri discuss` produces zero file diffs.
- [ ] `design-state.py --json` valid in <2s.
- [ ] STATE.md updated with Onda C.
