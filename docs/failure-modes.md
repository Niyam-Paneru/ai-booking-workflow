# Failure modes

## Empty availability
No usable slots come back. Response: hand off instead of inventing one.

## Caller chooses an unoffered time
The request sounds reasonable but was never in provider state. Response: hand off.

## Confirmation drifts
The selected slot and the confirmed slot differ. Response: refuse the booking side effect.

## Low-confidence qualification
The assistant cannot reliably determine whether booking is appropriate. Response: hand off.

## Duplicate / messy provider slots
Provider output contains blanks or repeated values. Response: normalize while preserving real order.

## Mid-conversation change of mind
The caller changes slot after selection. Response: return to the offer state and clear the previous selection.
