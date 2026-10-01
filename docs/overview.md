# Design overview

This repository is intentionally about the **decision boundary**, not calendar-provider plumbing.

A booking assistant has three jobs:

1. understand whether a booking action is appropriate;
2. offer only slots it was actually given;
3. bind confirmation to the exact slot the caller selected.

Everything else is integration detail.

The public slice is split so those responsibilities are reviewable:

- `models.py` — states and the final booking value;
- `availability.py` — slot normalization without inventing availability;
- `guardrails.py` — handoff and confirmation rules;
- `fsm.py` — the conversation-state transitions.

The private DentSignal system adds provider integrations, persistence, clinic policy, voice, and handoff. Those parts are not required to review the core booking truth rule.
