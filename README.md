# AI Booking Workflow

**Assistant:** I have 10 AM or 11 AM.  
**Caller:** How about 2 PM?  
**Assistant:** You're booked!  
**Calendar:** Sorry, who?

I built this Python state machine to keep that conversation honest. It creates a booking value only when the caller confirms a time the workflow actually offered. No creative interpretation of the calendar.

## The calendar gets the last word

The normal sequence is **greeting → qualification → offer → confirmation → end**.

| Caller or system does this | What the state machine does |
| --- | --- |
| No availability supplied | Handoff; no invented appointment |
| Caller fails qualification or confidence threshold | Handoff |
| Caller selects an unoffered time | Handoff; don't invent availability |
| Caller selects an offered time, then changes their mind | Clear selection and return to offered slots |
| Confirmation differs from selected time | Error; don't create a booking |
| Caller confirms the selected, offered time | Create a Python booking value |

There is only one path that creates a booking value: selecting and confirming a time that was actually offered. Here's the whole decision in one picture; the table above covers the awkward details.

```mermaid
flowchart TB
    G["Greeting"] --> Q{"Eligible and confident?"}
    Q -- No --> H["Handoff; no booking"]
    Q -- Yes --> O["Offer supplied slots"]
    O -- "No slots or unoffered choice" --> H
    O -- "Select offered slot" --> C{"Confirm selected time?"}
    C -- "Exact match" --> B["Create booking value"]
    C -- "Change slot" --> O
    C -- "Mismatch" --> X["Error; no booking"]
```

The code is split across [state transitions](src/booking_workflow/fsm.py), [availability cleanup](src/booking_workflow/availability.py), and [guardrails](src/booking_workflow/guardrails.py). Read the [state table](docs/state-table.md) for exact transitions and [behavior tests](docs/verification.md) for rejection cases.

## Important: “booking value” ≠ “calendar booking”

There is **no live calendar, provider SDK, database-backed reservation, final stale-slot revalidation, or external booking write** in this repository. It's a tested state machine, not a deployed receptionist.

A real booking integration would need fresh availability and a safely verified write. A Python object is not a dentist's schedule, no matter how enthusiastic the chatbot sounds. [Provenance](PROVENANCE.md) · [verification](docs/verification.md).
