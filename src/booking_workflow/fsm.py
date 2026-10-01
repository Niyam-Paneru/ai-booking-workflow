from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass
class BookingSession:
    state: State = State.GREETING
    offered_slots: list[str] = field(default_factory=list)
    selected_slot: str | None = None

    def begin(self) -> State:
        if self.state is not State.GREETING:
            raise ValueError("session_already_started")
        self.state = State.QUALIFY
        return self.state

    def qualify(self, *, eligible: bool, confident: bool = True) -> State:
        self._require(State.QUALIFY)
        if not eligible or not confident:
            self.state = State.HANDOFF
        else:
            self.state = State.OFFER_SLOT
        return self.state

    def offer(self, slots: list[str]) -> tuple[str, ...]:
        self._require(State.OFFER_SLOT)
        cleaned = list(dict.fromkeys(slot.strip() for slot in slots if slot.strip()))
        if not cleaned:
            self.state = State.HANDOFF
            return ()
        self.offered_slots = cleaned
        return tuple(cleaned)

    def choose(self, slot: str) -> State:
        self._require(State.OFFER_SLOT)
        if slot not in self.offered_slots:
            self.state = State.HANDOFF
            self.selected_slot = None
            return self.state
        self.selected_slot = slot
        self.state = State.CONFIRM
        return self.state

    def confirm(self, slot: str) -> Booking:
        self._require(State.CONFIRM)
        if self.selected_slot is None or slot != self.selected_slot:
            raise ValueError("confirmation_does_not_match_selected_slot")
        if slot not in self.offered_slots:
            raise ValueError("confirmation_slot_was_never_offered")
        booking = Booking(slot=slot)
        self.state = State.END
        return booking

    def change_slot(self) -> State:
        self._require(State.CONFIRM)
        self.selected_slot = None
        self.state = State.OFFER_SLOT
        return self.state

    def finish_handoff(self) -> State:
        self._require(State.HANDOFF)
        self.state = State.END
        return self.state

    def _require(self, expected: State) -> None:
        if self.state is not expected:
            raise ValueError(f"expected_{expected.value}_got_{self.state.value}")
