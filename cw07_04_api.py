import requests
import unittest


class BaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = r"http://pulse-rest-testing.herokuapp.com"

    def test_base_url(self):
        response = requests.get(self.base_url)
        self.assertEqual(200, response.status_code)
        response_body = response.json()
        self.assertEqual(2, len(response_body))
        expected_dict = {"Roles": self.base_url+"/roles", "Books": self.base_url+"/books"}
        self.assertDictEqual(expected_dict, response_body)


class BookTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = r"http://pulse-rest-testing.herokuapp.com"
        cls.test_url = cls.base_url + r"/books"

    def setUp(self):
        self.book_data = {'title': 'Title1', 'author': 'New Author'}

    def test_create_book(self):
        response = requests.post(self.test_url, data=self.book_data)
        self.assertEqual(response.status_code, 201)
        response_body = response.json()
        self.assertIn("id", response_body)
        self.book_id = response_body['id']  # !!!!!!!!!!!!!!!
        self.book_data['id'] = response_body['id']
        print(self.book_id)
        for key in self.book_data:
            self.assertEqual(response_body[key], self.book_data[key])
#        self.assertEqual(book_data, response_body)
#        self.assertDictContainsSubset(response_body, book_data)
        self.book_data['id'] = response_body['id']

    def tearDown(self):
        response = requests.delete(self.test_url+'/'+str(self.book_id))
        print(response.status_code)


if __name__ == '__main__':
    unittest.main(verbosity=2)
