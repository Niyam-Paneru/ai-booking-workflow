import unittest

from booking_workflow.availability import normalize_slots


class AvailabilityTests(unittest.TestCase):
    def test_trims_and_deduplicates(self):
        self.assertEqual(
            normalize_slots([" 10:00 ", "10:00", "", "11:00"]),
            ("10:00", "11:00"),
        )

    def test_preserves_provider_order(self):
        self.assertEqual(
            normalize_slots(["13:00", "09:00", "11:00"]),
            ("13:00", "09:00", "11:00"),
        )


if __name__ == "__main__":
    unittest.main()
