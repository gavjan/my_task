import requests

from enum import Enum
from async_get import async_get

DATA_URL = "https://random-data-api.com/api/v2/addresses"
COUNTRY_URL = "https://restcountries.com/v3.1/name"
class Result(Enum):
    SUCCESS = 0
    FATAL = 1
    RETRY = 2

def assert_int(s):
    try:
        return int(s)
    except:
        return None
def handle_country(res):
    # Assert response
    if res.status_code == 404:
        return 0, "No information found!"
    returned_countries = res.json()
    if not returned_countries:
        return 0, "No information found!"

    # Take first country
    country = returned_countries[0]

    # Check if required info fields are present
    if "languages" not in country or "capital" not in country or "population" not in country:
        return 0, "No information found!"

    # Assert Capital
    population = assert_int(country["population"])
    if not population:
        return 0, "No information found!"

    # Assert Capital
    if not country["capital"]:
        return 0, "No information found!"
    capital = country["capital"][0]

    # Parse Languages
    languages = ""
    for lang_key in country["languages"]:
        languages += f'{country["languages"][lang_key]}, '
    languages = languages or "No languages specified, "
    languages = languages[:-2]
    return population, f"{capital} - {population} - {languages}"




def handle(count, print_stream):
    # Assert Number
    num = assert_int(count)
    if not num:
        return Result.RETRY, "not a valid number, try again"
    if not (5 <= num <= 20):
        return Result.RETRY, "the number must be between 5 and 20"

    # Send Request
    res = requests.get(f"{DATA_URL}?size={num}")
    if res.status_code != 200:
        return Result.FATAL, "random-data-api.com not available right now"
    addresses = res.json()
    print_stream(addresses)

    # Extract Countries
    countries = []
    for addr in addresses:
        if "country" not in addr:
            return Result.FATAL, "random-data-api.com is misbehaving"

        countries.append(addr["country"])
    if not countries:
        return Result.FATAL, "empty response from random-data-api.com"

    # Make Unique
    countries = (list(set(countries)))

    parsed_countries = []
    for country in countries:

        res = requests.get(f"{COUNTRY_URL}/{country}")

        if res.status_code not in [200, 404]:
            return Result.FATAL, "restcountries.com not available right now"

        parsed_countries.append(handle_country(res))

    parsed_countries = sorted(parsed_countries, key=lambda x: x[0], reverse=True)
    for a in parsed_countries:
        print_stream(a)






