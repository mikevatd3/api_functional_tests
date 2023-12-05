import requests
from icecream import ic

BASE_URL = "http://localhost:5000"
REFERENCE_API = "https://sdcapi.datadrivendetroit.org"
DETROIT_COSUB_GEOID = "06000US2616322000"
DETROIT_POPULATION = 645_658


def test_healthcheck():
    response = requests.get(BASE_URL + "/healthcheck")
    assert response.content == b"OK"


def test_get_data():
    acs = "acs2021_5yr"
    geoids = [DETROIT_COSUB_GEOID]
    table_ids = ["B01001"]  # Must be upper case

    response = requests.get(
        BASE_URL + f"/1.0/data/show/{acs}",
        params=dict(table_ids=",".join(table_ids), geo_ids=",".join(geoids)),
    )

    reference = requests.get(
        REFERENCE_API + f"/1.0/data/show/{acs}",
        params=dict(table_ids=",".join(table_ids), geo_ids=",".join(geoids)),
    )

    data = response.json()
    check = reference.json()

    assert sorted(data.keys()) == sorted(check.keys())
    assert sorted(data["geography"].values()) == sorted(
        check["geography"].values()
    )
    assert data["release"] == check["release"]
    assert (
        data["data"][DETROIT_COSUB_GEOID]["B01001"]["estimate"]["B01001001"]
        == DETROIT_POPULATION
    )


def test_get_parents():
    response = requests.get(
        BASE_URL + f"/1.0/geo/tiger2021/{DETROIT_COSUB_GEOID}/parents"
    )
    detroit, *_ = response.json()["parents"]

    assert detroit["relation"] == "this"
    assert detroit["display_name"] == "Detroit city, Wayne County, MI"


def test_geo_search():
    response = requests.get(
        BASE_URL + "/1.0/geo/search",
        params={
            "lat": 42.3,
            "lon": -83.14,
            "q": None,
            "sumlevs": ["140"],
            "geom": False,
        },
    )


def test_geo_tiles():
    url = BASE_URL + "/1.0/geo/tiger2021/tiles/140/10/275/378.geojson"

    response = requests.get(url)
    data = response.json()
    assert data["features"][0]["geometry"]["type"] == "Polygon"


def test_geo_lookup():
    url = BASE_URL + f"/1.0/geo/tiger2021/{DETROIT_COSUB_GEOID}"
    response = requests.get(url)

    data = response.json()

    assert data["type"] == "Feature"
    assert (
        data["properties"]["display_name"] == "Detroit city, Wayne County, MI"
    )


def test_get_specified_geo_data():
    url = BASE_URL + "/1.0/geo/show/tiger2021"

    response = requests.get(url, params={"geo_ids": ["05000US26163"]})

    data = response.json()

    assert data["type"] == "FeatureCollection"
    assert data["features"][0]["type"] == "Feature"


def test_table_search():
    url = BASE_URL + "/1.0/table/search"
    response = requests.get(url, params={"q": "B0400"})

    data = response.json()

    assert data[0]["type"] == "table"
    assert data[0]["table_id"] == "B04004"
    assert data[1]["table_id"] == "B04005"


def test_tabulation_details():
    url = BASE_URL + "/1.0/tabulation/04004"
    response = requests.get(url)

    data = response.json()
    assert data["tabulation_code"] == "04004"
    assert data["table_title"] == "People Reporting Single Ancestry"
    assert data["subject_area"] == "Ancestry"


def test_table_details():
    url = BASE_URL + "/1.0/table/B28001"
    response = requests.get(url, params={"acs": "acs2021_5yr"})

    data = ic(response.json())

    assert "simple_table_title" in data


def test_table_details_with_release():
    url = BASE_URL + "/2.0/table/acs2021_5yr/B01001"
    response = requests.get(url)

    data = response.json()

    assert "table_id" in data
    assert "topics" in data

    assert data["table_id"] == "B01001"


def test_table_geo_comparison_rowcount():
    url = BASE_URL + "/1.0/table/compare/rowcounts/B01001"

    response = requests.get(
        url,
        params={
            "year": 2021,
            "sumlevel": "140",
            "within": DETROIT_COSUB_GEOID,
        },
    )

    data = response.json()
    assert "acs2021_5yr" in data


def test_full_text_search():
    url = BASE_URL + "/2.1/full-text/search"

    response = requests.get(url, params={"q": "Detr"})
    assert response.status_code == 404


def test_show_specified_data():
    url = BASE_URL + "/1.0/data/show/acs2021_5yr"
    response = requests.get(
        url, params={"table_ids": ["B01001"], "geo_ids": [DETROIT_COSUB_GEOID]}
    )

    data = response.json()

    assert "tables" in data
    assert "data" in data
    assert (
        data["data"][DETROIT_COSUB_GEOID]["B01001"]["estimate"]["B01001001"]
        == DETROIT_POPULATION
    )


def test_download_specified_data_kml():
    url = BASE_URL + "/1.0/data/download/acs2021_5yr"
    response = requests.get(
        url,
        params={
            "table_ids": ["B01001"],
            "geo_ids": [DETROIT_COSUB_GEOID],
            "format": "kml",
        },
    )

    data = response.json()
    assert "error" not in data


def test_download_specified_data_csv():
    url = BASE_URL + "/1.0/data/download/acs2021_5yr"
    response = requests.get(
        url,
        params={
            "table_ids": ["B01001"],
            "geo_ids": [DETROIT_COSUB_GEOID],
            "format": "csv",
        },
    )

    data = response.json()
    assert "error" not in data


def test_download_specified_data_geojson():
    url = BASE_URL + "/1.0/data/download/acs2021_5yr"
    response = requests.get(
        url,
        params={
            "table_ids": ["B01001"],
            "geo_ids": [DETROIT_COSUB_GEOID],
            "format": "geojson",
        },
    )

    data = response.json()
    assert "error" not in data


def test_compare_geoids_with_parent():
    url = BASE_URL + "/1.0/data/compare/acs2021_5yr/B01001"

    response = requests.get(
        url,
        params={
            "within": DETROIT_COSUB_GEOID,
            "sumlevel": "140",
            "geom": False,
        },
    )

    data = response.json()

    assert "child_geographies" in data
    assert "comparison" in data


def test_pull_metadata():
    url = BASE_URL + "/metadata/tables/b01997"

    response = requests.get(url)

    data = response.json()
