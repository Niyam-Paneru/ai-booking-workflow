from __future__ import annotations


def qualification_requires_handoff(*, eligible: bool, confident: bool) -> bool:
    # Input often comes from untyped JSON/transcripts. "false" and 1 are
    # truthy in Python, but neither is an explicit yes from the caller.
    return eligible is not True or confident is not True


def validate_confirmation(
    *,
    selected_slot: str | None,
    offered_slots: tuple[str, ...] | list[str],
    confirmed_slot: str,
) -> None:
    if selected_slot is None or confirmed_slot != selected_slot:
        raise ValueError("confirmation_does_not_match_selected_slot")
    if confirmed_slot not in offered_slots:
        raise ValueError("confirmation_slot_was_never_offered")
