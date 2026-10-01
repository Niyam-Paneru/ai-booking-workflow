# Walkthrough: “Tomorrow afternoon”

A caller asks:

> “Do you have anything tomorrow afternoon?”

Assume the provider returns:

- 14:00
- 15:30

The assistant may phrase those naturally, but those two values are the whole universe of bookable truth for this turn.

The caller chooses 15:30.

The session now holds:

- offered: 14:00, 15:30
- selected: 15:30
- state: confirm

If the confirmation tool is asked to create 15:30, the contract is satisfied.

If a later model turn suddenly asks to book 16:00, the guard rejects it because 16:00 was never offered.

If the caller says “Actually, can we do later?”, the old selection is cleared and the workflow returns to availability rather than silently mutating the booking.

The conversational layer gets freedom over wording. It does not get freedom over state.
