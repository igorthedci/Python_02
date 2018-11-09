import requests
import unittest


class BooksPositiveTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/books"

    def setUp(self):
        self.book_data = [
            {"title": "Title1", "author": "Author1"},
            {"title": "Anna Karenina", "author": "Lev Tolstoy"}
        ]
        self.book_ids = []

    def tearDown(self):
        for book_id in self.book_ids:
            requests.delete(self.url + "/" + str(book_id))
            # print(r.status_code)
        return

    def test_create_book(self):  # CREATE
        for item in self.book_data:
            with self.subTest(item=item):
                response = requests.post(self.url, data=item)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.assertIn("id", body)
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                for key in item:
                    self.assertEqual(str(item[key]).strip(), str(body[key]))
        return True


if __name__ == "__main__":
    unittest.main(verbosity=2)
