# Provenance

This repository extracts the booking-state logic from earlier private voice/receptionist work and rewrites it as a small public package.

The public code keeps the parts that can be inspected independently: qualification, offered-slot tracking, exact selected-slot confirmation, state rejection, and human handoff.

It deliberately omits provider/calendar SDKs, persistence, patient or clinic data, telephony, credentials, and stale-slot revalidation. The slot list is an input to this package; the package does **not** prove where those slots came from.

The claim is therefore narrow: this repository demonstrates the state-machine boundary around a booking decision. It does not demonstrate a live clinic integration or current deployment.
