from __future__ import annotations

from collections.abc import Iterable


def normalize_slots(slots: Iterable[str]) -> tuple[str, ...]:
    """Trim, drop blanks, and preserve first-seen order without duplicates."""
    cleaned: list[str] = []
    seen: set[str] = set()
    for raw in slots:
        if not isinstance(raw, str):
            raise ValueError("slot_must_be_string")
        slot = raw.strip()
        if not slot or slot in seen:
            continue
        cleaned.append(slot)
        seen.add(slot)
    return tuple(cleaned)
