from HtmlTestRunner import HTMLTestRunner
import requests
import unittest


class BaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"

    def test_base_url(self):  # is the root is live
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        return

    def test_404_url(self):  # is 404 page present
        url = self.base_url + '/' + 'reFR3ff'
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)
        return

    def test_base_links(self):  # the root contains two links, they are live too
        response = requests.get(self.base_url)
        response_body = response.json()
        expected_body = {"Roles": self.base_url + "/roles", "Books": self.base_url + "/books"}
        self.assertEqual(response_body, expected_body)
        url = self.base_url + "/roles"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        url = self.base_url + "/books"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        return


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output=r"./"))
    #
