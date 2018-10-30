import requests
import unittest
"""
HW06_01
Тестовое приложение с REST API ​ ttp://pulse-rest-testing.herokuapp.com/
Создаём один скрипт:
1● Создаёт персонажа POST /roles/, вы запоминаете его id.
2● Проверяете, что он создался и доступен по ссылке GET /roles/[id]
3● Проверяете, что он есть в списке персонажа по GET /roles/
4● Изменяете этого персонажа методом PUT roles/[id]/
5● Проверяете, что он изменился и доступен по ссылке /roles/[id]
6● Проверяете, что он есть в списке персонажа по GET /roles/ с новой инфой
7● Удаляете этого персонажа методом DELETE roles/[id]
8● Второй скрипт: тоже самое с книгами

9● Попробуйте воспользоваться http.client вместо requests. Ощутите разницу
"""


class RoleTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/roles"

    def setUp(self):
        self.roles = [
            {'name': 'Name1', 'type': 'type1', 'level': 1, 'book': 2},
        ]
        self.role_ids = []
        return

    def tearDown(self):
        for role_id in self.role_ids:
            requests.delete(self.url + "/" + str(role_id))
        return

# 1● Создаёт персонажа POST /roles/, вы запоминаете его id.
    def test_role_create(self):
        for role in self.roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                for key in role:
                    self.assertEqual(str(role[key]).strip(), str(body[key]))
        return True

# 2● Проверяете, что персонаж создался и доступен по ссылке GET /roles/[id]
    def test_role_read(self):
        for role in self.roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                body = requests.get(self.url + '/' + str(body["id"])).json()
                for key in role:
                    self.assertEqual(str(role[key]).strip(), str(body[key]))
        return True

# 4● Изменяете этого персонажа методом PUT roles/[id]
    def test_role_update(self):
        for role in self.roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                for key in body:
                    if str(body[key]).isalpha():
                        body[key] += 'update'
                #
                body = requests.put(self.url + '/' + str(body["id"])).json()
                for key in role:
                    self.assertEqual(str(role[key]).strip(), str(body[key]))
        return True

# 7● Удаляете этого персонажа методом DELETE roles/[id]
    def test_role_delete(self):
        for role in self.roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                response = requests.delete(self.url + '/' + str(body["id"]))
                self.assertEqual(response.status_code, 204)  # check code === 204
                #
                response = requests.delete(self.url + '/' + str(body["id"]))
                self.assertEqual(response.status_code, 404)  # check code === 404
        return True


if __name__ == "__main__":
    unittest.main(verbosity=2)
