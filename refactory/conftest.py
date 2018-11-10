import pytest
import requests


@pytest.fixture()
def book():
    return ' Book_01 '


@pytest.fixture(scope="session")
def base_url():
    return "http://pulse-rest-testing.herokuapp.com/"


# @pytest.fixture()
# def book_data(base_url):
#     b = {'title': 'Title1', 'author': 'New Author'}
#     yield b
#     requests.delete(base_url+"book/"+str(b["id"]))


@pytest.fixture(scope="session")
def clean_book_ids(base_url):
    clean_book_ids = []
    yield clean_book_ids
    print(clean_book_ids)
    # to do: clean all
