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

class RolesTests(unittest.TestCase):

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

    def dict_contains(a={}, b={}):
        """
        :param a: dictionary
        :param b: dictionary
        :return: TRUE if A-dict contains B-dict
        """
        result = True
        for key in b:
            if key not in a or a[key] != b[key]:
                result = False
                break
        return result

    # url_books = 'http://pulse-rest-testing.herokuapp.com/books'
    # url_roles = 'http://pulse-rest-testing.herokuapp.com/roles'

# 1● Создаёт персонажа POST /roles/, вы запоминаете его id.
# 2● Проверяете, что он создался и доступен по ссылке GET /roles/[id]
# 3● Проверяете, что он есть в списке персонажа по GET /roles/
    def test_role_create(self):
        for role in self.roles:
            with self.subTest(role=self.roles):
                response = requests.post(self.url, data=role)
                self.assertEqual(response.status_code, 201)
                body = response.json()
                # self.assertDictContainsSubset(role, response.json(), )
                for key in role:
                    self.assertEqual(role[key].strip(), body[key])
                # TODO GET запросы
                self.role_ids.append(body["id"])
                #
                r = requests.get(self.base_url + 'role/' + str(body["id"]))
        hero_01 = {'name': 'Name1', 'type': 'type1', 'level': 1, 'role': 2}
        hero_01_id = requests.post(url_roles, hero_01).json()['id']
        print('Создан персонаж с номером', hero_01_id)
#    hero_01_id = 12

# 2● Проверяете, что он создался и доступен по ссылке GET /roles/[id]
    hero_test_url = url_roles + '/' + str(hero_01_id)
    hero_test = requests.get(hero_test_url).json()
    marker = dict_contains(hero_test, hero_01)
    print('Персонаж', 'существует' if marker else 'отсутствует.')

# 3● Проверяете, что он есть в списке персонажа по GET /roles/
    hero_list = requests.get(url_roles).json()
    marker = False
    for hero_test in hero_list:
        marker = dict_contains(hero_test, hero_01)
        if marker: break
    print('Персонаж', 'существует' if marker else 'отсутствует.')

# 4● Изменяете этого персонажа методом PUT roles/[id]/
    hero_01 = {'name': 'Name1new', 'type': 'type1new', 'level': 2, 'book': 2}
    hero_test_url = url_roles + '/' + str(hero_01_id)
    hero_test = requests.put(hero_test_url, hero_01).json()
    marker = dict_contains(hero_test, hero_01)
    print('Персонаж', 'обновлен' if marker else 'остался прежним.')

# 5● Проверяете, что он изменился и доступен по ссылке /roles/[id]
    hero_test_url = url_roles + '/' + str(hero_01_id)
    hero_test = requests.get(hero_test_url).json()
    marker = dict_contains(hero_test, hero_01)
    print('Изменение', 'правильно.' if marker else 'отсутствует.')

# 6● Проверяете, что он есть в списке персонажа по GET /roles/ с новой инфой
    hero_list = requests.get(url_roles).json()
    marker = False
    for hero_test in hero_list:
        marker = dict_contains(hero_test, hero_01)
        if marker: break
    print('Изменение', 'правильно.' if marker else 'отсутствует.')

# 7● Удаляете этого персонажа методом DELETE roles/[id]
    hero_test_url = url_roles + '/' + str(hero_01_id)
    hero_test = requests.delete(hero_test_url)
    print('Персонаж', hero_01_id, 'удален.' if hero_test.status_code == 204 else 'выжил.')

# 8● Второй скрипт: тоже самое с книгами
    book_01 = {'title': 'New Book', 'author': 'New Author'}
    book_01_id = requests.post(url_books, book_01).json()['id']
#    book_01_id = 820
    print('Создана книга с номером', book_01_id)
#
    book_test_url = url_books + '/' + str(book_01_id)
    book_test = requests.get(book_test_url).json()
    marker = dict_contains(book_test, book_01)
    if not marker:
        print('Запрос:', book_01)
        print('Ответ:', book_test)
    print('Книга', 'существует' if marker else 'отсутствует.')
#
    book_list = requests.get(url_books).json()
    marker = False
    for book_test in book_list:
        marker = dict_contains(book_test, book_01)
        if marker: break
    print('Книга', 'существует' if marker else 'отсутствует.')
#
    book_01 = {'title': 'Next Book', 'author': 'Edition 2'}
    book_test_url = url_books + '/' + str(book_01_id)
    book_test = requests.put(book_test_url, book_01).json()
    marker = dict_contains(book_test, book_01)
    print('Книга', 'переписана' if marker else 'осталась прежней.')
#
    book_test_url = url_books + '/' + str(book_01_id)
    book_test = requests.get(book_test_url).json()
    marker = dict_contains(book_test, book_01)
    print('Изменение', 'правильно.' if marker else 'отсутствует.')
#
    book_list = requests.get(url_books).json()
    marker = False
    for book_test in book_list:
        marker = dict_contains(book_test, book_01)
        if marker: break
    print('Изменение', 'правильно.' if marker else 'отсутствует.')
#
    book_test_url = url_books+'/'+str(book_01_id)
    book_test = requests.delete(book_test_url)
    print('Книга', book_01_id, 'удалена.' if book_test.status_code == 204 else 'сохранилась.')


if __name__ == "__main__":
    unittest.main(verbosity=2)
