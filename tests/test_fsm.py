import unittest

from booking_workflow.fsm import BookingSession, State


class BookingWorkflowTests(unittest.TestCase):
    def ready(self):
        s = BookingSession()
        self.assertEqual(s.begin(), State.QUALIFY)
        self.assertEqual(s.qualify(eligible=True), State.OFFER_SLOT)
        return s

    def test_ineligible_goes_to_handoff(self):
        s = BookingSession()
        s.begin()
        self.assertEqual(s.qualify(eligible=False), State.HANDOFF)

    def test_low_confidence_goes_to_handoff(self):
        s = BookingSession()
        s.begin()
        self.assertEqual(s.qualify(eligible=True, confident=False), State.HANDOFF)

    def test_empty_availability_goes_to_handoff(self):
        s = self.ready()
        self.assertEqual(s.offer([]), ())
        self.assertEqual(s.state, State.HANDOFF)

    def test_slots_are_deduplicated(self):
        s = self.ready()
        self.assertEqual(s.offer(["10:00", "10:00", "11:00"]), ("10:00", "11:00"))

    def test_unoffered_choice_never_advances_to_confirm(self):
        s = self.ready()
        s.offer(["10:00"])
        self.assertEqual(s.choose("12:00"), State.HANDOFF)

    def test_offered_choice_advances(self):
        s = self.ready()
        s.offer(["10:00", "11:00"])
        self.assertEqual(s.choose("11:00"), State.CONFIRM)

    def test_confirm_must_match_selected_slot(self):
        s = self.ready()
        s.offer(["10:00", "11:00"])
        s.choose("11:00")
        with self.assertRaisesRegex(ValueError, "confirmation_does_not_match"):
            s.confirm("10:00")

    def test_exact_confirm_creates_booking_and_ends(self):
        s = self.ready()
        s.offer(["10:00"])
        s.choose("10:00")
        booking = s.confirm("10:00")
        self.assertEqual(booking.slot, "10:00")
        self.assertEqual(s.state, State.END)

    def test_change_mind_returns_to_offer(self):
        s = self.ready()
        s.offer(["10:00"])
        s.choose("10:00")
        self.assertEqual(s.change_slot(), State.OFFER_SLOT)
        self.assertIsNone(s.selected_slot)

    def test_bad_transition_fails(self):
        s = BookingSession()
        with self.assertRaises(ValueError):
            s.offer(["10:00"])


if __name__ == "__main__":
    unittest.main()
