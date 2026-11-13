import unittest

from fastapi.testclient import TestClient

from orders_api import app


class CreateOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_quantity_one_is_accepted(self):
        response = self.client.post(
            "/orders", json={"product_id": "example", "quantity": 1}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"product_id": "example", "quantity": 1, "status": "accepted"},
        )

    def test_quantity_two_remains_accepted(self):
        response = self.client.post(
            "/orders", json={"product_id": "example", "quantity": 2}
        )

        self.assertEqual(response.status_code, 201)

    def test_non_positive_quantities_are_rejected(self):
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                response = self.client.post(
                    "/orders", json={"product_id": "example", "quantity": quantity}
                )
                self.assertEqual(response.status_code, 400)
