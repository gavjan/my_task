import requests
import time
from enum import Enum
from async_get import async_get




MIN_COUNT = 5
MAX_COUNT = 20
DATA_URL = "https://random-data-api.com/api/v2/addresses"
COUNTRY_URL = "https://restcountries.com/v3.1/name"
class Result(Enum):
    SUCCESS = 0
    FATAL = -1
    RETRY = -2

def assert_int(s):
    try:
        return int(s)
    except:
        return None

def handle_country_wrapper(job):
    ret = handle_country(job)
    if ret == Result.FATAL:
        job['return'] = Result.FATAL
    else:
        job['return'] = ret[0], f"{job['country']}: {ret[1]}"

def handle_country(job):
    if job['status_code'] not in [200, 404]:
        return Result.FATAL

    # Assert response
    if job['status_code'] == 404:
        return 0, "No information found!"
    returned_countries = job['json']
    if not returned_countries:
        return 0, "No information found!"

    # Take first country
    country = returned_countries[0]

    # Check if required info fields are present
    if "languages" not in country or "capital" not in country or "population" not in country:
        return 0, "No information found!"

    # Assert Population
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
    if not (MIN_COUNT <= num <= MAX_COUNT):
        return Result.RETRY, "the number must be between 5 and 20"

    # Send Request
    start_time = time.time()
    res = requests.get(f"{DATA_URL}?size={num}")
    random_data_api_time = time.time() - start_time
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

    # Send GET Requests asynchronously
    jobs = [{'country': country, 'url': f"{COUNTRY_URL}/{country}"} for country in countries]
    start_time = time.time()
    async_get(jobs, handle_country_wrapper)
    print_stream("-----------------------------------\nDONE:")
    print_stream(f'random-data-api.com:\t{"%.2f" % (time.time()-start_time)}s')
    print_stream(f'restcountries.com x{count}:\t{"%.2f" % random_data_api_time}s')

    parsed_countries = [job['return'] for job in jobs]

    # Check if some request failed altogether
    if Result.FATAL in parsed_countries:
        return Result.FATAL, "restcountries.com not available right now"

    # Sort countries according to population
    parsed_countries = [x[1] for x in sorted(parsed_countries, key=lambda x: x[0], reverse=True)]

    return Result.SUCCESS, parsed_countries
