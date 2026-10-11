# Invariants

1. **Every offered slot came from provider state.**
2. **Every confirmed slot was previously offered.**
3. **The confirmed slot equals the caller's selected slot.**
4. **Uncertainty exits to handoff instead of inventing state.**
5. **Changing the selected time clears the prior confirmation path.**
6. **An empty provider result never becomes a guessed appointment.**

The conversation can be flexible. The side effect cannot.

7. **Qualification is explicit, not truthiness-based.** Only actual Boolean `eligible=True` and `confident=True` can proceed to the offer state. Raw `"false"`, numeric `1`, missing values, and unrecognized states must hand off.
