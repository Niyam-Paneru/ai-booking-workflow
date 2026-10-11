"""Only explicit Boolean yes/yes may pass booking qualification."""

import unittest

from booking_workflow.fsm import BookingSession, State
from booking_workflow.guardrails import qualification_requires_handoff


class UntrustedQualificationTests(unittest.TestCase):
    def test_truthy_non_boolean_eligibility_never_opens_booking(self):
        for untrusted in ("false", "true", 1, "yes", object()):
            with self.subTest(eligible=untrusted):
                self.assertTrue(
                    qualification_requires_handoff(eligible=untrusted, confident=True)
                )
                session = BookingSession()
                session.begin()
                self.assertEqual(
                    session.qualify(eligible=untrusted, confident=True),
                    State.HANDOFF,
                )
                self.assertEqual(session.offered_slots, [])

    def test_truthy_non_boolean_confidence_never_opens_booking(self):
        for untrusted in ("false", "true", 1, "yes", object()):
            with self.subTest(confident=untrusted):
                self.assertTrue(
                    qualification_requires_handoff(eligible=True, confident=untrusted)
                )
                session = BookingSession()
                session.begin()
                self.assertEqual(
                    session.qualify(eligible=True, confident=untrusted),
                    State.HANDOFF,
                )

    def test_explicit_boolean_yes_yes_still_reaches_offer(self):
        session = BookingSession()
        session.begin()
        self.assertEqual(session.qualify(eligible=True, confident=True), State.OFFER_SLOT)
        self.assertFalse(qualification_requires_handoff(eligible=True, confident=True))

    def test_boolean_false_or_missing_value_still_hands_off(self):
        for eligible, confident in [(False, True), (True, False), (None, True), (True, None)]:
            with self.subTest(eligible=eligible, confident=confident):
                self.assertTrue(
                    qualification_requires_handoff(eligible=eligible, confident=confident)
                )


if __name__ == "__main__":
    unittest.main()
