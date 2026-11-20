# AI Booking Workflow

A caller asks for **2 PM**. The receptionist offered **10 AM and 11 AM**.

A very agreeable chatbot might say “Of course!” and invent an appointment. Unfortunately, the imaginary calendar can't tell the real receptionist.

I built this Python booking **state machine** so the assistant has to work with time slots it actually offered. It creates a booking value only after the caller confirms one of those slots.

## The appointments that don't exist

The normal sequence is **greeting → qualification → offer → confirmation → end**.

| Caller or system does this | What the state machine does |
| --- | --- |
| No availability supplied | Handoff; no invented appointment |
| Caller fails qualification or confidence threshold | Handoff |
| Caller selects an unoffered time | Handoff; don't invent availability |
| Caller selects an offered time, then changes their mind | Clear selection and return to offered slots |
| Confirmation differs from selected time | Error; don't create a booking |
| Caller confirms the selected, offered time | Create a Python booking value |

There is only one path that creates a booking value: selecting and confirming a time that was actually offered.

The code is split across [state transitions](src/booking_workflow/fsm.py), [availability cleanup](src/booking_workflow/availability.py), and [guardrails](src/booking_workflow/guardrails.py). Read the [state table](docs/state-table.md) for exact transitions and [behavior tests](docs/verification.md) for rejection cases.

## Important: “booking value” ≠ “calendar booking”

There is **no live calendar, provider SDK, database-backed reservation, final stale-slot revalidation, or external booking write** in this repository. It's a tested state machine, not a deployed receptionist.

A real booking integration would need fresh availability and a safely verified write. A returned Python value is not an appointment on a real calendar. [Provenance](PROVENANCE.md) · [verification](docs/verification.md).
