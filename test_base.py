import requests
import unittest


class BaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com/"

    def test_base_url(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        return

    def test_base_links(self):
        response = requests.get(self.base_url)
        response_body = response.json()
        expected_body = {"Roles": self.base_url + "roles", "Books": self.base_url + "books"}
        self.assertEqual(response_body, expected_body)
        return 


