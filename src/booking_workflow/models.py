from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class State(str, Enum):
    GREETING = "greeting"
    QUALIFY = "qualify"
    OFFER_SLOT = "offer_slot"
    CONFIRM = "confirm"
    HANDOFF = "handoff"
    END = "end"


@dataclass(frozen=True)
class Booking:
    slot: str
