import unittest

from booking_workflow.guardrails import qualification_requires_handoff, validate_confirmation


class GuardrailTests(unittest.TestCase):
    def test_uncertain_qualification_hands_off(self):
        self.assertTrue(qualification_requires_handoff(eligible=True, confident=False))

    def test_ineligible_hands_off(self):
        self.assertTrue(qualification_requires_handoff(eligible=False, confident=True))

    def test_exact_selected_offered_slot_passes(self):
        validate_confirmation(
            selected_slot="11:00",
            offered_slots=("10:00", "11:00"),
            confirmed_slot="11:00",
        )

    def test_unoffered_slot_fails(self):
        with self.assertRaisesRegex(ValueError, "never_offered"):
            validate_confirmation(
                selected_slot="12:00",
                offered_slots=("10:00", "11:00"),
                confirmed_slot="12:00",
            )


if __name__ == "__main__":
    unittest.main()
