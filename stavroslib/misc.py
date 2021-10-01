import requests

# https://restcountries.eu/


def get_country_data(country: str) -> list:
    """Country Data

    Arguments:
        country {str} -- Country Name

    Returns:
        list -- Country Data
    """
    data = requests.get('https://restcountries.com/v2/name/' + country)
    return data.json()
