import requests
import unittest


class BooksTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/books"

    def setUp(self):
        self.book_data = {"title": "Anna Karenina", "author": "Lev Tolstoy"}

    def test_create_book(self):

        response = requests.post(self.url, data=self.book_data)
        self.assertEqual(response.status_code, 201)
        response_body = response.json()
        self.assertIn("id", response_body)
        for key in self.book_data:
            self.assertEqual(response_body[key], self.book_data[key])

        self.book_data["id"] = response_body["id"]
        self.assertEqual(self.book_data, response_body)

    def tearDown(self):
        r = requests.delete(self.url+str(self.book_data["id"]))
        print(r.status_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
