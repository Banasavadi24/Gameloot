import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        item = {
            "title": "Test Game",
            "type": "CD",
            "price": 10,
            "status": "available"
        }
        response = self.client.post('/items', json=item)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
