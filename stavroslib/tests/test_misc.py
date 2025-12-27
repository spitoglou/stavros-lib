from stavroslib.misc import get_country_data


def test_get_country_data():
    data = get_country_data("Greece")
    assert "Greece" == data[0]["name"]
