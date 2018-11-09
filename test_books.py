import requests
import unittest
from HtmlTestRunner import HTMLTestRunner


class BookPositiveTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/books"
        return True

    def setUp(self):
        self.books = [
            {"title": "Title1", "author": "Author1"},
            {"title": "Title1 Title2", "author": "Author1 Author2"},
            {"title": "Anna Karenina", "author": "Lev Tolstoy"}
        ]
        self.book_ids = []
        return True

    def tearDown(self):
        for book_id in self.book_ids:
            requests.delete(self.url + "/" + str(book_id))
        return True

    def test_book_create(self):  # CREATE
        for book in self.books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                for key in book:
                    self.assertEqual(str(book[key]).strip(), str(body[key]))
        return True

    def test_book_read(self):  # READ
        for book in self.books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                body = requests.get(self.url + '/' + str(body["id"])).json()
                for key in book:
                    self.assertEqual(str(book[key]).strip(), str(body[key]))
        return True

    def test_book_update(self):  # UPDATE
        for book in self.books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                for key in body:
                    if str(body[key]).isalpha():
                        body[key] += 'update'
                #
                response = requests.put(self.url + '/' + str(body["id"]))
                body = response.json()
                self.assertEqual(response.status_code, 200)  # check code === 200
                for key in book:
                    self.assertEqual(str(book[key]).strip(), str(body[key]))
        return True

    def test_book_delete(self):  # DELETE
        for book in self.books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                response = requests.delete(self.url + '/' + str(body["id"]))
                self.assertEqual(response.status_code, 204)  # check code === 204
        return True


class BookNegativeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/books"
        cls.keys = ['title', 'author']
        return True

    def setUp(self):
        self.invalid_books = [
            {},
            {"title": ""},
            {"author": ""},
            {"title": 0, "author": None}
        ]
        self.valid_book = {"title": "Title1", "author": "Author1"}
        self.book_ids = []
        return True

    def tearDown(self):
        for book_id in self.book_ids:
            requests.delete(self.url + "/" + str(book_id))
        return True

    def test_book_create(self):  # negative CREATE
        for book in self.invalid_books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                if response.status_code == 201:
                    body = response.json()
                    self.book_ids.append(body["id"])  # save id for tearDown()
                    print(response.status_code, body)
#                self.assertEqual(response.status_code, 201)  # check code === 201
                self.assertNotEqual(response.status_code, 201)  # check code === 201
                #
        return False

    def test_book_read(self):  # negative READ
        invalid_ids = [
            "0",
            " 10",
            "d"
        ]
        for item in invalid_ids:
            with self.subTest(item=item):
                url = self.url + '/' + str(item)
                response = requests.get(url)
                self.assertEqual(response.status_code, 404)  # check code === 404
                #
        return False

    def test_book_update(self):  # negative UPDATE
        invalid_puts = [
            {"title": ""},
            {"author": ""}
        ]
        response = requests.post(self.url, data=self.valid_book)  # create an item
        body = response.json()
        valid_id = body["id"]
        valid_url = self.url + "/" + str(valid_id)
        self.book_ids.append(valid_id)  # save id for tearDown()
        for item in invalid_puts:
            with self.subTest(item=item):
                response = requests.put(valid_url, data=item)  # update the item
                # body = response.json()
                # print(response.status_code, body)
                self.assertEqual(response.status_code, 400)  # check code === 400
                #
        return False

    def test_book_delete(self):  # negative DELETE
        invalid_puts = [
            {"title": ""},
            {"author": ""}
        ]
        response = requests.post(self.url, data=self.valid_book)  # create an item
        body = response.json()
        valid_id = body["id"]
        valid_url = self.url + "/" + str(valid_id)
        self.book_ids.append(valid_id)  # save id for tearDown()
        for item in invalid_puts:
            with self.subTest(item=item):
                response = requests.put(valid_url, data=item)  # update the item
                # body = response.json()
                # print(response.status_code, body)
                self.assertEqual(response.status_code, 400)  # check code === 400
                #
        return False

    def test_book_delete(self):  # DELETE
        invalid_ids = [
            "0",
            " 10",
            "d"
        ]
        for book in self.books:
            with self.subTest(book=book):
                response = requests.post(self.url, data=book)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.book_ids.append(body["id"])  # save id for tearDown()
                #
                response = requests.delete(self.url + '/' + str(body["id"]))
                self.assertEqual(response.status_code, 204)  # check code === 204
        return True


if __name__ == "__main__":
    unittest.main()
    # unittest.main(verbosity=2, testRunner=HTMLTestRunner(output=r"./"))
