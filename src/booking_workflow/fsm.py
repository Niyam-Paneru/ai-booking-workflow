from __future__ import annotations

from dataclasses import dataclass, field

from .availability import normalize_slots
from .guardrails import qualification_requires_handoff, validate_confirmation
from .models import Booking, State


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
        self.state = (
            State.HANDOFF
            if qualification_requires_handoff(eligible=eligible, confident=confident)
            else State.OFFER_SLOT
        )
        return self.state

    def offer(self, slots: list[str]) -> tuple[str, ...]:
        self._require(State.OFFER_SLOT)
        cleaned = normalize_slots(slots)
        if not cleaned:
            self.state = State.HANDOFF
            return ()
        self.offered_slots = list(cleaned)
        return cleaned

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
        validate_confirmation(
            selected_slot=self.selected_slot,
            offered_slots=self.offered_slots,
            confirmed_slot=slot,
        )
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
