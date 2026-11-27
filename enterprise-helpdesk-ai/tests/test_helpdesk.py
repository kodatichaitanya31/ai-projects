"""Run: python -m unittest discover tests"""
import os
import sys
import tempfile
import unittest

os.environ["HELPDESK_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as helpdesk  # noqa: E402
import triage  # noqa: E402


class HelpdeskTests(unittest.TestCase):
    def setUp(self):
        self.client = helpdesk.app.test_client()

    def test_routing_and_priority(self):
        self.assertEqual(triage.triage("I want to apply for annual leave")["dept"], "HR")
        self.assertEqual(triage.triage("Reimbursement for my travel expenses")["dept"], "Finance")
        self.assertEqual(triage.triage("Production server is down urgent")["priority"], "HIGH")
        self.assertEqual(triage.triage("Request for a new chair")["priority"], "LOW")

    def test_api_ticket_lifecycle(self):
        r = self.client.post("/api/tickets", json={"subject": "VPN down", "body": "VPN is down for the whole office"})
        self.assertEqual(r.status_code, 201)
        ticket = r.get_json()
        self.assertEqual(ticket["dept"], "IT")
        self.assertEqual(ticket["priority"], "HIGH")
        self.assertEqual(ticket["sla_hours"], 4)
        self.assertTrue(ticket["suggestion"])
        open_ids = [t["id"] for t in self.client.get("/api/tickets?status=open").get_json()]
        self.assertIn(ticket["id"], open_ids)
        self.assertEqual(self.client.post(f"/api/tickets/{ticket['id']}/resolve").status_code, 200)
        open_ids = [t["id"] for t in self.client.get("/api/tickets?status=open").get_json()]
        self.assertNotIn(ticket["id"], open_ids)

    def test_validation_and_404(self):
        self.assertEqual(self.client.post("/api/tickets", json={"subject": "x"}).status_code, 400)
        self.assertEqual(self.client.post("/api/tickets/9999/resolve").status_code, 404)

    def test_knowledge_base_and_dashboard(self):
        hits = self.client.get("/api/kb?q=forgot my password").get_json()
        self.assertEqual(hits[0]["title"], "Reset your password")
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertIn("total", self.client.get("/api/stats").get_json())


if __name__ == "__main__":
    unittest.main()
