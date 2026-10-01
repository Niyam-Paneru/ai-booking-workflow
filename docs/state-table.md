# Booking state table

| Current state | Event | Next state | Side effect? |
|---|---|---|---|
| greeting | begin | qualify | no |
| qualify | eligible + confident | offer slot | no |
| qualify | ineligible or uncertain | handoff | no |
| offer slot | no usable availability | handoff | no |
| offer slot | caller selects offered slot | confirm | no |
| offer slot | caller selects unknown slot | handoff | no |
| confirm | exact selected slot confirmed | end | create booking |
| confirm | caller changes mind | offer slot | no |
| handoff | human takes over | end | external to this core |

The only booking side effect occurs after an offered slot and the caller's selected slot agree exactly.
