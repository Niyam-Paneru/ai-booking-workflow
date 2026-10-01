# AI Booking Workflow

A deterministic booking-state core that only creates a booking after the caller confirms a slot the system actually offered.

## Verify it

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests
```

Those are the checks used by [CircleCI](.circleci/config.yml).

![Booking state and decision flow](docs/workflow.svg)

## What the workflow enforces

1. `GREETING` can only advance to `QUALIFY`.
2. Qualification reaches `OFFER_SLOT` only when the caller is eligible **and** confidence is sufficient; otherwise it hands off.
3. Provider-supplied slots are trimmed and deduplicated without inventing new availability. No usable slots means handoff.
4. A caller selection reaches `CONFIRM` only when it is one of the stored `offered_slots`; an unknown slot hands off.
5. Confirmation creates `Booking(slot=...)` only when the confirmed slot exactly matches the selected slot and is still in `offered_slots`.
6. A confirmation mismatch raises an error and creates no booking. `change_slot()` clears the selection and returns to `OFFER_SLOT`.

## Code to inspect

| File | Responsibility |
|---|---|
| [`availability.py`](src/booking_workflow/availability.py) | Normalize provider slots without inventing any. |
| [`guardrails.py`](src/booking_workflow/guardrails.py) | Qualification handoff and exact-confirmation checks. |
| [`fsm.py`](src/booking_workflow/fsm.py) | Explicit booking states and transitions. |
| [`models.py`](src/booking_workflow/models.py) | State enum and final `Booking` value. |
| [`tests/`](tests/) | Availability, transition, and guardrail behavior. |

## Boundary

This public repository demonstrates the booking decision boundary, not a live booking integration. It contains no provider SDK, persistence layer, patient data, clinic credentials, telephony, or external calendar write.

It also does **not** implement stale-slot revalidation. The public proof ends when the validated state machine creates a `Booking` value; any real provider write would need its own integration and concurrency controls.

For the exact behavioral contract, see the [state table](docs/state-table.md), [invariants](docs/invariants.md), and [failure modes](docs/failure-modes.md). Provenance is documented in [`PROVENANCE.md`](PROVENANCE.md).
