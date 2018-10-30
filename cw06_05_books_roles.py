import requests

url_books = 'http://pulse-rest-testing.herokuapp.com/books'
url_roles = 'http://pulse-rest-testing.herokuapp.com/roles'

book_01 = {'title': 'Dragon Haven', 'author': 'Robin Hobb'}
r = requests.post(url_books, data=book_01)
print(r.status_code)
r_dict = r.json()
print(r_dict)

r2 = requests.delete(url_books+'/'+str(r_dict['id']))
print(r2.status_code)
print(r2.url)
# print(r2.json())
# r2_dict = r2.json()
# print(r2_dict)
