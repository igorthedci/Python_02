import requests
import unittest
from HtmlTestRunner import HTMLTestRunner
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


class RolePositiveTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/roles"
        return True

    def setUp(self):
        self.roles = [
            {'name': 'Name1', 'type': 'type1', 'level': 1, 'book': 2},
            {'level': 1, 'book': 2, 'name': 'Name1', 'type': 'type1'},
            {'name': 'Name2 Name2', 'type': 'type2 type2', 'level': 1, 'book': 2}
        ]
        self.role_ids = []
        return True

    def tearDown(self):
        for role_id in self.role_ids:
            requests.delete(self.url + "/" + str(role_id))
        return True

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
                self.assertEqual(response.status_code, 201)  # check code === 201
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
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                for key in body:
                    if str(body[key]).isalpha():
                        body[key] += 'update'
                #
                response = requests.put(self.url + '/' + str(body["id"]))
                body = response.json()
                self.assertEqual(response.status_code, 200)  # check code === 200
                for key in role:
                    self.assertEqual(str(role[key]).strip(), str(body[key]))
        return True

# 7● Удаляете этого персонажа методом DELETE roles/[id]
    def test_role_delete(self):
        for role in self.roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                #
                response = requests.delete(self.url + '/' + str(body["id"]))
                self.assertEqual(response.status_code, 204)  # check code === 204
        return True


class RoleNegativeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://pulse-rest-testing.herokuapp.com"
        cls.url = cls.base_url + "/roles"
        cls.keys = ['name', 'type', 'level', 'book']

    def setUp(self):
        self.invalid_roles = [
            {'name': '', 'type': 'type1', 'level': 1, 'book': 2},
            {'name': 'Name1', 'type': '', 'level': 1, 'book': 2},
            # {'name': 'Name1', 'type': 'type1', 'level': -1, 'book': 2},
            {'name': 'Name1', 'type': 'type1', 'level': 1, 'book': 0},
            # {'name': 'Name1', 'type': 'type1', 'book': 2},
            {'name': 'Name1', 'type': 'type1', 'level': 'aasd', 'book': 2}
        ]
        self.valid_roles = [
            {'name': 'Name1', 'type': 'type1', 'level': 1, 'book': 2}
        ]
        self.role_ids = []
        return

    def tearDown(self):
        for role_id in self.role_ids:
            requests.delete(self.url + "/" + str(role_id))
        return

    def isRoleValid(self, role={}):
        if len(role) != 4:   # all role elements are present
            return False
        akeys = role.keys()
        for akey in akeys:
            if akey not in self.keys:  # role keys are matched with expected list
                return False
        # check NAME, TYPE
        for i in range(2):
            ttt = role[self.keys[i]]
            if type(ttt) != str:
                return False
            ttt = ttt.strip()
            if not ttt.isalpha():
                return False
        # check LEVEL, BOOK
        for i in [2, 3]:
            ttt = role[self.keys[i]]
            if type(ttt) != int:
                return False
            if ttt < 1:
                return False
        #
        return True

# 1● Создаёт персонажа POST /roles/ с некорректными данными
#    @unittest.expectedFailure
    def test_role_create(self):
        for role in self.invalid_roles:
            with self.subTest(role=role):
                # self.assertFalse(isRoleValid(role))
                response = requests.post(self.url, data=role)  # create an item
                if response.status_code == 201:
                    body = response.json()
                    self.role_ids.append(body["id"])  # save id for tearDown()
                    print(body)
#                self.assertEqual(response.status_code, 201)  # check code === 201
                self.assertNotEqual(response.status_code, 201)  # check code === 201
                #
        return False

# 2● Проверяете, что отсутствующий персонаж недоступен по ссылкам GET/PUT/DELETE /roles/[id]
    def test_role_read(self):
        for role in self.valid_roles:
            with self.subTest(role=role):
                response = requests.post(self.url, data=role)  # create an item
                self.assertEqual(response.status_code, 201)  # check code === 201
                body = response.json()
                self.role_ids.append(body["id"])  # save id for tearDown()
                url_role = self.url + '/' + str(body["id"])
                #
                response = requests.delete(url_role)
                self.assertEqual(response.status_code, 204)  # check code === 204
                #
                response = requests.get(url_role)
                self.assertEqual(response.status_code, 404)  # check code === 404
                #
                response = requests.put(url_role)
                self.assertEqual(response.status_code, 404)  # check code === 404
                #
                response = requests.delete(url_role)
                self.assertEqual(response.status_code, 404)  # check code === 404
        return True


if __name__ == "__main__":

    roles_positive_suite = unittest.TestLoader().loadTestsFromTestCase(RolePositiveTests)
    result = roles_positive_suite.run()
    print(result)
#
    roles_negative_suite = unittest.TestLoader().loadTestsFromTestCase(RoleNegativeTests)
    result = roles_negative_suite.run()
    print(result)
#
    unittest.main(testRunner=HTMLTestRunner(output=r'./reports'))
    result = unittest.TestResult()
    print(result)
