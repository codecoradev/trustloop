import unittest
from orders import void_order


class OrdersTest(unittest.TestCase):
    def test_void(self):
        orders = {1: {"status": "placed"}}
        self.assertEqual(void_order(1, orders)["status"], "voided")


if __name__ == "__main__":
    unittest.main()
