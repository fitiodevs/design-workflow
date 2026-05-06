# Ralph — audit log schema (JSONL)

## File location

`.design-spec/features/<feature>/loop-log/<YYYY-MM-DD>.jsonl`

One file per UTC date. Append-only — never rotated, never truncated by Ralph (ops decision).

## Per-line schema

```json
{
  "ts": "2026-05-02T10:00:00Z",
  "tier": "watch | mechanical | composer",
  "tick_index": 7,
  "loop_id": "<uuid generated at loop start>",
  "task_id": "T-03 | null",
  "skill": "/theme-port | null",
  "input_tokens": 4200,
  "output_tokens": 1800,
  "cost_usd": 0.027,
  "duration_ms": 8400,
  "verify_result": "pass | fail | n/a",
  "verify_command": "flutter analyze ... | null",
  "commit_hash": "ab12cd3 | null",
  "halt_reason": "halt_file | budget_exceeded:tokens | requires_human:<reason> | branch_protection | cycle_detected | verify_fail_2x:T-03 | external_signal | gate_failure | null",
  "files_touched": ["lib/.../page.dart", ...],
  "warnings": ["budget_80pct_tokens", "drift_detected_juri", ...]
}
```

## Required fields

- `ts`, `tier`, `tick_index`, `loop_id` — always present.
- `halt_reason` — present and non-null on the last entry of any halted loop.

Optional fields use `null` (not omitted) for parser stability.

## Querying

DuckDB-friendly:

```sql
SELECT
  date_trunc('day', cast(ts as timestamp)) AS day,
  sum(cost_usd) AS daily_cost,
  count(*) AS ticks
FROM read_json_auto('.design-spec/features/*/loop-log/*.jsonl')
GROUP BY 1
ORDER BY 1 DESC;
```

## Retention

- Default: never delete (audit trail).
- Ops can compress old logs (e.g. `gzip` files older than 90 days).
- Ralph never reads its own old logs (no learning from history); ops uses them for cost / quality dashboards.

## Anti-patterns

- ❌ Mutating an entry post-write. Always append.
- ❌ Multi-line JSON entries. JSONL = exactly one JSON object per line.
- ❌ Skipping `halt_reason: null` when not halted. Always emit the field.
- ❌ Storing secrets (API keys, user PII) in the log. Audit log is shareable; sanitize.
