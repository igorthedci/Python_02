import requests
import pytest
import json


with open("data_books.json", encoding="utf8") as f:
    books_data = json.load(f)


@pytest.mark.parametrize("book_data", books_data, ids=["...letter...", "...spec symbols.."])
def test_create_book(base_url, book_data, clean_book_ids):
    response = requests.post(base_url+"books/", data=book_data)
    assert response.status_code == 201
    response_body = response.json()
    assert "id" in response_body
    book_data["id"] = response_body["id"]
    assert book_data == response_body
    clean_book_ids.append(book_data["id"])


if __name__ == '__main__':
    pass
