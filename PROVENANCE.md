# Provenance

This public workflow was rewritten from the booking state-machine ideas used in private DentSignal voice/receptionist work.

## Preserved

- qualify → offer → select → confirm → end/handoff states;
- provider-backed availability;
- exact selected-slot confirmation;
- human handoff for uncertainty.

## Rewritten for public review

Calendar/provider SDKs, clinic policy, persistence, patient data, telephony, and credentials are intentionally absent.

## Claim boundary

The repo demonstrates booking-state correctness. It does not claim a live clinic integration or current production deployment.
