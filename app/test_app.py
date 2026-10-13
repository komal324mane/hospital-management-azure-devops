import unittest
from app import app, appointments

class HospitalAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.original_count = len(appointments)

    def tearDown(self):
        del appointments[self.original_count:]

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CarePoint Hospital", response.data)
        self.assertIn(b"Dr. Asha Mehta", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "healthy"})

    def test_valid_demo_appointment(self):
        response = self.client.post("/book", data={
            "patient": "Test Patient",
            "doctor": "Dr. Asha Mehta",
            "department": "Cardiology",
            "date": "2099-12-31",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Demo appointment added successfully.", response.data)
        self.assertTrue(any(a["patient"] == "Test Patient" for a in appointments))

    def test_invalid_doctor_is_rejected(self):
        response = self.client.post("/book", data={
            "patient": "Test Patient",
            "doctor": "Unknown Doctor",
            "department": "Cardiology",
            "date": "2099-12-31",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter valid demo appointment details.", response.data)

if __name__ == "__main__":
    unittest.main()
