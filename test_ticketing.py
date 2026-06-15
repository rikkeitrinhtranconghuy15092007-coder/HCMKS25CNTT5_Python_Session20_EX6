import unittest
from main import calculate_total_revenue

class TestCalculateTotalRevenue(unittest.TestCase):

    def test_mixed_tickets(self):
        tickets = [
            {"ticket_id": "T01", "price": 500.0, "status": "Booked"},
            {"ticket_id": "T02", "price": 300.0, "status": "Cancelled"},
            {"ticket_id": "T03", "price": 700.0, "status": "Booked"}
        ]
        self.assertEqual(calculate_total_revenue(tickets), 1200.0)

    def test_empty_list(self):
        self.assertEqual(calculate_total_revenue([]), 0.0)

    def test_all_cancelled(self):
        tickets = [
            {"ticket_id": "T01", "price": 500.0, "status": "Cancelled"},
            {"ticket_id": "T02", "price": 300.0, "status": "Cancelled"}
        ]
        self.assertEqual(calculate_total_revenue(tickets), 0.0)

    def test_missing_price(self):
        tickets = [{"ticket_id": "T01", "status": "Booked"}]
        self.assertEqual(calculate_total_revenue(tickets), 0.0)


if __name__ == '__main__':
    unittest.main()