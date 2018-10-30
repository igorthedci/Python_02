import unittest
import sys
import requests


class CreateBookTests(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://pulse-rest-testing.herokuapp.com/"
        self.books = [
            {"title": "sdgfs", "author": "sdfds     "},
            {"title": "$%^&%&", "author": "sdfds"},
            {"title": "234234", "author": "243324"}
        ]
        self.book_ids = []

    @unittest.skipIf(sys.platform.startswith("darwin"), "Not implemented on MacOS version")
    def test_create_book_positive(self):
        for book in self.books:
            with self.subTest(book=self.books):
                response = requests.post(self.base_url + "books/", data=book)
                self.assertEqual(response.status_code, 201)
                body = response.json()
                # self.assertDictContainsSubset(book, response.json(), )
                for key in book:
                    self.assertEqual(book[key].strip(), body[key])
                # TODO GET запросы
                self.book_ids.append(body["id"])
                r = requests.get(self.base_url + 'book/' + str(body["id"]))

    @unittest.skip
    def test_create_book_withou_author(self):
        book = {"title": "sdfsdf"}
        response = requests.post(self.base_url + "books/", data=book)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        for book_id in self.book_ids:
            r = requests.delete(self.base_url + 'books/' + str(book_id) + "/")


if __name__ == "__main__":
    # from HtmlTestRunner import HTMLTestRunner
    # unittest.main(verbosity=2, testRunner=HTMLTestRunner(output=r"E:\workspace\untitled3"))
    unittest.main(verbosity=2)
    # # test2 = CreateBookTests("test_two")
    # # # test1.run()
    # # result = test2.run()
    # # print(result)
    # # test1 = CreateBookTests("one")
    # # result = test1.run()
    # # test1.test_two()
    # # test1.test_one()
    # test_suite = unittest.TestLoader().loadTestsFromTestCase(CreateBookTests)
    # # # test_suite.addTest(test1)
    # # # test_suite.addTest(test2)
    # result = unittest.TestResult()
    # test_suite.run(result)
    # print(result)
