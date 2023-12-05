import requests

BASE_URL = "https://sdcapi.datadrivendetroit.org"

def test_table_search():
    url = BASE_URL + "/1.0/table/search"
    response = requests.get(url, params={"q": "B0400"})

    data = response.json()

    assert data[0]["type"] == "table"
    assert data[0]["table_id"] == "B04004"
    assert data[1]["table_id"] == "B04005"


if __name__ == "__main__":
    test_table_search()


