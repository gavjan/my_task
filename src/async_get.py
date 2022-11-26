import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
MAX_WORKERS = 20

def fetch(session, _job):
    with session.get(_job['url']) as response:
        _job['json'] = response.json()
        _job['status_code'] = response.status_code
        return _job


async def get_data_asynchronous(_jobs, _callback):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, _job)
                )
                for _job in _jobs
            ]
            for response in await asyncio.gather(*tasks):
                _callback(response)


def async_get(_jobs, _callback):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(_jobs, _callback))
    loop.run_until_complete(future)


# Example
if __name__ == "__main__":
    jobs = [
        {'url': "https://restcountries.com/v3.1/name/unknown_country",
         'arg': 1},
        {'url': "https://restcountries.com/v3.1/name/poland",
         'arg': 2},
        {'url': "https://restcountries.com/v3.1/name/armenia",
         'arg': 3}
    ]

    def callback(job):
        print(f"{job['arg']}:{job['json']}")
        job['return'] = job['status_code']



    async_get(jobs, callback)
    for job in jobs:
        print(f"{job['arg']}: {job['return']}")