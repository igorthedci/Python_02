import pytest
import requests


@pytest.fixture()
def book():
    return ' Book_01 '


@pytest.fixture(scope="session")
def base_url():
    return "http://pulse-rest-testing.herokuapp.com"


@pytest.fixture()
def book_data(base_url):
    b = {'title': 'Title1', 'author': 'New Author'}
    yield b
    requests.delete(base_url+"book/"+str(b["id"]))


@pytest.fixture()
def clean(base_url):
    yield
    # to do: clean all
