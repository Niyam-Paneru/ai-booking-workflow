# Decisions

## Never invent availability

The assistant may rephrase a slot, but it may not manufacture one. If the provider returns nothing usable, the state moves to handoff.

## Ambiguity is a handoff condition

Low confidence is not treated as “close enough.” Booking the wrong time is not a cute LLM mistake; it is an operational problem for two humans.

## Confirmation is content-bound

The confirmed slot must equal the selected slot **and** exist in the offered set. This blocks a later model/tool mismatch from quietly changing the action.

## Keep the FSM boring

The state machine is deliberately explicit. Clever control flow is harder to audit than a small list of states, and dental receptionists already have enough surprises.
